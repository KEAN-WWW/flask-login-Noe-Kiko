from application import init_app
from application.database import db, User

app = init_app()

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()
    
    # Create a test user
    user = User.create('steve@123.com', '123456')
    db.session.add(user)
    db.session.commit()
    print("Database initialized and test user created successfully!") 