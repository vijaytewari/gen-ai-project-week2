import { test, expect } from '@playwright/test';
import path from 'node:path';

test('photographed CMS1450 uploads into the institutional schema', async ({ page }) => {
  test.setTimeout(150000);
  await page.goto('/');
  await page.locator('input[type="file"]').setInputFiles(path.resolve('..', 'sample1450.JPG'));
  await page.getByRole('button', { name: 'Analyzer', exact: true }).click();
  await expect(page.getByText(/fields populated · CMS-1450/)).toBeVisible({ timeout: 120000 });
  await expect(page.locator('[id="value-1"]')).toHaveValue(/COLLEGE/);
  await page.getByRole('button', { name: /Provider & claim/ }).click();
  await page.getByRole('button', { name: 'Patient demographics', exact: true }).click();
  await expect(page.locator('[id="value-8"]')).toHaveValue(/TORRE/);
  await page.locator('[id="value-8"]').focus();
  await expect(page.getByRole('button', { name: 'Source FL 8', exact: true })).toHaveClass(/selected/);
  await page.screenshot({ path: '../.runtime/screenshots/institutional-review.png', fullPage: true });
  await page.getByRole('button', { name: /Patient demographics/ }).click();
  await page.getByRole('button', { name: 'Service lines & charges', exact: true }).click();
  await expect(page.getByRole('textbox', { name: 'Service row 1 Charges dollars', exact: true })).toHaveValue('4800');
  await expect(page.getByRole('textbox', { name: 'Service row 1 Charges cents', exact: true })).toHaveValue('00');
  await expect(page.locator('[id="value-47.total"]')).toHaveValue('15171');
  const cents = page.getByRole('textbox', { name: 'Service row 1 Charges cents', exact: true });
  await cents.fill('');
  await cents.pressSequentially('25');
  await expect(cents).toHaveValue('25');
  await page.screenshot({ path: '../.runtime/screenshots/service-charges.png', fullPage: true });
});
