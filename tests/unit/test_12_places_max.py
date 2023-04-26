from server import app
from server import MAX_PLACES


def test_should_not_allow_more_than_12_places_per_competition(client, mock_competitions, mock_clubs):
    "Test l'impossibilité de réserver 12 places max par compétition + message"
    competitions = mock_competitions
    clubs = mock_clubs
    with app.app_context():
        places_required = 16
        response = client.post('/purchasePlaces', data={
            'competition': competitions[2]['name'],
            'club': clubs[2]['name'],
            'places': places_required
        })
        assert response.status_code == 400
        assert f'Cannot book more than {MAX_PLACES} places per competition'.encode(
        ) in response.data
