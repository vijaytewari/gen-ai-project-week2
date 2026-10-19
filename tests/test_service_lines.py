def test_add_service_line_preserves_row_identity_and_conflicts(client):
    claim = client.post("/api/samples/0").json()
    endpoint = f"/api/claims/{claim['id']}/service-lines"
    response = client.post(endpoint, json={"revision": 1})
    assert response.status_code == 200
    updated = response.json()
    added = [f for f in updated["fields"] if f["id"] in {f"{loc}.3" for loc in range(42, 49)}]
    assert len(added) == 7
    assert all(f["row"] == "3" and f["evidence"] is None for f in added)
    assert updated["revision"] == 2
    assert client.post(endpoint, json={"revision": 1}).status_code == 409
