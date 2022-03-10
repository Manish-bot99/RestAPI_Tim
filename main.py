from email import message
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(99), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# db.create_all()

# names = {"tim":{"age":30,"gender":"Male" },
#          "sam":{"age":10,"gender":"Female"}}

# class HelloWorld(Resource):
#     def get(self, name ):
#         return names[name]

#     def post(self):
#         return {'data': 'Posted'}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required!")
video_put_args.add_argument("views", type=int,  help="Views of the video!")
video_put_args.add_argument("likes", type=int,  help="Likes of the video!")

# videos = {}

# def abort_video_get(video_id):
#     if video_id not in videos:
#         abort(404, message=f"Video {video_id} doesn't exist")
    
# def abort_video_put(video_id):
#     if video_id in videos:
#         abort(404, message=f"Video {video_id} already exists")

resourse_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer 
}

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required!")
video_update_args.add_argument("views", type=int,  help="Views of the video!")
video_update_args.add_argument("likes", type=int,  help="Likes of the video!")

class Video(Resource):
    @marshal_with(resourse_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with id {video_id}")
        return result

    @marshal_with(resourse_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message=f"Video {video_id} already exists")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resourse_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Video {video_id} doesn't exist, cannot update")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
            # db.session.add(result)
        db.session.commit()
        return result, 301

    # @marshal_with(resourse_fields)
    # def delete(self, video_id):
    #     # abort_video_get(video_id)
    #     del videos[video_id]
    #     return '', 204

api.add_resource(Video, "/video/<int:video_id>" )
if __name__ == "__main__":
    app.run(debug=True)