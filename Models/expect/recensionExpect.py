from flask_restx import fields

from Domain.extensions import api

recensionPost = api.model('Recension post',
                         {
                             "clientId": fields.String(required=True),
                             "restaurantId": fields.String(required=True),
                             "recension": fields.String(required=True),
                             "rating":fields.Float(required=True)
                         })