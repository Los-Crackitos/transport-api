from flask import jsonify
from flask_restx import Namespace, Resource, fields
import requests


api = Namespace('transports', description='')

type_details = api.model('Type_details', { ## Modele qui est retourné par la route via le tag @api.marshal_with
    'id': fields.Integer,
    'isDeleted': fields.Boolean,
    'vehicule': fields.String,
    'alert': fields.String,
    'line': fields.String(attribute='entity.0.tripUpdate.trip.routeId')
})

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
    # Quand @api.marshal_with est déclaré, c'est l'objet qui est retourné même si les valeurs sont nulles
    #@api.marshal_with(type_details, envelope='transports_type_details')
    def get(self, city):
        """Fetch all transport type from a given city"""
        url = 'https://tr.transport.data.gouv.fr/%s/gtfs-rt.json' % (city)
        response = requests.get(url)
        if response.status_code == 404:
            api.abort(404)

        test = response.json()
        #return test["entity"]
        return jsonify(response.json())
