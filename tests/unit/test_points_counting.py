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
    with app.app_context():
        placesRequired = 10
        expected_points = 3
        competitions = mock_competitions
        club = mock_clubs
        client.post('/purchasePlaces', data={
            'competition': competitions[3]['name'],
            'club': club[3]['name'],
            'places': placesRequired
        })
        assert club[3]['points'] == expected_points 