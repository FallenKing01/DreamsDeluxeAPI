from flask_restx import fields

from Domain.extensions import api

employerExpect = api.model("Waiter Expect", {

    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "role": fields.String,
    "salary": fields.Float,
    "birthdate": fields.String,
    "description": fields.String,
    "userId": fields.String

})


editEmployer = api.model("Edit Employer",  {

    "name": fields.String,
    "password": fields.String,
    "role": fields.String,
    "salary": fields.Float,
    "income": fields.Float,
    "description": fields.String,
    "birthdate": fields.String
})
