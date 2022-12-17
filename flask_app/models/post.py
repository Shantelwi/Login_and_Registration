from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
import math

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.user_id = data['user_id']
        # None can represent a currently empty space for a single User dictionary to be placed here, as a Tweet is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.user = None

    # def timespan(self):
    #     now = date.today()
    #     today = now.strftime("%b %d,%Y")
    #     print('today', today)
    #     return today

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_all_posts_with_user(cls):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        result = connectToMySQL('login_registration').query_db(query)
        all_posts = []
        for row in result:
            # Create a Tweet class instance from the information from each db row
            one_post = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_posts_user_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            this_user = user.User(one_posts_user_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_post.user = this_user
            # Append the Tweet containing the associated User to your list of tweets
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def get_by_post_id(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s"
        results = connectToMySQL('login_registration').query_db(query,data)
        return cls(results[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (content,user_id) VALUES (%(content)s,%(user_id)s);"
        return connectToMySQL("login_registration").query_db(query, data)

    @classmethod
    def destroy(cls, id):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('login_registration').query_db(query,{"id": id})

    @staticmethod
    def validate_post(post):
        is_valid = True  # we assume this is true
        if len(post['content']) <= 0:
            flash("***Post content must not be blank", "error")
            is_valid = False
        return is_valid



