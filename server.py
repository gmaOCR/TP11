import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

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

club_bookings = {}
competition_bookings = {}


@app.route('/')
def index():
    return render_template('index.html',
                           clubs=clubs,
                           competitions=competitions)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    if club is None:
        flash('Club not found')
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        foundClub = foundClub[0]
        foundCompetition = foundCompetition[0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash('Club or competition not found')
        return render_template(
            'welcome.html', club=club, competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                   == request.form['competition']]
    if not competition:
        raise IndexError('Competition not found')
    competition = competition[0]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if not club:
        raise IndexError('Club not found')
    club = club[0]
    placesRequired = int(request.form['places'])
    competition_date = datetime.strptime(
        competition['date'], '%Y-%m-%d %H:%M:%S')

    # Check if the purchase is over the MAX_PLACES set
    if placesRequired > MAX_PLACES:
        flash(f'Cannot book more than {MAX_PLACES} places per competition')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Check if the competition still have enough places avalaible
    elif int(competition['numberOfPlaces']) < placesRequired:
        flash('Not enough places available')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Check if the club have enough points to purchase
    elif int(club['points']) < placesRequired:
        flash('Not enough points available')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Check if the competetion is outdated
    if competition_date < datetime.now():
        flash('Cannot book places for a past competition')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    else:

        # Check if the amount of places purchased by the same club on the same competition is over MAX_PLACES set
        if competition['name'] in competition_bookings and competition_bookings[competition['name']] + placesRequired > 12:
            flash(f'Max {MAX_PLACES} places per competition')
            return render_template('welcome.html', club=club, competitions=competitions), 400
        if competition['name'] in competition_bookings:
            competition_bookings[competition['name']] += placesRequired

        # In all ohter cases -> do the purchase
        else:
            competition_bookings[competition['name']] = placesRequired
        if club['name'] in club_bookings:
            club_bookings[club['name']] += placesRequired
        else:
            club_bookings[club['name']] = placesRequired
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/displayPlaces', methods=['GET'])
def points_display_board():
    return render_template('display_places.html',
                        clubs=clubs,
                        competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
