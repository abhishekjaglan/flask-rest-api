from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from logger import logger
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


db.create_all()

## validation of input required, validates all arguemnts' type as well as makes sure mandatory args are retrieved othertwise throws error
video_put_ags = reqparse.RequestParser()
video_put_ags.add_argument("name", type=str, help="Name of video required", required=True)
video_put_ags.add_argument("views", type=int, help="Views of video required", required=True)
video_put_ags.add_argument("likes", type=int, help="Likes of video required", required=True)

videos = {}

def abort_if_videoid_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message='Video id does not exist...') ## rather than server crashing it sends an error message back

def abort_if_video_exist(video_id):
    if video_id in videos:
        abort(409,message="Video with this id already exists...")

class Video(Resource):
    def get(self, video_id):
        abort_if_videoid_doesnt_exist(video_id)
        return {video_id: videos[video_id]}, 200

    def put(self, video_id):
        abort_if_video_exist(video_id)
        args = video_put_ags.parse_args() ## fetches all the values of arguements defined from body data and returns it
        logger.debug(args)
        print(args)
        videos[video_id] = args
        return {video_id: videos[video_id]}, 201
    
    def delete(self, video_id):
        abort_if_videoid_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204


api.add_resource(Video, '/video/<int:video_id>')    

if __name__ == "__main__":
    app.run(debug=True, port=2024)