from flask_restx import Api
from .transport import api as transport
from .line import api as line

api = Api(
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(transport, path='/api/v1/transports')
api.add_namespace(line, path='/api/v1/lines')