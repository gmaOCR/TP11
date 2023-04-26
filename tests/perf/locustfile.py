from locust import HttpUser, task

competition = 'Spring Festival'
club = 'Simply Lift'


class ProjectPerfTest(HttpUser):

    @task(12)
    def showSummary(self):
        """Connexion avec un email
        pour obtenir la page welcome.html
        avec la liste des compétitions."""

        email = 'john@simplylift.co'
        self.client.post('/showSummary', data={'email': email})

    @task
    def purchasePlaces(self):
        """Acheter des places pour un évènement.
        Retour sur la page welcome.html après l'achat."""
        self.client.post(
            '/purchasePlaces',
            data={'places': 1, 'competition': competition, 'club': club},
        )

    @task(12)
    def index(self):
        """Teste la page d'accueil publique
        """
        self.client.get('/')

    @task(12)
    def book(self):
        """Teste la vue de booking
        """
        url = f"/book/{competition}/{club}"
        self.client.get(url)

    @task(12)
    def points_display_board(self):
        """Teste le board public
        """
        self.client.get('/displayPlaces')

    @task(12)
    def logout(self):
        """Teste le logout
        """
        self.client.get('/logout')
