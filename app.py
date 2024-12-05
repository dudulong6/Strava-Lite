from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import constants
import uuid

app = Flask(__name__)
api = Api(app)

users = {}
following = {}


# register
class UserRegister(Resource):
    def post(self):
        data = request.json
        if 'name' not in data or 'age' not in data:
            return {"error": "Missing required fields"}, 400

        user_id = str(uuid.uuid4())  # generate unique ID
        users[user_id] = {
            "name": data['name'],
            "age": data['age'],
            "workouts": []
        }
        following[user_id] = []
        return {"id": user_id, "name": data['name'], "age": data['age']}, 200


api.add_resource(UserRegister, "/user")


# get,remove
class User(Resource):
    def get(self, user_id):
        if user_id in users:
            return users[user_id], 200
        return {"message": "User not found!"}, 404

    def delete(self, user_id):
        if user_id in users:
            del users[user_id]
            del following[user_id]  # delete following list
            return {}, 200
        return {"message": "User not found!"}, 404


api.add_resource(User, "/user/<string:user_id>")


# list
class UsersList(Resource):
    def get(self):
        return {"users": [{"id": uid, **info} for uid, info in users.items()]}, 200


api.add_resource(UsersList, "/users")


# add
class Workout(Resource):
    def put(self, user_id):
        data = request.json
        if 'date' not in data or 'time' not in data or 'distance' not in data:
            return {"error": "Missing required fields"}, 400
        if user_id not in users:
            return {"message": "User not found!"}, 404

        workout = {
            "date": data['date'],
            "time": data['time'],
            "distance": data['distance']
        }
        users[user_id]['workouts'].append(workout)
        return workout, 200

    def get(self, user_id):
        if user_id not in users:
            return {"message": "User not found!"}, 404
        return {"workouts": users[user_id]['workouts']}, 200


api.add_resource(Workout, "/workouts/<string:user_id>")


# follow
class FollowUser(Resource):
    def put(self, user_id):
        data = request.json
        if 'follow_id' not in data:
            return {"error": "Missing required fields"}, 400
        follow_id = data['follow_id']

        if user_id not in users or follow_id not in users:
            return {"message": "User not found!"}, 404

        if follow_id not in following[user_id]:
            following[user_id].append(follow_id)  # 添加关注
        return {"following": following[user_id]}, 200


api.add_resource(FollowUser, "/follow-list/<string:user_id>")


# show friend
class ShowFriendWorkouts(Resource):
    def get(self, user_id, follow_id):
        if user_id not in users or follow_id not in users:
            return {"message": "User not found!"}, 404

        if follow_id not in following[user_id]:
            return {"message": "Forbidden: You do not follow this user."}, 403

        return {"workouts": users[follow_id]['workouts']}, 200


api.add_resource(ShowFriendWorkouts, "/follow-list/<string:user_id>/<string:follow_id>")

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=constants.PORT)