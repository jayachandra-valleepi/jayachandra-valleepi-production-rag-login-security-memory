from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app.chatbot.rag_chain import get_response

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():

    data = request.json

    query = data.get("query")

    username = get_jwt_identity()

    response = get_response(query, username)

    return {
        "username": username,
        "query": query,
        "answer": response
    }