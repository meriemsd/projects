from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models.user import User
from flask import flash

class Travel:
    def __init__(self , data):
        self.id= data["id"]
        self.destination = data["destination"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.plan = data["plan"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = None

    @classmethod
    def get_by_id(cls , data):
        query = "SELECT * FROM travels JOIN users ON travels.user_id = users.id WHERE travels.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query , data)

        travel = None
        if result:
            travel = cls(result[0])
            user_data ={

                    'id': result[0]['users.id'],
                    'first_name': result[0]['first_name'],
                    'last_name': result[0]['last_name'],
                    'email': result[0]['email'],
                    'password': result[0]['password'],
                    'created_at': result[0]['users.created_at'],
                    'updated_at': result[0]['users.updated_at']
            }
            travel.user = User(user_data)
        return travel


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM travels JOIN users ON travels.user_id = users.id"
        results = connectToMySQL(DB).query_db(query)

        travels = []
        if results:
            for row in results:
                travel = cls(row)
                user_data={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']

                }
                travel.user = User(user_data)
                travels.append(travel)
        return travels

    @classmethod
    def create(cls , data):
        query = "INSERT INTO travels (destination , start_date , end_date , plan , user_id) VALUES (%(destination)s , %(start_date)s , %(end_date)s , %(plan)s , %(user_id)s);" 
        result = connectToMySQL(DB).query_db(query , data)
        return result


    @classmethod
    def update(cls , data):
        query = "UPDATE travels SET destination = %(destination)s , start_date = %(start_date)s  , end_date = %(end_date)s , plan = %(plan)s WHERE id= %(id)s;" 
        result = connectToMySQL(DB).query_db(query , data)
        return result


    @classmethod
    def delete(cls , data):
        query = "DELETE FROM travels WHERE id = %(id)s;" 
        result = connectToMySQL(DB).query_db(query , data)
        return result
    
    @staticmethod
    def validate_trip(data):
        is_valid = True

        if len(data['destination']) < 3:
            is_valid = False
            flash("a trip destination must consist of at least 3 caracters)", "register")

        if len(data["plan"]) == 0:
            is_valid = False
            flash("a plan must be provided! ", "register")

        if data["start_date"]>data["end_date"]:
            is_valid = False
            flash("time travel is not allowed")
        return is_valid
