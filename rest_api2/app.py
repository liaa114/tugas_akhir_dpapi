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
    def __init__(self, nim):
        self.id = nim


@login_manager.user_loader
def load_user(nim):
    return User(nim)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and password == user[2]:
            login_user(User(user[0]))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()

    return render_template('home.html', students=students)

@app.route('/data')
@login_required
def data():
    flash('Ini adalah pesan flash')
    pesan_flash = get_flashed_messages()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()

    
    per_page = 5  
    page = request.args.get('page', 1, type=int)  


    search_query = request.args.get('search_query', '')
    if search_query:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM students WHERE nama LIKE %s OR alamat LIKE %s"
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
        students = cursor.fetchall()
        cursor.close()

    total_students = len(students)
    num_pages = math.ceil(total_students / per_page)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    students_page = students[start_index:end_index]

    pesan_tidak_ditemukan = None  

    if not students:
        pesan_tidak_ditemukan = 'Data yang Anda cari tidak tersedia.'

    return render_template('data.html', students=students_page, page=page, num_pages=num_pages, search_query=search_query, pesan_flash=pesan_flash, pesan_tidak_ditemukan=pesan_tidak_ditemukan)

@app.route('/get', methods=['GET', 'POST'])
@login_required
def get_mhs():
    if request.method=='POST':
        nim = request.form['nim']
        index = request.form['index']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (nim, index, nama, email, alamat) VALUES (%s, %s, %s, %s, %s)", (nim, index, nama, email, alamat))
        mysql.connection.commit()
        cursor.close()
    return render_template('insert.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method=='POST':
        nim = request.form['nim']
        no = request.form['no']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (nim, no, nama, email, alamat) VALUES (%s, %s, %s, %s, %s)", (nim, no, nama, email, alamat))
        mysql.connection.commit()
        cursor.close()

    return render_template('insert.html')

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    flash('Ini adalah pesan flash')
    pesan_flash = get_flashed_messages()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()

    per_page = 5 
    page = request.args.get('page', 1, type=int) 


    search_query = request.args.get('search_query', '')
    if search_query:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM students WHERE nama LIKE %s OR alamat LIKE %s"
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
        students = cursor.fetchall()
        cursor.close()

    total_students = len(students)
    num_pages = math.ceil(total_students / per_page)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    students_page = students[start_index:end_index]

    pesan_tidak_ditemukan = None  

    if not students:
        pesan_tidak_ditemukan = 'Data yang Anda cari tidak tersedia.'

    return render_template('edit.html', students=students_page, page=page, num_pages=num_pages, search_query=search_query, pesan_flash=pesan_flash, pesan_tidak_ditemukan=pesan_tidak_ditemukan)

@app.route('/update/<string:nim>', methods=['GET', 'POST'])
@login_required
def update(nim):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students WHERE nim = %s", (nim,))
    student = cursor.fetchone()

    if request.method == 'POST':
        no = request.form['no']
        nama = request.form['nama']
        email = request.form['email']
        alamat = request.form['alamat']

        if student:
            
            cursor.execute("UPDATE students SET no = %s, nama = %s, email = %s, alamat = %s WHERE nim = %s", (no, nama, email, alamat, nim))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('edit'))  

    return render_template('update.html', student=student)
        
    return render_template('update.html')

@app.route('/delete/<string:nim>', methods=['GET', 'POST'])
@login_required
def delete(nim):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students WHERE nim = %s", (nim,))
    student = cursor.fetchone()

    if student:
        cursor.execute("DELETE FROM students WHERE nim = %s", (nim,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('edit'))  

    return redirect(url_for('edit'))


if __name__ == '__main__':
    app.run(debug=True)
