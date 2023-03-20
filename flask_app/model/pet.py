from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pet:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.species = data['species']
        self.lifestyle = data['lifestyle']
        self.time = data['time']
        self.date = data['date']
        self.description = data['description']
        self.imageone = data['imageone']
        self.imagetwo = data['imagetwo']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def addpet(cls, data):
        query = "INSERT INTO pets (name, age, species, lifestyle, time, date, description, imageone, imagetwo, user_id, created_at, updated_at) VALUES (%(name)s, %(age)s, %(species)s, %(lifestyle)s, %(time)s, %(date)s, %(description)s, %(imageone)s, %(imagetwo)s, %(user_id)s, NOW(), NOW());"
        result = connectToMySQL('petschema').query_db(query, data)
        return result
    
    @classmethod
    def viewpet(cls, pet_id):
        data = {
            "pet_id" : pet_id
        }
        query = "SELECT * FROM pets WHERE id = %(pet_id)s"
        result = connectToMySQL('petschema').query_db(query, data)
        pet = cls(result[0])
        return pet
    
    @classmethod
    def getpets(cls):
        query = "SELECT * FROM pets;"
        result = connectToMySQL('petschema').query_db(query)
        return result
    
    @classmethod
    def updatepet(cls, data):
        query = "UPDATE pets SET name = %(name)s, age = %(age)s, species = %(species)s, lifestyle = %(lifestyle)s, time = %(time)s, date = %(date)s, description = %(description)s, imageone = %(imageone)s, imagetwo = %(imagetwo)s, updated_at = NOW() WHERE pets.id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        return result
    
    @classmethod
    def deletepet(cls, id):
        data = {"id" : id}
        query = "DELETE FROM pets WHERE id = %(id)s;"
        result = connectToMySQL('petschema').query_db(query, data)
        return result
    
    @staticmethod
    def validate_pet(data):
        is_valid= True
        if len(data['name']) < 2:
            flash("Name should be at least two characters")
            is_valid = False
        if (data['age']) <= 0:
            flash("The pet cannot be a negative age")
            is_valid = False
        if len(data['description']) < 10:
            flash("Please provide a description of the pet at least 10 characters long")
            is_valid = False
        return is_valid
