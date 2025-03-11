from flask_restx import Namespace, Resource
from Domain.extensions import authorizations,api
from Utils.Exceptions.customExceptions import CustomException
from Infrastructure.Repositories.regionRepo import *
from flask import abort


nsRegion = Namespace("region", authorizations=authorizations, description="Region operations")

@nsRegion.route("/judete")
class getJudete(Resource):
    def get(self):

        try:

            client = getJudeteRepo()

            return client, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")

@nsRegion.route("/orase/<string:judet>")
class getOrase(Resource):
    def get(self,judet):

        try:

            client = getOraseRepo(judet)

            return client, 200

        except CustomException as ce:

            abort(ce.statusCode, ce.message)

        except Exception:

            abort(500, "Something went wrong")