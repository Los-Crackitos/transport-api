"""
This module represent transports api methods
"""
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# Return transports for a given id or all transports datasets
# Param name is city
@app.route('/api/v1/transports', methods=['GET'])
def get_transports():
    """ Get all transports or transports
    from a city
    Param name is city
    """
    # Default url that return all datasets
    url = 'https://tr.transport.data.gouv.fr'

    # If request contain a city param, change url to fetch specified dataset
    if 'city' in request.args:
        city = request.args['city']
        url = '%s/%s/gtfs-rt.json' % (url, city)

    response = requests.get(url)
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
