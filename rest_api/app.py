from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import math

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_api'
app.config['SECRET_KEY'] = '@12w4n42y4'
mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    user_list = []
    for data in result:
        user = {
            'id': data[0],
            'username': data[1],
            'password': data[2],
        }
        user_list.append(user)
    return jsonify(user_list)
# Endpoint yang memerlukan autentikasi menggunakan token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200

@app.route('/login', methods=['POST'])
def register():
    no = request.json['id']
    username = request.json['username']
    password = request.json['password']
    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (id, username, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (no, username, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data berhasil ditambahkan'}), 200

@app.route('/login/<int:id>', methods=['PUT'])
def update_user(id):
    if not request.json:
        return jsonify({'error': 'Invalid request. Data should be in JSON format.'}), 400

    no = request.json['id']
    username = request.json['username']
    password = request.json['password']

    if not no or not username or not password:
        return jsonify({'error': 'Incomplete data. All fields are required.'}), 400

    cursor = mysql.connection.cursor()
    query = "UPDATE users SET id = %s, username = %s, password = %s WHERE id = %s"
    cursor.execute(query, (no, username, password, id))
    mysql.connection.commit()

    return jsonify({'message': 'Data mahasiswa berhasil diupdate'}), 200

@app.route('/login/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    return jsonify({'message': 'Data mahasiswa berhasil dihapus'})


@app.route('/mhs', methods=['GET'])
def get_mahasiswa():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    mahasiswa_list = []
    for data in result:
        mahasiswa = {
            'nim': data[0],
            'no': data[1],
            'nama': data[2],
            'email': data[3],
            'alamat': data[4],
        }
        mahasiswa_list.append(mahasiswa)
    return jsonify(mahasiswa_list)

@app.route('/mhs', methods=['POST'])
def insert():
    nim = request.json['nim']
    student_index = request.json['no']
    nama = request.json['nama']
    email = request.json['email']
    alamat = request.json['alamat']
    cursor = mysql.connection.cursor()
    query = "INSERT INTO students (nim, no, nama, email, alamat) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nim, student_index, nama, email, alamat))
    mysql.connection.commit()
    cursor.close()
    if request.headers.get('Content-Type') == 'application/json':
        
        return jsonify({'message': 'Data berhasil ditambahkan'}), 200
    else:
    
        return render_template('insert.html', message='Data berhasil ditambahkan')

@app.route('/mhs/<int:nim>', methods=['GET'])
def get_mahasiwa(nim):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students WHERE nim=%s", (nim,))
    mysql.connection.commit()
    mahasiswa = cursor.fetchone()
    cursor.close()
    
    if mahasiswa:
        return jsonify(mahasiswa)
    else:
        return jsonify({'error': 'Student not found'}), 404


@app.route('/mhs/<int:nim>', methods=['PUT'])
def update_mahasiswa(nim):
    if not request.json:
        return jsonify({'error': 'Invalid request. Data should be in JSON format.'}), 400

    nip = request.json.get('nim')
    student_index = request.json.get('no')
    nama = request.json.get('nama')
    email = request.json.get('email')
    alamat = request.json.get('alamat')

    if not nip or not student_index or not nama or not email or not alamat:
        return jsonify({'error': 'Incomplete data. All fields are required.'}), 400

    cursor = mysql.connection.cursor()
    query = "UPDATE students SET nim = %s, no = %s, nama = %s, email = %s, alamat = %s WHERE nim = %s"
    cursor.execute(query, (nip, student_index, nama, email, alamat, nim))
    mysql.connection.commit()

    return jsonify({'message': 'Data mahasiswa berhasil diupdate'}), 200


@app.route('/mhs/<int:nim>', methods=['DELETE'])
def delete_mahasiswa(nim):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE nim = %s", (nim,))
    mysql.connection.commit()
    return jsonify({'message': 'Data mahasiswa berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)
