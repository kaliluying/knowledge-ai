<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, shallowRef } from 'vue';
import { useRouter } from 'vue-router';
import { EditorView, basicSetup } from 'codemirror';
import { EditorState } from '@codemirror/state';
import { markdown } from '@codemirror/lang-markdown';
import { keymap } from '@codemirror/view';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { marked } from 'marked';
import { notesApi } from '@/api';

interface NoteSuggestion {
  id: number;
  title: string;
}

interface Props {
  modelValue: string;
  placeholder?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '开始书写你的笔记...（支持 Markdown 语法）',
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

const router = useRouter();
const editorContainer = ref<HTMLDivElement | null>(null);
const editorView = shallowRef<EditorView | null>(null);
const previewMode = ref(false);
const previewContent = ref('');

// Note mention popup state
const showNotePopup = ref(false);
const notePopupQuery = ref('');
const notePopupResults = ref<NoteSuggestion[]>([]);
const notePopupLoading = ref(false);
const notePopupPosition = ref({ top: 0, left: 0 });
const notePopupIndex = ref(0);
const notePopupInputRef = ref<HTMLInputElement | null>(null);

// Debounce function
function debounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return (...args: Parameters<T>) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// Search notes for popup
const searchNotes = debounce(async (query: string) => {
  if (!query) {
    notePopupResults.value = [];
    return;
  }

  notePopupLoading.value = true;
  try {
    const response = await notesApi.getSuggestions(query);
    if (response.code === 200 && response.data) {
      notePopupResults.value = response.data.slice(0, 10);
    }
  } catch (error) {
    console.error('Failed to search notes:', error);
    notePopupResults.value = [];
  } finally {
    notePopupLoading.value = false;
  }
}, 200);

// Show note popup
const showNoteMentionPopup = (query: string, position: { top: number; left: number }) => {
  notePopupQuery.value = query;
  notePopupPosition.value = position;
  notePopupIndex.value = 0;
  showNotePopup.value = true;
  searchNotes(query);
};

// Hide note popup
const hideNotePopup = () => {
  showNotePopup.value = false;
  notePopupQuery.value = '';
  notePopupResults.value = [];
};

// Insert note link
const insertNoteLink = (note: NoteSuggestion) => {
  if (!editorView.value) return;

  // Store the mapping for preview rendering
  noteLinkMappings.value[note.title] = note.id;

  const selection = editorView.value.state.selection.main;
  const cursorPos = selection.from;
  const doc = editorView.value.state.doc;

  // Get text after cursor to check for ]]
  const textAfter = doc.sliceString(cursorPos, Math.min(cursorPos + 5, doc.length));

  // Calculate how much to delete after cursor
  let deleteAfter = 0;
  if (textAfter.startsWith(']]')) {
    deleteAfter = 2;
  }

  // Build the link
  const link = `[${note.title}](/notes/${note.id})`;

  // Apply changes: delete closing ]] if present, then insert link
  editorView.value.dispatch({
    changes: [
      { from: cursorPos, to: cursorPos + deleteAfter, insert: link }
    ]
  });

  hideNotePopup();
};

// Handle note popup input
const handleNotePopupInput = () => {
  searchNotes(notePopupQuery.value);
};

// Handle note popup keydown
const handleNotePopupKeydown = (event: KeyboardEvent) => {
  if (!showNotePopup.value) return;

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault();
      notePopupIndex.value = Math.min(notePopupIndex.value + 1, notePopupResults.value.length - 1);
      scrollToSelectedNote();
      break;
    case 'ArrowUp':
      event.preventDefault();
      notePopupIndex.value = Math.max(notePopupIndex.value - 1, 0);
      scrollToSelectedNote();
      break;
    case 'Enter':
      event.preventDefault();
      if (notePopupResults.value[notePopupIndex.value]) {
        insertNoteLink(notePopupResults.value[notePopupIndex.value]);
      }
      break;
    case 'Escape':
      hideNotePopup();
      break;
  }
};

const scrollToSelectedNote = () => {
  const listEl = document.querySelector('.note-popup-list');
  const selectedEl = listEl?.children[notePopupIndex.value] as HTMLElement;
  if (selectedEl) {
    selectedEl.scrollIntoView({ block: 'nearest' });
  }
};

