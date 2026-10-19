# Synthetic claim fixtures

`backend/app/fixture_values.py` defines curated values; `fixtures.py` maps them to locator fields.
`source_pdf.py` renders an original synthetic institutional layout with matching evidence locations.
No real patient, provider, payer, clinical code or identifier is used.

Twelve cases combine four fictional names, distinct identifiers/charges and six visual scenarios:
clean print, italic handwriting-style text, 90-degree rotation, faint values, missing boundaries and continuation pages.
The handwriting-style scenario is deliberately simulated; it is not handwriting recognition.

Run `python -m scripts.export_fixtures` to regenerate case manifests and 60 query judgments.
The reference PDF was retrieved from the public source recorded in `reference_manifest.json`.
That historical reference remains in private `data/reference/`; the application does not redistribute or use it as a billing template.

Each query identifies its claim case, gold field IDs, expected values and development/held-out split.
Cases 0–2 provide 15 development queries; cases 3–11 provide 45 held-out queries.
Judgments are authored from fixture templates and require independent review before stronger accuracy claims.
