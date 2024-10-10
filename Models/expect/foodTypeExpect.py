from flask_restx import fields

from Domain.extensions import api

foodTypePost = api.model('Food Type',
                         {
                             "typeName": fields.String(required=True),

                         })