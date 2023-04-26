from server import app


def test_should_not_allow_negative_numberOfPlaces(client, mock_competitions, mock_clubs):
    "Test l'impossibilité de reserver une competition sans places disponibles + message"
    competitions = mock_competitions
    clubs = mock_clubs
    with app.app_context():
        places_required = 2
        response = client.post('/purchasePlaces', data={
            'competition': competitions[1]['name'],
            'club': clubs[0]['name'],
            'places': places_required
        })
        assert response.status_code == 400
        assert b'Not enough places available' in response.data
