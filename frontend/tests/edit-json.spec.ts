import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';
import { openSynthetic } from './synthetic';

test('editing stays available, saves with review and exports persisted JSON', async ({ page }) => {
  await page.goto('/');
  await openSynthetic(page);
  const provider = page.locator('[id="value-1"]');
  await provider.fill('Synthetic reviewed provider');
  await expect(page.getByRole('button', { name: 'Save & mark reviewed' })).toBeEnabled();
  await expect(page.getByRole('button', { name: 'Save fields', exact: true })).toBeEnabled();
  await page.locator('[id="value-2"]').fill('Synthetic updated pay-to address');
  await page.getByRole('button', { name: 'Save & mark reviewed' }).click();
  await expect(page.getByText('Group reviewed', { exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
  await provider.fill('Synthetic JSON provider');
  await expect(page.getByRole('button', { name: 'Save & mark reviewed' })).toBeEnabled();
  await page.getByRole('button', { name: 'Save & view JSON', exact: true }).click();
  const dialog = page.getByRole('dialog', { name: 'Saved claim JSON' });
  await expect(dialog).toBeVisible();
  const snapshot = JSON.parse(await dialog.locator('pre').innerText());
  expect(snapshot.fields.find((f: { id: string }) => f.id === '1').value).toBe('Synthetic JSON provider');
  expect(snapshot.reviewed).not.toContain('identity');
  expect(snapshot.audit.length).toBeGreaterThan(0);
  expect(snapshot.file).toBeUndefined();
  const pending = page.waitForEvent('download');
  await dialog.getByRole('button', { name: 'Download JSON', exact: true }).click();
  const downloaded = await pending;
  expect(downloaded.suggestedFilename()).toMatch(/\.json$/);
  expect(JSON.parse(await readFile((await downloaded.path())!, 'utf8'))).toEqual(snapshot);
  await dialog.getByRole('button', { name: 'Close JSON', exact: true }).click();
  await provider.fill('Synthetic separately saved provider');
  await page.getByRole('button', { name: 'Save fields', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
  await page.reload();
  await page.getByRole('button', { name: 'Claim workspace', exact: true }).click();
  await expect(provider).toHaveValue('Synthetic separately saved provider');
});

test('a save conflict retains edits and does not mark the group reviewed', async ({ page }) => {
  await page.goto('/');
  await openSynthetic(page);
  await page.locator('[id="value-1"]').fill('Synthetic unsaved correction');
  await page.route('**/api/claims/*/fields', route => route.fulfill({
    status: 409, contentType: 'application/json', body: JSON.stringify({ detail: 'Claim changed. Reload before saving.' }),
  }));
  await page.getByRole('button', { name: 'Save & mark reviewed' }).click();
  await expect(page.getByText('Claim changed. Reload before saving.')).toBeVisible();
  await expect(page.locator('[id="value-1"]')).toHaveValue('Synthetic unsaved correction');
  await expect(page.getByRole('button', { name: 'Save & mark reviewed' })).toBeEnabled();
  await expect(page.getByText('Group reviewed', { exact: true })).not.toBeVisible();
  await page.unroute('**/api/claims/*/fields');
  await page.getByRole('button', { name: 'Save fields', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
});
