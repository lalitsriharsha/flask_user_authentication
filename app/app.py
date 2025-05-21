from flask import Flask, render_template, request, redirect, url_for, session, flash
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import InvalidRequest

app = Flask(__name__)
app.secret_key = 'flask_task'

KEYSPACE = 'user_auth'

# Cassandra Setup
cluster = Cluster()
session_db = cluster.connect()

# Create keyspace and table
session_db.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1 }}
""")
session_db.set_keyspace(KEYSPACE)

session_db.execute("""
    CREATE TABLE IF NOT EXISTS users_detail (
        username TEXT PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        age INT,
        password TEXT,
        security_question TEXT,
        security_answer TEXT
    )
""")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'firstname': request.form['firstname'],
            'lastname': request.form['lastname'],
            'age': int(request.form['age']),
            'password': request.form['password'],
            'security_question': request.form['security_question'],
            'security_answer': request.form['security_answer']
        }

        query = SimpleStatement("""
            INSERT INTO users_detail (username, firstname, lastname, age, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        try:
            session_db.execute(query, (
                data['username'], data['firstname'], data['lastname'],
                data['age'], data['password'],
                data['security_question'], data['security_answer']
            ))
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
        except InvalidRequest as e:
            flash("Registration failed. Please check your input.")
            return redirect(url_for('register'))
        except Exception as e:
            flash("Username already exists.")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = session_db.execute(
            "SELECT * FROM users_detail WHERE username=%s", (username,)
        )
        user = result.one()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        session['recover_user'] = username
        result = session_db.execute("SELECT security_question FROM users_detail WHERE username=%s ALLOW FILTERING", (username,))
        row = result.one()
        if row:
            return render_template('reset_password.html', step='question', question=row.security_question, step_action=url_for('security_question'))
        else:
            flash("Username not found.")
    return render_template('reset_password.html', step='username', step_action=url_for('forgot_password'))

@app.route('/security_question', methods=['POST'])
def security_question():
    answer = request.form['answer']
    username = session.get('recover_user')
    result = session_db.execute("SELECT security_answer FROM users_detail WHERE username=%s ALLOW FILTERING", (username,))
    row = result.one()
    if row and row.security_answer == answer:
        return render_template('reset_password.html', step='new_password', step_action=url_for('reset_password'))
    else:
        flash("Incorrect answer.")
        return redirect(url_for('forgot_password'))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    new_password = request.form['new_password']
    username = session.get('recover_user')
    session_db.execute("UPDATE users_detail SET password=%s WHERE username=%s", (new_password, username))
    flash("Password reset successful.")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/delete_user')
def delete_user():
    username = session.get('username')
    session_db.execute("DELETE FROM users_detail WHERE username=%s", (username,))
    session.pop('username', None)
    flash("Account deleted.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)