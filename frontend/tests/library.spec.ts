import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';
import { openSynthetic } from './synthetic';

test('JSON library stores complete forms and revisions without demo documents', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle('Claims Processor');
  await expect(page.getByRole('link', { name: 'Claims Processor' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Review by HITL' })).toBeVisible();
  const filename = await openSynthetic(page);
  const provider = page.locator('[id="value-1"]');
  for (const value of ['Synthetic library first edit', 'Synthetic library second edit']) {
    await provider.fill(value);
    await page.getByRole('button', { name: 'Save fields', exact: true }).click();
    await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
  }
  await page.getByRole('button', { name: 'Document library', exact: true }).click();
  await page.getByRole('textbox', { name: 'Find a saved claim' }).fill(filename);
  const card = page.locator('.saved-record').filter({ hasText: filename });
  await expect(card).toBeVisible();
  await expect(card).toContainText('Revision 3');
  await expect(card).toContainText('2 field edits');
  await expect(page.getByText('Curated demo', { exact: true })).not.toBeVisible();
  await card.getByRole('button', { name: 'View JSON', exact: true }).click();
  const dialog = page.getByRole('dialog', { name: 'Saved claim JSON' });
  const json = JSON.parse(await dialog.locator('pre').innerText());
  expect(new Set(json.fields.map((f: { locator: number }) => f.locator)).size).toBe(81);
  expect(json.revisions).toHaveLength(3);
  expect(json.audit[1].event.changes[0].old).toBe('Synthetic library first edit');
  await dialog.getByRole('button', { name: 'Close JSON' }).click();
  const pending = page.waitForEvent('download');
  await card.getByRole('button', { name: 'Download JSON', exact: true }).click();
  const downloaded = await pending;
  const exported = JSON.parse(await readFile((await downloaded.path())!, 'utf8'));
  expect(exported).toEqual(json);
  await card.getByRole('button', { name: `Open ${filename}` }).click();
  await expect(provider).toHaveValue('Synthetic library second edit');
});
