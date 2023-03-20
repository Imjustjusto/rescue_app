from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import pet
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pets =[]

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) < 4:
            flash("Username must be more than 3 characters", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "registration")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "registration")
            is_valid = False
        if not data['password2'] == data['password']:
            flash('Passwords do not match', "registration")
            is_valid = False
        return is_valid
    
    @classmethod
    def updateuser(cls, data):
        query = "UPDATE users SET username = %(username)s, email = %(email)s, password = %(password)s WHERE users.id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        return result
    
    @classmethod
    def getuser(cls, id):
        data = {'id':id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def createuser(cls, data):
        query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL('petschema').query_db(query, data)
        return result
    
    @classmethod
    def getbyemail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def getuserpet(cls, id):
        data = {"id":id}
        query = "SELECT * FROM users LEFT JOIN pets ON pets.user_id WHERE user_id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        if len(result) > 0:
            users = cls(result[0])
            for row in result:
                pet_data = {
                "id": row['pets.id'],
                "name": row['name'],
                "age": row['age'],
                "lifestyle": row['lifestyle'],
                "time": row['time'],
                "date": row['date'],
                "description": row['description'],
                "imageone": row['imageone'],
                "imagetwo": row['imagetwo'],
                "created_at": row['pets.created_at'],
                "updated_at": row['pets.updated_at']
                }
                users.pepts.append(pet.Pet(pet_data))
                return users
        else:
            data = {"id": id}
            query = "SELECT * FROM users WHERE id = %(id)s;"
            result - connectToMySQL('petschema').query_db(query, data)
            return cls(result[0])
        
    @classmethod
    def getuserbypet(cls, id):
        data = {"id": id}
        query = "SELECT * FROM users LEFT JOIN pets ON pets.user_id = users.id WHERE pets.id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        users = cls(result[0])
        return users

