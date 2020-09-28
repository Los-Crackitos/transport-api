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


transport = api.schema_model(
    'transport', {
        'bus': [{
            'id': fields.Integer,
            'trip_id': fields.String,
            'vehicle_id': fields.Integer,
            'position': {
                'latitude': fields.Integer,
                'longitude': fields.Integer,
            },
            'speed': fields.String,
        }],
        'metro': [{
            'id': fields.Integer,
        }],
    })


@api.route('/<city>')
@api.param('city', 'City of transport data')
@api.response(200, transport)
@api.response(404, 'City not found')
class CityTransportsList(Resource):

    @api.doc('get_transport_type')
    def get(self, city):
        """Fetch all transport type from a given city"""
        url = 'https://tr.transport.data.gouv.fr/%s/gtfs-rt.json' % (city)
        response = requests.get(url)
        if response.status_code == 404:
            api.abort(404)

        transportList = {}
        busList = []
        metroList = []
        for entity in response.json()['entity']:
            if entity['vehicle'] is not None:
                busList.append({
                    'id':
                        entity['id'],
                    'trip_id':
                        entity['vehicle']['trip']['tripId'],
                    'vehicle_id':
                        entity['vehicle']['vehicle']['id'],
                    'position': {
                        'latitude':
                            entity['vehicle']['position']['latitude']
                            if entity['vehicle']['position'] is not None else
                            'N/A',
                        'longitude':
                            entity['vehicle']['position']['longitude']
                            if entity['vehicle']['position'] is not None else
                            'N/A',
                    },
                    'speed':
                        entity['vehicle']['position']['speed']
                        if entity['vehicle']['position'] is not None else 0
                })

        transportList['bus'] = busList
        transportList['metro'] = metroList

        return transportList
