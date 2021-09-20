from flask import Flask, render_template, request, session

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']
EVENT_URL = 'https://app.ticketmaster.com/discovery/v2/events/'


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite.
    
    Use form data from /afterparty (in 'search-form.html') to populate any search parameters.
    """

    parameters = ['keyword', 'zipcode', 'radius', 'unit', 'sort']

    # keyword = request.args.get('keyword', '')
    # postalcode = request.args.get('zipcode', '')
    # radius = request.args.get('radius', '')
    # unit = request.args.get('unit', '')
    # sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}

    for item in parameters:
        if item in 'zipcode':
            payload['postalCode'] = request.args.get(item, '')
        else:
            payload[item] = request.args.get(item, '')

    payload['size'] = 2

    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    # data = {'Test': ['This is just some test data'],
    #         'page': {'totalElements': 1}}
    res = requests.get(url, params=payload)
    data = res.json()
    session['json_data'] = data
    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""
    url = f"{EVENT_URL}{id}"
    payload = {'apikey': API_KEY}

    response = requests.get(url, params=payload)

    event = response.json()
    venues = event['_embedded']['venues']

    # event_details_req_url = f"{EVENT_URL}{id}.json?apikey={API_KEY}"
    # event_json = requests.get(event_details_req_url).json()

    # event_details = ['name', 'start_date', 'venues', 'classifications', 'ticketmaster_url']
    # start_date = event_json['embedded']['events'][0]['dates']['start']['localDate']

    image_req_url = f"{EVENT_URL}{id}/images.json?apikey={API_KEY}"
    image_json = requests.get(image_req_url).json()
    image_url = image_json['images'][0]['url']

    return render_template('event-details.html', venues=venues, id=id, image_url=image_url, event=event, pformat=pformat)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
