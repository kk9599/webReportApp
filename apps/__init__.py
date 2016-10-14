from flask import Flask
from flask_restful import Resource, Api,fields,marshal_with_field

app= Flask(__name__)
api = Api(app)


import apps.model
import apps.view




