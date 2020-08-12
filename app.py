#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from models import Artist, Venue, Show

from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://coolguy:meme@localhost:5432/fyyur'

#db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():  
  venues = Venue.query.order_by(Venue.city)

  data=[]
  cities = []
  for venue in venues:
    city = venue.city

    if (city not in cities):
      cities.append(city)
      data.append({
        "city": city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "upcoming_shows_count": venue.upcoming_shows_count
        }]
      })
      print('Added ' + venue.name + ' to ' + city)
    else:
      next(filter(lambda venue_city: venue_city['city'] == city, data))['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "upcoming_shows_count": venue.upcoming_shows_count
      })
      print('Added ' + venue.name + ' to ' + city)  
        
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()

  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count
    })

  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  return render_template('pages/show_venue.html', venue=Venue.query.get(venue_id))

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False

  form = VenueForm()
  try:
    venue = Venue(
      name=form.name.data,
      genres=form.genres.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      facebook_link=form.facebook_link.data,
      address=form.address.data,
      seeking_talent=True,
      seeking_description='',
      upcoming_shows_count=0,
      past_shows_count=0
    )

    venue.insert()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()

  if error:
    abort(400)
    flash('An error occured')
  else: 
    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=[' '])
def delete_venue(venue_id):
  success = True
  try:
    venue = Venue.query.filter_by(id=venue_id)
    venue.delete()
  except:
    success = False
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({'success': success})

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm()
  
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.address.data = venue.address
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    form = VenueForm()

    venue = Venue.query.get(venue_id)
    venue.name=form.name.data,
    venue.genres=form.genres.data,
    venue.city=form.city.data,
    venue.state=form.state.data,
    venue.phone=form.phone.data,
    venue.address=form.address.data,
    #image_link=request.form['image_link'],
    venue.facebook_link=form.facebook_link.data,
    venue.update()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()

  if error:
    abort (400)
    flash('An error occured')
  else:
    # on successful db insert, flash success
    flash('Venue ' + venue.name + ' was successfully edited!')

  return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  
  data = []
  for artist in artists:
    print(artist.name)
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.upcoming_shows_count
    })

  response = {
    "count": len(data),
    "data": data
  }


        
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  
  return render_template('pages/show_artist.html', artist=Artist.query.get(artist_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False

  form = ArtistForm()

  try:
    artist = Artist(
      name=form.name.data,
      genres=form.genres.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      #image_link=request.form['image_link'],
      facebook_link=form.facebook_link.data,
      upcoming_shows_count=0,
      past_shows_count=0
    )
    artist.insert()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()
  #finally:
    #db.session.close()
  
  if error:
    abort (400)
    flash('An error occured')
  else:
    # on successful db insert, flash success
    flash('Artist ' + artist.name + ' was successfully listed!')
  
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm()

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes
  error = False
  

  try:
    artist = Artist.query.get(artist_id)
    form = ArtistForm()

    artist.name=form.name.data,
    artist.genres=form.genres.data,
    artist.city=form.name.data,
    artist.state=form.name.data,
    artist.phone=form.name.data,
    #image_link=request.form['image_link'],
    artist.facebook_link=form.name.data,
    artist.update()
  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()

  if error:
    abort (400)
    flash('An error occured')
  else:
    # on successful db insert, flash success
    flash('Artist ' + artist.name + ' was successfully edited!')

  return redirect(url_for('show_artist', artist_id=artist_id))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows

  shows = Show.query.all()

  data=[]
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form

  error = False
  try:
    form = ShowForm()
    show = Show(
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      start_time=form.start_time.data
    )
    show.insert()

    #venue =  Venue.query.get(show.venue_id)
    #venue.upcoming_shows_count += 1
    #venue.update()

    #artist = Artist.query.get(show.artist_id)
    #artist.upcoming_shows_count += 1
    #artist.update()

  except:
    error = True
    print(sys.exc_info())
    db.session.rollback()

  if error:
    abort (400)
    flash('An error occured')
  else:
    flash('Show was successfully listed')
  # on successful db insert, flash success
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
