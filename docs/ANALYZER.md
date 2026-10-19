# Analyzer, schema and saved JSON

Upload opens the source and a draft field editor. It does not run OCR, create a JSON file, or add a library record.
Press **Analyzer** at the top to run local OCR and generate a schema for the detected form.
Press **Save JSON**, **Save fields**, or save edited fields to publish one JSON record per claim.
Saving again updates that record; its JSON contains all fields, original values, revisions and audit events.
Library viewing/downloading reads the last published JSON, not a later unsaved analysis draft.

## GPT setup

Set `OPENAI_API_KEY` in the backend `.env` or Replit Secrets and restart the backend.
`OPENAI_SCHEMA_MODEL=gpt-4.1-mini` selects the default configurable model.
The Responses API uses [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
Only the known field IDs, labels and detected form type are sent; images, OCR text and claim values stay local.
Model responses must include every field exactly once. Unknown/duplicate/missing IDs are rejected.
Money constraints remain enforced even if GPT suggests an overly permissive field definition.

The app compiles GPT definitions into a JSON Schema for `form_data` and validates values locally using jsonschema.
Exports include `form_schema`, `form_data`, `schema_generation` and `schema_validation`.
Invalid OCR values remain editable and appear as review issues; saving never fabricates replacement values.
These checks validate structure/formats, not medical necessity, eligibility or payer policy.

Without a key, or if GPT fails/refuses/omits fields, Analyzer keeps the OCR and uses a visibly labeled local schema.
GPT schema generation is tested with mocked API responses; a live call requires configured credentials.

## Storage and tests

SQLite stores drafts, saved snapshots and complete audit/revision history. `data/json/<claim-id>.json` mirrors a published save.
Analyzer and uploads do not publish. Subsequent edits update the same library card when saved.
Browser tests use a separate port and data directory so synthetic test records cannot enter the user's library.
`python scripts/clear_library.py` explicitly clears claim/library rows and generated JSON files; run with the server stopped.
Original uploaded source files are retained by that command.
