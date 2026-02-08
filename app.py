import os
import sys
from flask import Flask
from dotenv import load_dotenv
from site_meta import SITE_CREATED, site_last_updated

# Ensure local modules are importable when run via Flask CLI
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")

@app.context_processor
def inject_site_meta():
    return {
        "site_created": SITE_CREATED,
        "site_updated": site_last_updated(),
    }

from home import home_bp
from markets import markets_bp
from tools import tools_bp
from personal import personal_bp
from admin_page import admin_bp
from api import api_bp
from news import news_bp
from guide import guide_bp
from suggestions import suggestions_bp

app.register_blueprint(home_bp)
app.register_blueprint(markets_bp)
app.register_blueprint(tools_bp)
app.register_blueprint(personal_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)
app.register_blueprint(news_bp)
app.register_blueprint(guide_bp)
app.register_blueprint(suggestions_bp)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
