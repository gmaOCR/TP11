import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for, make_response

MAX_PLACES = 12

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    if club is None:
        flash('Club not found')
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

club_bookings = {}  
competition_bookings = {}

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') 
    if placesRequired > MAX_PLACES:
        flash(f'Cannot book more than {MAX_PLACES} places per competition')
        return render_template('welcome.html', club=club, competitions=competitions)
    elif int(competition['numberOfPlaces']) < placesRequired:
        return 'Not enough places available', 400 
    elif int(club['points']) < placesRequired:
        return 'Not enough points available', 400 
    if competition_date < datetime.now():
        return 'Cannot book places for a past competition', 400 
    else:
        if competition['name'] in competition_bookings and competition_bookings[competition['name']] + placesRequired > 12:
            return f'Max {MAX_PLACES} places per competition', 400
        if club['name'] in club_bookings and club_bookings[club['name']] + placesRequired > 12:
            return f'IMax {MAX_PLACES} places per competition and per club', 400
        if competition['name'] in competition_bookings:
            competition_bookings[competition['name']] += placesRequired
        else:
            competition_bookings[competition['name']] = placesRequired
        if club['name'] in club_bookings:
            club_bookings[club['name']] += placesRequired
        else:
            club_bookings[club['name']] = placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/displayPlaces')
def displayPlaces():
    # Créer un dictionnaire pour stocker le nombre de places réservées par club et par compétition
    places_by_club_and_competition = {}
    for club in clubs:
        for competition in competitions:
            if club['name'] not in places_by_club_and_competition:
                places_by_club_and_competition[club['name']] = {}
            places_by_club_and_competition[club['name']][competition['name']] = 0
    for club in clubs:
        for booking_club, places in club_bookings.items():
            if club['name'] == booking_club:
                for competition in competitions:
                    if competition['name'] in competition_bookings:
                        places_by_club_and_competition[club['name']][competition['name']] = competition_bookings[competition['name']]
                        if booking_club in places_by_club_and_competition:
                            places_by_club_and_competition[booking_club][competition['name']] += places
                        else:
                            places_by_club_and_competition[booking_club][competition['name']] = places
    return render_template('display_places.html', clubs=clubs, competitions=competitions, places_by_club_and_competition=places_by_club_and_competition)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))