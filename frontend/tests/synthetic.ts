import { expect, type Page } from '@playwright/test';

export async function openSynthetic(page: Page, caseId = 0) {
  // Fixtures are test data only; the product library never offers demo documents.
  const created = await page.request.post(`/api/samples/${caseId}`);
  const claim = await created.json();
  const original = await page.request.get(`/api/claims/${claim.id}/original`);
  const filename = `synthetic-review-${caseId}-${Date.now()}.pdf`;
  await page.locator('input[type="file"]').setInputFiles({
    name: filename, mimeType: 'application/pdf', buffer: await original.body(),
  });
  await expect(page.locator('[id="value-1"]')).toBeVisible();
  return filename;
}
