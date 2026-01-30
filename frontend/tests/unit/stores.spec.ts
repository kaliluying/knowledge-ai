/**
 * Unit tests for Pinia stores
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useNotesStore } from '@/stores/notes'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with null user', () => {
    const authStore = useAuthStore()
    expect(authStore.user).toBeNull()
    expect(authStore.isAuthenticated).toBe(false)
  })

  it('should set user on login', async () => {
    const authStore = useAuthStore()
    
    // Mock login
    authStore.user = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
      avatar: null,
      bio: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    expect(authStore.user).not.toBeNull()
    expect(authStore.user?.username).toBe('testuser')
    expect(authStore.isAuthenticated).toBe(true)
  })

  it('should clear user on logout', async () => {
    const authStore = useAuthStore()
    
    authStore.user = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
      avatar: null,
      bio: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    authStore.logout()
    
    expect(authStore.user).toBeNull()
    expect(authStore.isAuthenticated).toBe(false)
  })
})

describe('Notes Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with empty notes list', () => {
    const notesStore = useNotesStore()
    expect(notesStore.notes).toEqual([])
    expect(notesStore.currentNote).toBeNull()
  })

  it('should set current note', () => {
    const notesStore = useNotesStore()
    
    const mockNote = {
      id: '1',
      title: 'Test Note',
      slug: 'test-note',
      content: [],
      plain_text: '',
      cover_image: null,
      category: null,
      tags: [],
      is_pinned: false,
      is_archived: false,
      view_count: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    notesStore.setCurrentNote(mockNote)
    
    expect(notesStore.currentNote).not.toBeNull()
    expect(notesStore.currentNote?.title).toBe('Test Note')
  })

  it('should add note to list', () => {
    const notesStore = useNotesStore()
    
    const mockNote = {
      id: '1',
      title: 'New Note',
      slug: 'new-note',
      content: [],
      plain_text: '',
      cover_image: null,
      category: null,
      tags: [],
      is_pinned: false,
      is_archived: false,
      view_count: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    notesStore.notes.push(mockNote)
    
    expect(notesStore.notes.length).toBe(1)
    expect(notesStore.notes[0].title).toBe('New Note')
  })
})
