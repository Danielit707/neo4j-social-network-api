# app/models/user_model.py
from app.database import get_db

def create_user(username, email, password_hash):
    with get_db() as session:
        session.run("""
            CREATE (u:User {username: $username, email: $email, password: $password})
        """, username=username, email=email, password=password_hash)

def get_user_by_email(email):
    with get_db() as session:
        result = session.run("""
            MATCH (u:User {email: $email}) RETURN u
        """, email=email)
        return result.single()
