from flask_restx import Api
from .transport import api as transport

api = Api(
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(transport, path='/api/v1/transports')
