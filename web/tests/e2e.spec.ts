import { test, expect } from '@playwright/test'

test('login form renders with session hints', async ({ page }) => {
  await page.goto('/login')
  await expect(page.getByRole('textbox', { name: /email/i })).toBeVisible()
  await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible()
  await expect(page.getByText(/Server-managed sessions/i)).toBeVisible()
})

test.describe('navigate core experience', () => {
  test('mail hub and search reflect virtual views', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByText(/Guest access/i)).toBeVisible()
    await expect(page.getByRole('heading', { name: /Folders & threads/i })).toBeVisible()
    await page.getByRole('link', { name: /Search/i }).click()
    await page.fill('input[type="text"]', 'Important server update')
    await page.getByRole('button', { name: /Run server search/i }).click()
    await expect(page.getByText(/Results ready/i)).toBeVisible()
  })

  test('compose page exposes autosave indicator', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('link', { name: /Compose/i }).click()
    await expect(page.getByRole('heading', { name: /Compose/i })).toBeVisible()
    await page.fill('input[placeholder="recipient@provider"]', 'user@hcasc.cz')
    await expect(page.getByText(/Draft pending/i)).toBeVisible()
  })
})
