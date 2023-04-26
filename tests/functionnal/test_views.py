from flask_testing import TestCase
# from blinker import signal
from server import app, loadClubs, loadCompetitions

clubs = loadClubs()
competitions = loadCompetitions()


class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show_summary(self):
        response = self.client.post('/showSummary', data=dict(email=clubs[0]['email']))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('welcome.html')

    def test_book(self):
        response = self.client.get('/book/competition1/club1')
        self.assertEqual(response.status_code, 200)

    def test_purchase_places(self):
        data = dict(competition=competitions[0]['name'], club=clubs[0]['name'], places='5')
        response = self.client.post('/purchasePlaces', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)

    def test_points_display_board(self):
        response = self.client.get('/displayPlaces')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
