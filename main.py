from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {
    "abhishek":{
        "age":25,
        "gender":"male"
    },
    "tim":{
        "age":23,
        "gender":"male"
    }
}

class HelloWorld(Resource):
    def get(self, name, test):
        return {
            name:name,
            "data":names[name]
        }
    
api.add_resource(HelloWorld, '/helloworld/<string:name>/<int:test>')    

if __name__ == "__main__":
    app.run(debug=True, port=2024)