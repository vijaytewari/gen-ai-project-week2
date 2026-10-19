const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('../frontend/node_modules/@playwright/test');

(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    const page = await browser.newPage();
    for (const name of ['ARCHITECTURE', 'PROJECT_SUBMISSION']) {
      const source = path.join(root, '.runtime', 'submission-pdfs', `${name}.html`);
      await page.goto(pathToFileURL(source).href, { waitUntil: 'load' });
      await page.pdf({
        path: path.join(root, 'docs', `${name}.pdf`), format: 'A4', printBackground: true,
        margin: { top: '17mm', bottom: '18mm', left: '17mm', right: '17mm' },
        displayHeaderFooter: true, headerTemplate: '<span></span>',
        footerTemplate: '<div style="font:9px Arial;color:#667b71;width:100%;padding:0 17mm;display:flex;justify-content:space-between"><span>CLAIMS PROCESSOR</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
      });
      console.log(`Created docs/${name}.pdf`);
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
