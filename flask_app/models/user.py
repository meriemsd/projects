from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def create(cls, data):

        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """

        return connectToMySQL(DB).query_db(query, data)

    # get a user by email
    @classmethod
    def get_by_email(cls, data):

        query = """
                    SELECT * FROM users
                    WHERE email = %(email)s;
            """
        result = connectToMySQL(DB).query_db(query, data)

        if result:
                return cls(result[0])
        else:
                return None


    @classmethod
    def get_by_id(cls, data):

        query = """
                    SELECT * FROM users
                    WHERE id = %(id)s;
            """
        result = connectToMySQL(DB).query_db(query, data)

        if result:
                return cls(result[0])
        else:
                return None

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data["first_name"]) < 2:
            is_valid = False
            flash("first name is required ! (at least 2 caracters)", "register")

        if len(data["last_name"]) < 2:
            is_valid = False
            flash("last name is required ! (at least 2 caracters)", "register")

        if len(data["email"]) == 0:
            is_valid = False
            flash("email is required !")

        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        else:
            email_dict = {"email": data["email"]}
            potential_user = User.get_by_email(email_dict)
            if potential_user:
                is_valid = False
                flash("This email is already taken; Hopefully by you !", "register")

        if len(data["password"]) < 7:
            is_valid = False
            flash("password required", "register")

        elif not data["password"] == data["confirm_password"]:
            is_valid = False
            flash("passwords don't match !", "register")

        return is_valid

    @staticmethod
    def validate_login_user(data):
        is_valid = True

        if len(data["email"]) < 1:
            is_valid = False
            flash("email is required !", "login")

        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "login")
            is_valid = False

        if len(data["password"]) < 1:
            is_valid = False
            flash("password is required !", "login")

        return is_valid