// Store note link mappings
const noteLinkMappings = ref<Record<string, number>>({});

// Parse markdown to HTML with internal link handling
const parseMarkdown = (markdownText: string): string => {
  // Find all [[title]] patterns and store mappings
  const regex = /\[\[([^\]]+)\]\]/g;
  let match;
  while ((match = regex.exec(markdownText)) !== null) {
    const title = match[1];
    // Check if we have this note in the search results
    const note = notePopupResults.value.find(n => n.title === title);
    if (note) {
      noteLinkMappings.value[title] = note.id;
    }
  }

  // Process [[title]] to a format that marked can render
  let processedText = markdownText.replace(
    /\[\[([^\]]+)\]\]/g,
    (match, title) => {
      const id = noteLinkMappings.value[title];
      if (id) {
        return `[${title}](/notes/${id})`;
      }
      // Keep as plain text if no ID found
      return title;
    }
  );

  return marked(processedText, {
    breaks: true,
    gfm: true,
  }) as string;
};

// Update preview content
const updatePreview = () => {
  if (editorView.value) {
    const doc = editorView.value.state.doc.toString();
    previewContent.value = parseMarkdown(doc);
  }
};

// Create editor
const createEditor = () => {
  if (!editorContainer.value) return;

  const doc = props.modelValue || '';

  const updateListener = EditorView.updateListener.of((update) => {
    if (update.docChanged) {
      const newValue = update.state.doc.toString();
      emit('update:modelValue', newValue);

      const selection = update.state.selection.main;
      const cursorPos = selection.from;
      const doc = update.state.doc;

      // Get text before cursor using sliceString
      const textBeforeCursor = doc.sliceString(Math.max(0, cursorPos - 30), cursorPos);

      // Check if cursor is inside [[...]] pattern
      const lastOpen = textBeforeCursor.lastIndexOf('[[');

      let query = '';
      let isInside = false;

      if (lastOpen !== -1) {
        // Found [[, extract the content between [[ and cursor
        query = textBeforeCursor.slice(lastOpen + 2);

        // Check if there's a ]] between the last [[ and cursor
        const contentBetween = textBeforeCursor.slice(lastOpen + 2);
        const hasClosing = contentBetween.includes(']]');

        if (!hasClosing) {
          // No ]] between [[ and cursor, we're inside the pattern
          isInside = true;
        }
      }

      if (isInside) {
        const coords = update.view?.coordsAtPos(cursorPos);
        const containerRect = update.view?.dom.getBoundingClientRect();

        if (coords && containerRect) {
          showNoteMentionPopup(query, {
            top: coords.bottom - containerRect.top,
            left: coords.left - containerRect.left,
          });
        }
      } else if (!update.view?.dom.closest('.note-popup')) {
        // Hide popup if not in [[ ]]
        if (showNotePopup.value && !notePopupQuery.value) {
          hideNotePopup();
        }
      }
    }
  });

  const state = EditorState.create({
    doc,
    extensions: [
      basicSetup,
      markdown(),
      keymap.of([...defaultKeymap, ...historyKeymap]),
      history(),
      updateListener,
      EditorView.lineWrapping,
      EditorView.theme({
        '&': {
          height: '100%',
          fontSize: '15px',
          backgroundColor: '#ffffff',
        },
        '.cm-scroller': {
          overflow: 'auto',
          fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
        },
        '.cm-content': {
          padding: '16px',
          backgroundColor: '#ffffff',
        },
        '.cm-placeholder': {
          color: '#9ca3af',
        },
        '.cm-gutters': {
          backgroundColor: '#f8fafc',
          color: '#9ca3af',
          borderRight: '1px solid #e5e7eb',
        },
      }),
    ],
  });

  editorView.value = new EditorView({
    state,
    parent: editorContainer.value,
  });

  updatePreview();
};

// Handle preview link clicks
const handlePreviewClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (target.tagName === 'A' && target.classList.contains('internal-link')) {
    event.preventDefault();
    const href = target.getAttribute('href');
    if (href) {
      router.push(href);
    }
  }
};

