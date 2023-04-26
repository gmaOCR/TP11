def test_should_status_code_ok(client):
    "test mail login ok"
    mail = 'john@simplylift.co'
    data = client.post('/showSummary', data={'email': mail})
    assert data.status_code == 200

def test_should_status_code_302(client):
    "test mail login ko"
    mail = 'john@simplylift.com'
    data = client.post('/showSummary', data={'email': mail})
    assert data.status_code == 302
    