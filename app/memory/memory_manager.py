import os
import json

CHAT_FOLDER = "chat_history"


def save_chat_history(username, question, answer):

    os.makedirs(CHAT_FOLDER, exist_ok=True)

    filepath = os.path.join(
        CHAT_FOLDER,
        f"{username}.json"
    )

    chat_data = {
        "question": question,
        "answer": answer
    }

    history = []

    if os.path.exists(filepath):

        with open(filepath, "r") as f:
            history = json.load(f)

    history.append(chat_data)

    with open(filepath, "w") as f:
        json.dump(history, f, indent=4)