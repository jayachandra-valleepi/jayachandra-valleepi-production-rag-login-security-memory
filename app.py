
from flask import Flask
from flask_jwt_extended import JWTManager

from app.routes.auth_routes import auth_bp
from app.routes.chat_routes import chat_bp


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "jay_medibot_secret"

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)


@app.route("/")
def home():

    return {
        "message": "Realtime RAG Chatbot Running"
    }


if __name__ == "__main__":

    app.run(
        debug=True
    )

