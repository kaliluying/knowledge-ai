<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  uploadUrl?: string;
  maxSize?: number;
  accept?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  uploadUrl: '/api/attachments/',
  maxSize: 5 * 1024 * 1024, // 5MB
  accept: () => ['image/*'],
});

const emit = defineEmits<{
  uploaded: [url: string, alt?: string];
  error: [message: string];
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const dragover = ref(false);

const handleFileSelect = async (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    await uploadFile(file);
  }
  target.value = '';
};

const handleDrop = async (e: DragEvent) => {
  dragover.value = false;
  const file = e.dataTransfer?.files[0];
  if (file) {
    await uploadFile(file);
  }
};

const handleDragover = (e: DragEvent) => {
  e.preventDefault();
  dragover.value = true;
};

const handleDragleave = () => {
  dragover.value = false;
};

const uploadFile = async (file: File) => {
  // 验证文件类型
  if (!props.accept.some(pattern => {
    if (pattern.endsWith('/*')) {
      return file.type.startsWith(pattern.replace('/*', ''));
    }
    return file.type === pattern;
  })) {
    emit('error', '不支持的文件类型');
    return;
  }

  // 验证文件大小
  if (file.size > props.maxSize) {
    emit('error', `文件大小不能超过 ${Math.round(props.maxSize / 1024 / 1024)}MB`);
    return;
  }

  isUploading.value = true;

  try {
    // 如果有上传 URL，使用上传接口
    if (props.uploadUrl) {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(props.uploadUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        emit('uploaded', data.url, file.name);
      } else {
        emit('error', '上传失败');
      }
    } else {
      // 否则使用 FileReader
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        emit('uploaded', result, file.name);
      };
      reader.readAsDataURL(file);
    }
  } catch (error) {
    emit('error', '上传失败，请重试');
  } finally {
    isUploading.value = false;
  }
};

const openFilePicker = () => {
  fileInput.value?.click();
};

const triggerUpload = () => {
  openFilePicker();
};
</script>

<template>
  <div class="image-uploader">
    <input
      ref="fileInput"
      type="file"
      :accept="accept.join(',')"
      class="file-input"
      @change="handleFileSelect"
    />

    <div
      class="dropzone"
      :class="{ 'dragover': dragover, 'uploading': isUploading }"
      @drop="handleDrop"
      @dragover="handleDragover"
      @dragleave="handleDragleave"
      @click="triggerUpload"
    >
      <template v-if="isUploading">
        <div class="uploading-state">
          <div class="loading-spinner"></div>
          <span>上传中...</span>
        </div>
      </template>
      <template v-else>
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
        <span class="upload-text">点击或拖拽上传图片</span>
        <span class="upload-hint">支持 PNG、JPG、GIF，最大 5MB</span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.image-uploader {
  width: 100%;
}

.file-input {
  display: none;
}

.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px;
  border: 2px dashed #e5e7eb;
  border-radius: 16px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.3s;
}

.dropzone:hover {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}

.dropzone.dragover {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.1);
}

.dropzone.uploading {
  cursor: default;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #9ca3af;
  transition: color 0.3s;
}

.dropzone:hover .upload-icon {
  color: #8b5cf6;
}

.upload-text {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.upload-hint {
  font-size: 12px;
  color: #9ca3af;
}

.uploading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.uploading-state span {
  font-size: 14px;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
