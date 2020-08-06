from flask import jsonify
from flask_restx import Namespace, Resource, fields
import requests

api = Namespace('transports', description='')


@api.route('/')
class CitiesTransportsList(Resource):

    @api.doc('list_transports')
    def get(self):
        """Fetch all cities transports"""
        response = requests.get('https://tr.transport.data.gouv.fr/')
        return jsonify(response.json())


@api.route('/<city>')
@api.param('city', 'City of transport data')
@api.response(404, 'City not found')
class CityTransportsList(Resource):

    @api.doc('get_transport_type')
    def get(self, city):
        """Fetch all transport type from a given city"""
        url = 'https://tr.transport.data.gouv.fr/%s/gtfs-rt.json' % (city)
        response = requests.get(url)
        if response.status_code == 404:
            api.abort(404)
        return jsonify(response.json())
