
from flask_restx import Namespace, Resource

from Models.expect.userExpect import login
from Domain.extensions import db
from Utils.Exceptions.customExceptions import CustomException
from Infrastructure.Repositories.loginRepo import loginRepo, forgotPasswordRepo, resetPasswordRepo

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
@nsLogin.route("/forgotpasswordsendemail/<string:email>")
class ForgotPasswordApi(Resource):
    def get(self,email):
        try:
            return forgotPasswordRepo(email)

        except CustomException as ce:
            return {"message": ce.message}, ce.statusCode

        except Exception:
            return {"message": "Something went wrong"}, 500

@nsLogin.route("/resetpassword/<string:email>/<string:newpassword>/<int:code>")
class ResetPasswordApi(Resource):
    def put(self,email,newpassword,code):
        try:
            return resetPasswordRepo(email,newpassword,code)

        except CustomException as ce:
            return {"message": ce.message}, ce.statusCode

        except Exception:
            return {"message": "Something went wrong"}, 500





