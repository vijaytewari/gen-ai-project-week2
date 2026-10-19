"""Only explicit field/JSON saves publish a record in the library."""
import json
import os
import tempfile
import logging
import threading
from fastapi import HTTPException
from . import database as db
from .config import DATA

PUBLISH_LOCK = threading.Lock()


def visible(claim):
    origin = claim.get('origin', 'demo' if claim.get('sample') is not None else 'upload')
    return origin != 'demo' and claim.get('saved_json', False)


def clean(claim):
    return {key: value for key, value in claim.items() if key != 'file'}


def snapshot(claim):
    from .form_schema import attach_data
    claim = dict(claim)
    attach_data(claim)
    with db.connection() as connection:
        history = connection.execute(
            'SELECT body FROM history WHERE id=? AND revision<=? ORDER BY revision',
            (claim['id'], claim['revision'])).fetchall()
        audit = connection.execute('SELECT timestamp,body FROM audit WHERE claim_id=? ORDER BY id',
                                   (claim['id'],)).fetchall()
    return {**clean(claim), 'schema_version': '2.0', 'audit': [
        {**dict(row), 'event': json.loads(row['body'])} for index, row in enumerate(audit, 2)
        if json.loads(row['body']).get('revision', index) <= claim['revision']],
        'revisions': [clean(json.loads(row['body'])) for row in history]}


def _publish(claim):
    if not visible(claim):
        return
    payload = snapshot(claim)
    with db.connection() as connection:
        changed = connection.execute('INSERT INTO saved_json VALUES(?,?,?) ON CONFLICT(id) DO UPDATE '
                           'SET revision=excluded.revision,body=excluded.body '
                           'WHERE excluded.revision>=saved_json.revision',
                           (claim['id'], claim['revision'], json.dumps(payload))).rowcount
    if not changed:
        return
    directory = DATA / 'json'
    directory.mkdir(exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=directory, suffix='.tmp')
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as output:
            json.dump(payload, output, ensure_ascii=False, indent=2)
        os.replace(temporary, directory / f"{claim['id']}.json")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def publish(claim):
    with PUBLISH_LOCK:
        try:
            _publish(claim)
        except OSError:
            logging.exception('JSON file mirror failed; the saved JSON remains available in SQLite')


def saved_snapshot(claim_id):
    with db.connection() as connection:
        row = connection.execute('SELECT body FROM saved_json WHERE id=?', (claim_id,)).fetchone()
    if not row:
        raise HTTPException(404, 'This claim has not been saved as JSON')
    return json.loads(row[0])


def records():
    with db.connection() as connection:
        rows = connection.execute('SELECT body FROM saved_json ORDER BY rowid DESC').fetchall()
    result = []
    for row in rows:
        claim = json.loads(row[0])
        result.append({'id': claim['id'], 'filename': claim['filename'],
                       'revision': claim['revision'], 'form_type': claim['form_type'],
                       'field_count': len(claim['fields']), 'status': 'saved',
                       'edit_count': sum(len(e['event'].get('changes', [])) for e in claim['audit'])})
    return result
