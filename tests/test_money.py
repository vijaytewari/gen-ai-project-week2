import pytest
from backend.app.extraction.money import normalize_money


def amount(value, key="47.1", source="ocr"):
    return {"id": key, "locator": int(key.split(".")[0]), "value": value,
            "original": value, "source": source}


@pytest.mark.parametrize("raw,expected", [
    ("480000", "4800.00"), ("1517150", "15171.50"), ("5", "0.05"),
    ("0", "0.00"), ("1 234 56", "1234.56"), ("$4,800.50", "4800.50"),
    ("123.4", "123.40"), ("unreadable", "unreadable"), ("", ""),
])
def test_currency_normalization_preserves_raw_and_is_idempotent(raw, expected):
    field = amount(raw)
    normalize_money([field])
    assert field["value"] == expected
    assert field["original"] == raw
    assert normalize_money([field]) == []


def test_currency_does_not_change_codes_units_or_reviewer_corrections():
    fields = [amount("480000", "42.1"), amount("12", "46.1"),
              amount("4800", source="reviewer")]
    assert normalize_money(fields) == []
    assert [f["value"] for f in fields] == ["480000", "12", "4800"]


def test_existing_claim_migration_is_audited_and_preserves_manual_edits(client):
    from backend.app import database as db
    from backend.app.extraction.money_migration import migrate_money
    field = amount("1517150", "47.total")
    field["group"] = "services"
    manual = amount("4800.00", "47.1", source="reviewer")
    manual["group"] = "services"
    claim = {"id": "money-migration-test", "revision": 1, "fields": [field, manual],
             "reviewed": ["services"], "acknowledgments": {"services": "checked"},
             "index_revision": 1}
    db.insert(claim)
    migrate_money()
    updated = db.load(claim["id"])
    assert updated["revision"] == 2 and updated["index_revision"] is None
    assert updated["fields"][0]["value"] == "15171.50"
    assert updated["fields"][0]["original"] == "1517150"
    assert updated["fields"][1]["value"] == "4800.00"
    assert not updated["reviewed"] and not updated["acknowledgments"]
    migrate_money()
    assert db.load(claim["id"])["revision"] == 2
