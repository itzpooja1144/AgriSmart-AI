from flask import Flask, send_from_directory, render_template
import os
from dotenv import load_dotenv
from groq import Groq
from route import route
from route import route
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/static"
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# ===============================
# UPLOAD FOLDER CONFIG
# ===============================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "../uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ===============================
# IMAGE DISPLAY ROUTE
# ===============================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# ===============================
# CHATBOT PAGE
# ===============================

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# ===============================
# REGISTER BLUEPRINT
# ===============================

app.register_blueprint(route)

# ===============================
# RUN APPLICATION
# ===============================

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))