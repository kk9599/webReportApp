from apps import Api, Resource,marshal_with_field
from flask import jsonify



data = {"name", "hello"}
taseCase =[
    {"test_id":1,"testName":"103 payRollTest"},
    {"test_id":2,"testName":"104 payRollTest"}
]


class jobResult(Resource):
      def get(self):
          return jsonify(taseCase)




# resource_fields = {
#     'task':   fields.String,
#     'uri':    fields.Url('todo_ep')
# }

class jobTrackResult(object):
      def __init__(self, id):
          self.id = id




def jobResultResopond(Resource):
      #@marshal_with(resource_fields)
    return jsonify(data)