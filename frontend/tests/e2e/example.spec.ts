/**
 * Cypress E2E Test Configuration
 * 
 * This file contains example E2E tests for the knowledge management system.
 * Run with: npx cypress open
 */

// Example test structure - actual tests would require Cypress installation

describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('should show login form', () => {
    cy.get('input[name="email"]').should('exist')
    cy.get('input[name="password"]').should('exist')
    cy.get('button[type="submit"]').should('exist')
  })

  it('should show validation errors for empty fields', () => {
    cy.get('button[type="submit"]').click()
    cy.contains('请输入邮箱').should('exist')
    cy.contains('请输入密码').should('exist')
  })

  it('should navigate to register page', () => {
    cy.contains('立即注册').click()
    cy.url().should('include', '/register')
  })
})

describe('Notes Management', () => {
  beforeEach(() => {
    // Login before each test
    cy.login('test@example.com', 'password123')
    cy.visit('/notes')
  })

  it('should display notes list', () => {
    cy.get('.note-list').should('exist')
  })

  it('should create a new note', () => {
    cy.contains('新建笔记').click()
    cy.get('input[name="title"]').type('Test Note Title')
    cy.get('.tiptap').type('This is test content')
    cy.contains('保存').click()
    cy.contains('Test Note Title').should('exist')
  })

  it('should search notes', () => {
    cy.get('input[placeholder="搜索笔记..."]').type('test')
    cy.wait(500)
    cy.get('.note-card').should('exist')
  })
})

describe('Categories Management', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123')
    cy.visit('/categories')
  })

  it('should display category tree', () => {
    cy.get('.category-tree').should('exist')
  })

  it('should create new category', () => {
    cy.contains('新建分类').click()
    cy.get('input[name="name"]').type('Test Category')
    cy.get('input[name="color"]').type('#3498db')
    cy.contains('保存').click()
    cy.contains('Test Category').should('exist')
  })
})

describe('Knowledge Graph', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123')
    cy.visit('/graph')
  })

  it('should display graph canvas', () => {
    cy.get('.graph-canvas').should('exist')
    cy.get('.graph-node').should('exist')
  })

  it('should zoom in and out', () => {
    cy.get('.zoom-in').click()
    cy.get('.graph-canvas').should('have.css', 'transform')
  })
})

describe('Responsive Design', () => {
  it('should work on mobile', () => {
    cy.viewport('iphone-x')
    cy.visit('/notes')
    cy.get('.mobile-menu').should('exist')
    cy.get('.sidebar').should('not.be.visible')
  })

  it('should work on desktop', () => {
    cy.viewport('macbook-15')
    cy.visit('/notes')
    cy.get('.sidebar').should('be.visible')
  })
})
