from flask_restx import fields
from Domain.extensions import api

gridExpect = api.model("Grid", {

    "rows": fields.Integer,
    "columns": fields.Integer,
    "type": fields.String,
    "name": fields.String,
})

tableMapExpect = api.model("Tables map", {
    "totalRows": fields.Integer,
    "totalColumns": fields.Integer,
    "cells": fields.List(fields.Nested(gridExpect))
})