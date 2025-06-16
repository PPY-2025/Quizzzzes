from app import create_app
from backend.models import db
from backend.services import dbService

# Create the Flask app
app = create_app()


# Initialize the database tables within the application context
with app.app_context():
    db.create_all()  # Create all database tables if they don't already exist
    dbService.populate_dummy_data()

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
