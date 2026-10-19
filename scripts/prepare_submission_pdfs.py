"""Prepare print HTML from the two submission Markdown documents."""
from pathlib import Path
from submission_markup import render

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.runtime' / 'submission-pdfs'
OUTPUT.mkdir(parents=True, exist_ok=True)
CSS = """
@page { size: A4; }
* { box-sizing: border-box; }
body { font-family: Arial, sans-serif; color: #263b34; font-size: 10.5pt; line-height: 1.48; margin: 0; }
h1 { color: #153d33; font-size: 23pt; line-height: 1.2; margin: 0 0 15px; padding-bottom: 13px; border-bottom: 3px solid #4f9079; }
h2 { color: #205844; font-size: 13pt; margin: 19px 0 7px; break-after: avoid; }
p { margin: 0 0 9px; }
.item { margin-bottom: 7px; padding-left: 12px; text-indent: -12px; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #eef3ef; padding: 1px 3px; overflow-wrap: anywhere; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 8px 0 15px; }
th { background: #e8f1eb; text-align: left; color: #153d33; }
th, td { padding: 7px 9px; border: 1px solid #d5e2d9; vertical-align: top; }
td:first-child { width: 30%; font-weight: 600; }
tr { break-inside: avoid; }
.diagram { margin: 10px 0 16px; break-inside: avoid; }
svg { width: 100%; display: block; }
.architecture h2:nth-of-type(3) { break-before: page; }
.submission { font-size: 10pt; line-height: 1.43; }
.submission h1 { font-size: 22pt; }
.submission h2 { margin-top: 16px; font-size: 12pt; }
"""

for name in ('ARCHITECTURE', 'PROJECT_SUBMISSION'):
    source = ROOT / 'docs' / f'{name}.md'
    kind = 'architecture' if name == 'ARCHITECTURE' else 'submission'
    markup = render(source.read_text(encoding='utf-8-sig'))
    page = f'<!doctype html><html><head><meta charset="utf-8"><title>Claims Processor</title><style>{CSS}</style></head>'
    page += f'<body class="{kind}">{markup}</body></html>'
    (OUTPUT / f'{name}.html').write_text(page, encoding='utf-8')
    print(f'Prepared {name}.html')
