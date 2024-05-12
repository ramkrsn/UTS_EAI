# inisialisasi library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# import library flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

# inisialisasi object library
app = Flask(__name__)

# inisiasai objek flask restful
api = Api(app)

# inisiasi object flask cors
CORS(app)

# inisialisasi object flask sqlalchemy


# mongkonfigurasi dulu database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

db = SQLAlchemy(app)

# Membuat database model
class ModelMovie(db.Model):
    # membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100))
    judul = db.Column(db.Integer)
    deskripsi = db.Column(db.TEXT) # field tambahan

    # membuat mothode untuk menyimpan data agar lebih simple
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


# mencreate database
with app.app_context():
    db.create_all()

# inisiasi variabel kosong bertipe dictionary
identitas = {}

# Membuat class untuk restfull 
class ContohResource(Resource):
    def get(self):
        # menampilkan data dari database sqlite
        query = ModelMovie.query.all()

        # melakukan iterasi pada modelDatabase dengan teknik 
        output = [
            {
                "id":data.id,
                "genre":data.genre, 
                "judul":data.judul, 
                "deskripsi":data.deskripsi
            } 
            for data in query
        ]

        response = {
            "code" : 200, 
            "msg"  : "Query data sukses",
            "data" : output
        }

        return response, 200

    def post(self):
        dataGenre = request.form["genre"]
        dataJudul = request.form["judul"]
        dataDeskripsi = request.form["deskripsi"]

        # masukan data ke dalam database model
        model = ModelMovie(genre=dataGenre, judul=dataJudul, deskripsi=dataDeskripsi)
        model.save()
         
        response = {
            "msg" : "Data berhasil dimasukan",
            "code": 200
        }

        return response, 200

    # delete all / hapus semua datanya
    def delete(self):
        # query all data
        query = ModelMovie.query.all() # list / kumpulan data => iterasi/looping

        # looping
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg":"Semua data berhasil dihapus",
            "code":200
        }

        return response, 200
        


# membuat class baru untuk mengedit / menghapus data
class UpdateResource(Resource):
    def put(self, id):
        # konsumsi id itu untuk query di model databasenya
        # pilih data yang ingin diedit berdasarkan id yang dimasukan
        query = ModelMovie.query.get(id)

        # form untuk pegeditan data
        editGenre = request.form["genre"]
        editJudul = request.form["judul"]
        editDeskripsi = request.form["deskripsi"]

        # mereplace nilai yang ada di setiap field/kolom
        query.genre = editGenre
        query.judul = editJudul
        query.deskripsi = editDeskripsi
        db.session.commit()

        response = {
            "msg" : "edit data berhasil",
            "code": 200
        }

        return response, 200

    # delete by id, bukan delete all
    def delete(self, id):
        queryData = ModelMovie.query.get(id)

        # panggil methode untuk delete data by id
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg" : "delete data berhasil",
            "code" : 200
        }
        return response, 200


# inisialisasi url / api 
# testing
api.add_resource(ContohResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
    