// Toggle preview mode
const togglePreview = () => {
  previewMode.value = !previewMode.value;
  if (previewMode.value) {
    updatePreview();
  }
};

// Handle keyboard shortcut for preview (Ctrl/Cmd + P)
const handleKeydown = (event: KeyboardEvent) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
    event.preventDefault();
    togglePreview();
  }
};

onMounted(() => {
  createEditor();
  window.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  editorView.value?.destroy();
  window.removeEventListener('keydown', handleKeydown);
});

// Watch for external content changes
watch(
  () => props.modelValue,
  (newValue) => {
    if (editorView.value) {
      const currentValue = editorView.value.state.doc.toString();
      if (newValue !== currentValue) {
        editorView.value.dispatch({
          changes: {
            from: 0,
            to: currentValue.length,
            insert: newValue,
          },
        });
      }
    }
  }
);

defineExpose({ editor: editorView });
</script>

<template>
  <div class="markdown-editor" :class="{ 'preview-mode': previewMode }">
    <!-- Note mention popup -->
    <Teleport to="body">
      <Transition name="popup">
        <div
          v-if="showNotePopup"
          class="note-popup"
          :style="{ top: `${notePopupPosition.top}px`, left: `${notePopupPosition.left}px` }"
        >
          <div class="note-popup-header">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input
              ref="notePopupInputRef"
              v-model="notePopupQuery"
              type="text"
              placeholder="搜索笔记..."
              class="note-popup-input"
              @input="handleNotePopupInput"
              @keydown="handleNotePopupKeydown"
            />
          </div>
          <div class="note-popup-list">
            <div
              v-for="(note, index) in notePopupResults"
              :key="note.id"
              class="note-popup-item"
              :class="{ selected: index === notePopupIndex }"
              @click="insertNoteLink(note)"
              @mouseenter="notePopupIndex = index"
            >
              <div class="note-popup-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
                </svg>
              </div>
              <span class="note-popup-title">{{ note.title }}</span>
            </div>
            <div v-if="notePopupLoading" class="note-popup-loading">
              <div class="loading-spinner"></div>
              <span>搜索中...</span>
            </div>
            <div v-else-if="notePopupResults.length === 0 && notePopupQuery" class="note-popup-empty">
              未找到笔记
            </div>
          </div>
          <div class="note-popup-footer">
            <span>按 Enter 选中，ESC 取消</span>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Toolbar -->
    <div class="editor-toolbar">
      <div class="toolbar-left">
        <button
          class="toolbar-btn"
          :class="{ active: !previewMode }"
          @click="previewMode = false"
          title="编辑模式"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          <span>编辑</span>
        </button>
        <button
          class="toolbar-btn"
          :class="{ active: previewMode }"
          @click="togglePreview"
          title="预览模式 (Ctrl+P)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
          <span>预览</span>
        </button>
      </div>
      <div class="toolbar-right">
        <span class="markdown-hint">支持 Markdown 语法</span>
      </div>
    </div>

    <!-- Editor / Preview -->
    <div class="editor-body">
      <div v-show="!previewMode" ref="editorContainer" class="editor-container"></div>
      <div v-show="previewMode" class="preview-container" @click="handlePreviewClick">
        <div class="preview-content" v-html="previewContent"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.markdown-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f8fafc;
  border-radius: 16px;
  overflow: hidden;
}

/* Toolbar */
.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.toolbar-left {
  display: flex;
  gap: 6px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f8fafc;
  border: none;
  border-radius: 8px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #f1f5f9;
  color: #1f2937;
}

.toolbar-btn.active {
  background: #8b5cf6;
  color: white;
}

