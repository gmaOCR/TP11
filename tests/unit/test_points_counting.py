from server import app
    
def test_should_not_allow_insufficient_points(client, mock_competitions, mock_clubs):
    ""
    competitions = mock_competitions
    clubs = mock_clubs
    with app.app_context():
        places_required = 1
        response = client.post('/purchasePlaces', data={
            'competition': competitions[1]['name'],
            'club': clubs[1]['name'],
            'places': places_required
        })
        assert response.status_code == 400
        assert b'Not enough points available' in response.data
        
        
def test_subtract_positive_value(client, mock_clubs, mock_competitions):
    """Test la soustraction de point d'un club"""
    placesRequired = 5
    expected_points = 8
    client.post('/purchasePlaces', data={
        'competition': mock_competitions[3]['name'],
        'club': mock_clubs[3]['name'],
        'places': placesRequired
    })
    assert int(mock_clubs[3]['points']) == expected_points