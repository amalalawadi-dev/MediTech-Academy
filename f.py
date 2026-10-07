from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

DB_PATH = 'database.db'

# إنشاء قاعدة البيانات من الصفر
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        users = [
            ('doc1@example.com', '123456', 'doctor'),
            ('stu1@example.com', '123456', 'student'),
            ('eng1@example.com', '123456', 'biomedical engineer'),
            ('inst1@example.com', '123456', 'instructor'),
            ('admin@example.com', 'admin1', 'admin')
        ]
        for user in users:
            try:
                cursor.execute(
                    'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
                    user
                )
            except sqlite3.IntegrityError:
                pass
        conn.commit()


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    flash("Here I am ", "success")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user[0]
                session["role"] = user[3]  # role موجود في العمود الرابع
                flash("تم تسجيل الدخول بنجاح!", "success")
                return redirect(url_for("home"))
            else:
                flash("البريد الإلكتروني أو كلمة المرور غير صحيحة", "danger")
    return render_template("Login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
                    (email, password, role)
                )
                conn.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Email already exists.', 'danger')
    return render_template('register.html')



@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password=? WHERE email=?', (new_password, email))
            if cursor.rowcount == 0:
                flash('البريد الإلكتروني غير موجود.', 'danger')
            else:
                conn.commit()
                flash('تم تغيير كلمة المرور بنجاح.', 'success')
                return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route("/home")
def home():
    if "user_id" not in session:
        flash("يجب تسجيل الدخول أولاً.", "warning")
        return redirect(url_for("login"))
    return render_template("register.html", role=session.get("role"))

@app.route("/videos")
def videos():
    free_video = {
        'title': 'Ventilators',
        'embed_url': 'https://www.youtube.com/embed/yDtKBXOEsoM?si=C6FB-GApO1F6ov9Y'
    }
    locked_videos = [
        {
            'title': 'Dialysis Machine',
            'embed_url': 'https://www.youtube.com/embed/8odarwgNCgw'
        },
        {
            'title': 'Dialysis Machine',
            'embed_url': 'https://www.youtube.com/embed/hxTxROuUj4g'
        },
        {
            'title': 'X-ray',
            'embed_url': 'https://www.youtube.com/embed/gsV7SJDDCY4'
        },
        {
            'title': 'Nebulization',
            'embed_url': 'https://www.youtube.com/embed/6Q3o-3rZOpA'
        },
        {
            'title': 'Electrosurgery Unit',
            'embed_url': 'https://www.youtube.com/embed/KNmQCQi-fnE'
        },
        {
            'title': 'Anesthesia Machines',
            'embed_url': 'https://www.youtube.com/embed/YhBSkfrCrWA'
        },
        {
            'title': 'Portable Suction Machine',
            'embed_url': 'https://www.youtube.com/embed/o0Hvd2YX7xI'
        },
        {
            'title': 'MRI Machine',
            'embed_url': 'https://www.youtube.com/embed/nFkBhUYynUw'
        },
        {
            'title': 'Dual Source CT - Turbo Flash',
            'embed_url': 'https://www.youtube.com/embed/CtPhxCc59lA'
        }
    ]
    subscribed = session.get("subscribed", False)
    return render_template(
        "Videos.html",
        free_video=free_video,
        locked_videos=locked_videos,
        subscribed=subscribed
    )   


@app.route("/subscribe", methods=["POST"])
def subscribe():
    if "user_id" not in session:
        flash("يجب تسجيل الدخول للاشتراك.", "warning")
        return redirect(url_for("login"))
    subscription_type = request.form.get("type")
    session["subscribed"] = True
    session["plan"] = subscription_type
    flash(f"تم الاشتراك في الخطة {subscription_type}.", "success")
    return redirect(url_for("videos"))


@app.route("/logout")
def logout():
    session.clear()
    flash("تم تسجيل الخروج.", "info")
    return redirect(url_for("login"))

@app.route("/description")
def description():
    return render_template("Description.html")


@app.route("/about")
def about():
    return render_template("About.html")

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        role = request.form['role']
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('create_account.html')
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
                    (email, password, role)
                )
                conn.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Email already exists.', 'danger')
    return render_template('create_account.html')  

# بدء التطبيق
if __name__ == "__main__":
    init_db()
    app.run(debug=True)