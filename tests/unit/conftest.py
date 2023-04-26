import pytest
import server


@pytest.fixture
def app():
    """
    App de test Flask
    """
    app = server.app
    app.config.update({
        "TESTING": True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def mock_competitions(mocker):
    """
    competitions[0] for testing error on booking on past competition
    competition[1] for testing error on negative competition places after booking
    competition[2] for testing error on booking over 12 places by club
    competition[3] for subtracting points
    """

    competitions = [
        {'name': 'Date_is_over', 'numberOfPlaces': '1',
            "date": "2020-03-27 10:00:00"},
        {'name': 'Negative_places_booking',
            'numberOfPlaces': '1', "date": "2024-03-27 10:00:00"},
        {'name': 'More_than_12_places_avalaible',
            'numberOfPlaces': '13', "date": "2024-03-27 10:00:00"},
        {"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"}
    ]
    mocker.patch('server.competitions', competitions)
    return competitions


@pytest.fixture
def mock_clubs(mocker):
    """
    clubs[0] nothing specific - used to valid data
    club[1] for testing error on not enough points to purchase a place
    club[2] for testing error on booking over 12 places by club on same competition
    club[3] for subtracting points
    """
    clubs = [
        {'name': 'Club 1', 'email': 'club1@example.com', "points": "1"},
        {'name': 'Not enough place',
            'email': 'Notenoughplace@example.com', "points": "0"},
        {'name': 'More_than_12_points_avalaible',
            'email': 'More_than_12_points_avalaible@example.com', "points": "13"},
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    ]
    mocker.patch('server.clubs', clubs)
    return clubs
