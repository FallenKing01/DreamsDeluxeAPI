from flask_restx import fields

from Domain.extensions import api

updateClientLocation = api.model('Update location',
                         {
                             "clientId": fields.String(required=True),
                             "location": fields.String(required=True),
                             "county": fields.String(required=True),
                         })