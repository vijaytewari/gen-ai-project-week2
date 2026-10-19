# Project conventions

- Keep every authored code, test and documentation file below 100 lines.
- Split by responsibility; do not compress code into unreadable lines to meet the limit.
- Run `python scripts/check_lines.py` before delivery.
- Generated dependency locks, vendor files, minified builds and binary assets are exceptions.
- Use synthetic claim data only in demos and tests.
- Preserve source evidence, original values and revision conflicts when changing claim workflows.
- Keep Pinecone/model secrets on the server; distinguish connected, local and simulated modes.
- Do not present fixture extraction as OCR or template-derived benchmark labels as independently reviewed.
