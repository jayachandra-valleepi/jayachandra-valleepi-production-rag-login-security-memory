from flask import Blueprint, request
from flask_jwt_extended import create_access_token


from app.users.users import users

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login",methods = ["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username not in users:
        return {
            "error" : "Invalid Username"
        }, 401
    if users[username]["password"] != password:

        return {
            "error" : "Invalid Password"
        }, 401
    
    token = create_access_token(identity=username)

    return {
    "message": "Login Success",
    "token": token,
    "department": users[username]["department"]
    }