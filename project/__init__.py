# Package initialization
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize routes
from .routes import init_routes

init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
