import { test, expect } from '@playwright/test';
import path from 'node:path';

test('uploaded image runs OCR and refreshes into editable professional fields', async ({ page }) => {
  test.setTimeout(150000);
  await page.goto('/');
  const file = path.resolve('..', 'cms1450Form_Sample.JPG');
  await page.locator('input[type="file"]').setInputFiles(file);
  await expect(page.getByText('This upload has not been read with OCR')).toBeVisible();
  await expect(page.locator('[id="value-1"]')).toHaveValue('');
  await page.getByRole('button', { name: 'Analyzer', exact: true }).click();
  await expect(page.getByText('Reading document and mapping fields…')).toBeVisible();
  await expect(page.getByText(/fields populated · CMS-1500/)).toBeVisible({ timeout: 120000 });
  await expect(page.locator('[id="value-1500.1a"]')).not.toHaveValue('');
  await page.getByRole('button', { name: 'Insured & coverage' }).click();
  await page.getByRole('button', { name: 'Patient demographics', exact: true }).click();
  const patient = page.locator('[id="value-1500.2"]');
  await expect(patient).toHaveValue(/Jane/);
  await patient.fill('Doe, Jane — verified');
  await page.getByRole('button', { name: 'Save changes' }).click();
  await expect(page.getByRole('button', { name: 'Saved', exact: true })).toBeVisible();
  await page.screenshot({ path: '../.runtime/screenshots/ocr-review.png', fullPage: true });
});
