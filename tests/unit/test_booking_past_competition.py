from server import app

def test_should_not_allow_booking_for_past_competition(client, mock_competitions, mock_clubs):
    "Test l'impossibilité de reserver une competition passée + message"
    with app.app_context():
        competition = mock_competitions
        club = mock_clubs
        places_required = 1
        response = client.post('/purchasePlaces', data={
            'competition': competition[0]['name'],
            'club': club[0]['name'],
            'places': places_required
        })
        assert response.status_code == 400
        assert b'Cannot book places for a past competition' in response.data