def test_should_status_index_error(client):
    mail = 'john@simplylift.com'
    data = client.post('/showSummary', data={'email': mail})
    assert data.status_code != 200