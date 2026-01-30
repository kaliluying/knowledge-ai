/**
 * Unit tests for Vue components
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import Tag from '@/components/tags/Tag.vue'
import Button from '@/components/common/Button.vue'
import Empty from '@/components/common/Empty.vue'
import NoteSearch from '@/components/notes/NoteSearch.vue'
import NoteCard from '@/components/notes/NoteCard.vue'
import NoteList from '@/components/notes/NoteList.vue'
import type { NoteListItem } from '@/types'

describe('Tag Component', () => {
  it('should render with default props', () => {
    const wrapper = mount(Tag, {
      props: {
        tag: {
          id: 1,
          name: 'Test Tag',
          slug: 'test-tag',
          color: '#6366f1',
          usage_count: 0
        }
      }
    })
    
    expect(wrapper.text()).toContain('Test Tag')
    expect(wrapper.classes()).toContain('tag')
  })

  it('should render with color', () => {
    const wrapper = mount(Tag, {
      props: {
        tag: {
          id: 2,
          name: 'Colored Tag',
          slug: 'colored-tag',
          color: '#ff0000',
          usage_count: 0
        }
      }
    })
    
    expect(wrapper.attributes('style')).toContain('rgb(255, 0, 0)')
  })

  it('should emit close event when closable', async () => {
    const wrapper = mount(Tag, {
      props: {
        tag: {
          id: 3,
          name: 'Closable Tag',
          slug: 'closable-tag',
          color: '#10b981',
          usage_count: 0
        },
        removable: true
      }
    })
    
    await wrapper.find('.remove-btn').trigger('click')
    expect(wrapper.emitted('remove')).toBeTruthy()
  })
})

describe('Button Component', () => {
  it('should render with default variant', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click Me'
      }
    })
    
    expect(wrapper.text()).toContain('Click Me')
    expect(wrapper.classes()).toContain('btn-primary')
  })

  it('should render with different variants', () => {
    const variants = ['primary', 'secondary', 'danger', 'ghost']
    
    variants.forEach(variant => {
      const wrapper = mount(Button, {
        props: {
          variant
        },
        slots: {
          default: 'Button'
        }
      })
      
      expect(wrapper.classes()).toContain(`btn-${variant}`)
    })
  })

  it('should emit click event', async () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click Me'
      }
    })
    
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('should be disabled when loading', () => {
    const wrapper = mount(Button, {
      props: {
        loading: true
      },
      slots: {
        default: 'Loading'
      }
    })
    
    expect(wrapper.attributes('disabled')).toBeDefined()
  })
})

describe('Empty Component', () => {
  it('should render with default message', () => {
    const wrapper = mount(Empty)
    
    expect(wrapper.text()).toContain('暂无数据')
    expect(wrapper.find('.empty-icon').exists()).toBe(true)
  })

  it('should render with custom message', () => {
    const wrapper = mount(Empty, {
      props: {
        title: 'Custom empty message'
      }
    })
    
    expect(wrapper.text()).toContain('Custom empty message')
  })

  it('should show action button when provided', () => {
    const wrapper = mount(Empty, {
      props: {
        title: 'Create something',
        actionLabel: 'Create',
        actionRoute: '/create'
      }
    })
    
    expect(wrapper.find('.empty-action').exists()).toBe(true)
    expect(wrapper.text()).toContain('Create')
  })
})

describe('NoteSearch Component', () => {
  it('should emit update on input', async () => {
    const wrapper = mount(NoteSearch, {
      props: {
        modelValue: ''
      }
    })

    await wrapper.find('input').setValue('hello')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
  })

  it('should toggle archived state', async () => {
    const wrapper = mount(NoteSearch, {
      props: {
        modelValue: '',
        archived: false
      }
    })

    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('update:archived')).toBeTruthy()
    expect(wrapper.emitted('toggleArchived')).toBeTruthy()
  })
})

describe('NoteCard Component', () => {
  const note: NoteListItem = {
    id: 1,
    title: 'Test Note',
    slug: 'test-note',
    cover_image: null,
    plain_text: 'Preview text',
    category_name: 'Category',
    tag_names: ['Tag1'],
    is_pinned: false,
    is_archived: false,
    view_count: 3,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z'
  }

  it('should render note title', () => {
    const wrapper = mount(NoteCard, {
      props: { note }
    })

    expect(wrapper.text()).toContain('Test Note')
  })

  it('should emit action events', async () => {
    const wrapper = mount(NoteCard, {
      props: { note }
    })

    await wrapper.find('.action-btn').trigger('click')
    expect(wrapper.emitted('edit')).toBeTruthy()
  })
})

describe('NoteList Component', () => {
  const notes: NoteListItem[] = [
    {
      id: 1,
      title: 'Note One',
      slug: 'note-one',
      cover_image: null,
      plain_text: 'Text',
      category_name: null,
      tag_names: [],
      is_pinned: false,
      is_archived: false,
      view_count: 0,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z'
    }
  ]

  it('should render note cards', () => {
    const wrapper = mount(NoteList, {
      props: {
        notes,
        searchQuery: ''
      }
    })

    expect(wrapper.findAllComponents(NoteCard).length).toBe(1)
  })

  it('should show empty state', () => {
    const wrapper = mount(NoteList, {
      props: {
        notes: [],
        searchQuery: ''
      }
    })

    expect(wrapper.findComponent(Empty).exists()).toBe(true)
  })
})
