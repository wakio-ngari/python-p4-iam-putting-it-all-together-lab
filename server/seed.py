#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Recipe, User

fake = Faker()

def seed_database():
    with app.app_context():
        print("Deleting all records...")
        Recipe.query.delete()
        User.query.delete()

        print("Creating users...")
        users = []
        usernames = set()

        for _ in range(20):
            username = fake.unique.first_name().lower()
            usernames.add(username)
            user = User(
                username=username,
                email=fake.unique.email(),
                bio=fake.paragraph(nb_sentences=3),
                image_url=fake.url()
            )
            user.password_hash = 'testpassword'  # Will be hashed
            users.append(user)

        db.session.add_all(users)

        print("Creating recipes...")
        recipes = []
        for _ in range(100):
            instructions = fake.paragraph(nb_sentences=8)
            while len(instructions) < 50:
                instructions = fake.paragraph(nb_sentences=8)
            
            recipes.append(Recipe(
                title=fake.sentence(),
                instructions=instructions,
                minutes_to_complete=randint(15, 90),
                user=rc(users)
            ))

        db.session.add_all(recipes)
        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_database()