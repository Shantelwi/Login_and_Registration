from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post
import re
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.creeated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('login_registration').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_registration').query_db(query, data)
        return cls(results[0])


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("login_registration").query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_registration").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_register(user):
        is_valid = True  # we assume this is true
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_registration').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken, please try again","register")
            is_valid = False
        if len(user['first_name']) <= 0:
            flash("First name is required.", "register")
            is_valid = False
        if len(user['last_name']) <= 0:
            flash("Last name is required.", "register")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Email is required.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!","register")
            is_valid = False
        if len(user['password']) <8:
            flash("Password too short!", "register")
            is_valid = False
        if user['password'] != user ['confirm']:
            flash('Passwords do not match.', "register")
            is_valid = False
        return is_valid
