from flask import Flask
from flask_migrate import Migrate
from database.models import db
from database.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    from routes import main
    app.register_blueprint(main.bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
