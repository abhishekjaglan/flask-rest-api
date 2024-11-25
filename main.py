from flask import Flask, request, views
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from logger import logger
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy()
db.init_app(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

## validation of input required, validates all arguemnts' type as well as makes sure mandatory args are retrieved othertwise throws error
video_put_ags = reqparse.RequestParser()
video_put_ags.add_argument("name", type=str, help="Name of video required", required=True)
video_put_ags.add_argument("views", type=int, help="Views of video required", required=True)
video_put_ags.add_argument("likes", type=int, help="Likes of video required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

#def abort_if_videoid_doesnt_exist(video_id):
#    if video_id not in videos:
#        abort(404, message='Video id does not exist...') ## rather than server crashing it sends an error message back

#def abort_if_video_exist(video_id):
#    if video_id in videos:
#        abort(409,message="Video with this id already exists...")

# Resource Field: How an object should be serialized
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer 
}

class Video(Resource):
    @marshal_with(resource_fields) # this serializes the result/output of db query by mapping them using resource fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() # returns an instance of VideoModel, not serializable i.e, not readable by response getter
        if not result:
            abort(404, message="Video with this id does not exist...")
        return result, 200

    @marshal_with(resource_fields)
    def post(self, video_id):        
        args = video_put_ags.parse_args() ## fetches all the values of arguements defined from body data and returns it
        logger.debug(args)
        print(args)
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video with this id already exists...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        try:
            db.session.add(video)
            db.session.commit()
            return video, 201
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while creating: {str(e)}")

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        try:
            if args['name']:
                result.name = args['name']
            if args['views']:
                result.views = args['views']
            if args['likes']:
                result.likes = args['likes']

            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while updating: {str(e)}")        
    
    @marshal_with(resource_fields)
    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404,message="Video with this id does not exist...")
        try:
            db.session.delete(video)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            abort(500, message=f'An error occured while deleting: {str(ex)}')
        return '', 204

# create database tables
with app.app_context():
    db.create_all()

api.add_resource(Video, '/video/<int:video_id>')    

if __name__ == "__main__":
    app.run(debug=True, port=2024)