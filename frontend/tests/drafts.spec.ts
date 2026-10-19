import { test, expect } from '@playwright/test';
import path from 'node:path';

test('upload waits for Analyzer and enters the library only after Save JSON', async ({ page }) => {
  await page.goto('/');
  const before = (await (await page.request.get('/api/library')).json()).records.length;
  await page.locator('input[type="file"]').setInputFiles(path.resolve('..', 'sample1450.JPG'));
  await expect(page.getByRole('button', { name: 'Analyzer', exact: true })).toBeEnabled();
  await expect(page.getByText('This upload has not been read with OCR')).toBeVisible();
  await expect(page.locator('[id="value-1"]')).toHaveValue('');
  const draft = await page.evaluate(() => localStorage.getItem('claimlens:last'));
  const preview = await page.request.get(`/api/claims/${draft}/export`);
  expect((await preview.json()).form_data['8']).toBe('');
  await page.getByRole('button', { name: 'Document library', exact: true }).click();
  await expect(page.locator('.saved-record')).toHaveCount(before);
  await page.getByRole('button', { name: 'Claim workspace', exact: true }).click();
  await page.getByRole('button', { name: 'Save JSON', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Document library', exact: true }).click();
  await expect(page.locator('.saved-record')).toHaveCount(before + 1);
});
