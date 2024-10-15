from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    app.config.from_object('config.Config')  # Load configuration

    db.init_app(app)  # Bind the database to the app
    migrate.init_app(app, db)  # Bind the migration to the app

    # Import Blueprints and register them
    from app.routes.auth import auth_bp
    from app.routes.hotels import hotels_bp
    from app.routes.bookings import bookings_bp
    from app.routes.reviews import reviews_bp
    from app.routes.deals import deals_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(hotels_bp, url_prefix='/hotels')
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(deals_bp, url_prefix='/deals')

    return app  # Return the created app instance