.toolbar-btn svg {
  width: 16px;
  height: 16px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.markdown-hint {
  font-size: 12px;
  color: #9ca3af;
}

/* Editor body */
.editor-body {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.editor-container {
  height: 100%;
  width: 100%;
  overflow: auto;
  background: white;
  position: absolute;
  top: 0;
  left: 0;
}

.preview-container {
  height: 100%;
  width: 100%;
  overflow: auto;
  padding: 32px;
  background: white;
}

.preview-content {
  max-width: 800px;
  margin: 0 auto;
  color: #374151;
  line-height: 1.8;
}

/* Markdown preview styles */
.preview-content :deep(h1) {
  font-size: 1.75em;
  font-weight: 700;
  margin: 1.5em 0 0.75em;
  color: #1f2937;
}

.preview-content :deep(h2) {
  font-size: 1.5em;
  font-weight: 600;
  margin: 1.25em 0 0.5em;
  color: #1f2937;
}

.preview-content :deep(h3) {
  font-size: 1.25em;
  font-weight: 600;
  margin: 1em 0 0.5em;
  color: #1f2937;
}

.preview-content :deep(p) {
  margin: 0.75em 0;
}

.preview-content :deep(a) {
  color: #8b5cf6;
  text-decoration: none;
}

.preview-content :deep(a:hover) {
  text-decoration: underline;
}

.preview-content :deep(code) {
  background: #f3f4f6;
  padding: 0.2em 0.45em;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875em;
  color: #dc2626;
}

.preview-content :deep(pre) {
  background: #1f2937;
  padding: 20px;
  border-radius: 12px;
  overflow-x: auto;
  margin: 1.25em 0;
}

.preview-content :deep(pre code) {
  background: transparent;
  padding: 0;
  color: #e5e7eb;
  font-size: 0.875em;
  line-height: 1.6;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  padding-left: 1.75em;
  margin: 0.75em 0;
}

.preview-content :deep(li) {
  margin: 0.4em 0;
}

.preview-content :deep(blockquote) {
  border-left: 4px solid #8b5cf6;
  padding: 12px 20px;
  margin: 1em 0;
  background: #faf5ff;
  color: #6b7280;
  border-radius: 0 8px 8px 0;
}

.preview-content :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 2em 0;
}

.preview-content :deep(strong) {
  font-weight: 600;
  color: #1f2937;
}

.preview-content :deep(em) {
  font-style: italic;
}

.preview-content :deep(del),
.preview-content :deep(s) {
  text-decoration: line-through;
  color: #9ca3af;
}

.preview-content :deep(img) {
  max-width: 100%;
  border-radius: 12px;
  margin: 1em 0;
}

.preview-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  border-radius: 8px;
  overflow: hidden;
}

.preview-content :deep(th),
.preview-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 12px 16px;
  text-align: left;
}

.preview-content :deep(th) {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
}

.preview-content :deep(tr:nth-child(even)) {
  background: #f9fafb;
}

/* Scrollbar */
.editor-container::-webkit-scrollbar,
.preview-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.editor-container::-webkit-scrollbar-track,
.preview-container::-webkit-scrollbar-track {
  background: transparent;
}

.editor-container::-webkit-scrollbar-thumb,
.preview-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.editor-container::-webkit-scrollbar-thumb:hover,
.preview-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Note popup */
.note-popup {
  position: absolute;
  width: 300px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
  z-index: 9999;
  overflow: hidden;
}

.note-popup-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
}

.note-popup-header .search-icon {
  width: 18px;
  height: 18px;
  color: #9ca3af;
  flex-shrink: 0;
}

.note-popup-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1f2937;
}

.note-popup-input::placeholder {
  color: #9ca3af;
}

.note-popup-list {
  max-height: 250px;
  overflow-y: auto;
}

.note-popup-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s;
}

.note-popup-item:hover,
.note-popup-item.selected {
  background: #f8fafc;
}

.note-popup-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.note-popup-icon svg {
  width: 16px;
  height: 16px;
  color: white;
}

.note-popup-title {
  font-size: 14px;
  color: #374151;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-popup-loading,
.note-popup-empty {
  padding: 20px;
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
}

.note-popup-footer {
  padding: 10px 16px;
  border-top: 1px solid #f3f4f6;
  background: #f9fafb;
  font-size: 12px;
  color: #9ca3af;
}

/* Internal link in preview */
.preview-content :deep(.internal-link) {
  color: #8b5cf6;
  text-decoration: none;
  font-weight: 500;
}

.preview-content :deep(.internal-link:hover) {
  text-decoration: underline;
}

/* Popup transition */
.popup-enter-active,
.popup-leave-active {
  transition: opacity 0.15s ease;
}

.popup-enter-from,
.popup-leave-to {
  opacity: 0;
}

/* Loading spinner */
.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
