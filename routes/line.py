from flask import jsonify
from flask_restx import Namespace, Resource, fields
import requests

api = Namespace('lines', description='')

line = api.schema_model(
    'line', {
        'id': fields.String,
        'stopPoint': [{
            'pointName': fields.String,
            'pointsCoordinates': {
                'longitude': fields.Float,
                'latitude': fields.Float
            }
        }]
    }
)


@api.route('/<city>/<bus>')
@api.param('bus', 'Bus reference id')
@api.response(200, line)
@api.response(404, 'Bus not found')
class TransportLine(Resource):

    @api.doc('get_transport_line')
    def get(self, city, bus):
        """Fetch all transport type from a given city"""
        url = 'https://tr.transport.data.gouv.fr/%s/gtfs-rt.json' % (city)
        response = requests.get(url)
    
        if response.status_code == 404:
            api.abort(404)

        busStopIdList = []
        for entity in response.json()['entity']:
            if entity['tripUpdate'] is not None:
                if entity['tripUpdate']['vehicle']['id'] == bus:
                    for stopIds in entity['tripUpdate']['stopTimeUpdate']:
                        busStopIdList.append(stopIds['stopId'])

        
        lineRef = ''
        busStopIdsNamesList = []
        for busStopId in busStopIdList:
            url = 'https://tr.transport.data.gouv.fr/%s/siri/2.0/stop-monitoring.json?MonitoringRef=%s' % (city, busStopId)
            response = requests.get(url)

            if response.status_code == 404:
                api.abort(404)

            for siri in response.json()['Siri']['ServiceDelivery']['StopMonitoringDelivery']:
                for monitoredStopVisit in siri['MonitoredStopVisit']:
                    lineRef = monitoredStopVisit['MonitoredVehicleJourney']['LineRef']
                    busStopIdsNamesList.append(monitoredStopVisit['MonitoredVehicleJourney']['MonitoredCall']['StopPointName'])

        busLineStopCoordinates = []
        for busStopName in busStopIdsNamesList: 
            flag = False
            for pointName in busLineStopCoordinates:
                if pointName['pointName'] == busStopName:
                    busLineStopCoordinates.append(pointName)
                    flag = True

            if flag != True:
                url = 'https://tr.transport.data.gouv.fr/%s/siri/2.0/stoppoints-discovery.json?q=%s' % (city, busStopName)
                response = requests.get(url)
                
                if response.status_code == 404:
                    api.abort(404)

                busLineStopCoordinates.append({
                    'pointName': busStopName,
                    'pointsCoordinates': {
                        'longitude': response.json()['Siri']['StopPointsDelivery']['AnnotatedStopPoint'][0]['Location']['longitude'],
                        'latitude': response.json()['Siri']['StopPointsDelivery']['AnnotatedStopPoint'][0]['Location']['latitude']
                    }
                })
        
        line = {
            'id': lineRef,
            'stopPoint': busLineStopCoordinates
        }   

        return line
