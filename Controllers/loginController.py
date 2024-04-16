
from flask_restx import Namespace, Resource

from Models.expect.userExpect import login
from Domain.extensions import db
from Utils.Exceptions.customExceptions import CustomException
from Infrastructure.Repositories.loginRepo import loginRepo
nsLogin = Namespace("login", description="Login user")
collection = db["user"]


@nsLogin.route("/")
class LoginApi(Resource):
    @nsLogin.expect(login)
    def post(self):

        try:
            return loginRepo(nsLogin.payload)

        except CustomException as ce:
            return {"message": ce.message}, ce.statusCode

        except Exception:
            return {"message": "Something went wrong"}, 500






