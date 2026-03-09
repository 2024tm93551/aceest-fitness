from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, Response, g
import sqlite3
import csv
import io
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aceest-fitness-secret-key'
DATABASE = 'aceest_fitness.db'

# Program Data
PROGRAMS = {
    "fat_loss": {
        "id": "fat_loss",
        "name": "Fat Loss (FL)",
        "workout": {
            "monday": "5x5 Back Squat + AMRAP",
            "tuesday": "EMOM 20min Assault Bike",
            "wednesday": "Bench Press + 21-15-9",
            "thursday": "10RFT Deadlifts/Box Jumps",
            "friday": "30min Active Recovery"
        },
        "diet": {
            "breakfast": "3 Egg Whites + Oats Idli",
            "lunch": "Grilled Chicken + Brown Rice",
            "dinner": "Fish Curry + Millet Roti",
            "target_calories": 2000
        },
        "color": "#e74c3c",
        "factor": 22
    },
    "muscle_gain": {
        "id": "muscle_gain",
        "name": "Muscle Gain (MG)",
        "workout": {
            "monday": "Squat 5x5",
            "tuesday": "Bench 5x5",
            "wednesday": "Deadlift 4x6",
            "thursday": "Front Squat 4x8",
            "friday": "Incline Press 4x10",
            "saturday": "Barbell Rows 4x10"
        },
        "diet": {
            "breakfast": "4 Eggs + PB Oats",
            "lunch": "Chicken Biryani (250g Chicken)",
            "dinner": "Mutton Curry + Jeera Rice",
            "target_calories": 3200
        },
        "color": "#2ecc71",
        "factor": 35
    },
    "beginner": {
        "id": "beginner",
        "name": "Beginner (BG)",
        "workout": {
            "all_days": "Circuit Training: Air Squats, Ring Rows, Push-ups",
            "focus": "Technique Mastery & Form (90% Threshold)"
        },
        "diet": {
            "breakfast": "Idli-Sambar",
            "lunch": "Rice-Dal",
            "dinner": "Chapati with Vegetables",
            "target_calories": 2200,
            "protein_target": "120g/day"
        },
        "color": "#3498db",
        "factor": 26
    }
}

GYM_METRICS = {
    "capacity": 150,
    "area_sqft": 10000,
    "break_even_members": 250
}


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                age INTEGER,
                height REAL,
                weight REAL,
                program TEXT,
                calories INTEGER,
                target_weight REAL,
                target_adherence INTEGER
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                week TEXT,
                adherence INTEGER
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                date TEXT,
                workout_type TEXT,
                duration_min INTEGER,
                notes TEXT
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                date TEXT,
                weight REAL,
                waist REAL,
                bodyfat REAL
            )
        ''')
        db.commit()


@app.route('/')
def home():
    return render_template('index.html', programs=PROGRAMS, metrics=GYM_METRICS)


@app.route('/programs')
def programs():
    return render_template('programs.html', programs=PROGRAMS)


@app.route('/programs/<program_id>')
def program_detail(program_id):
    program = PROGRAMS.get(program_id)
    if not program:
        return render_template('404.html'), 404
    return render_template('program_detail.html', program=program)


@app.route('/client', methods=['GET', 'POST'])
def client_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age', type=int)
        height = request.form.get('height', type=float)
        weight = request.form.get('weight', type=float)
        program_id = request.form.get('program')
        
        if not name or not program_id:
            flash('Name and Program are required', 'error')
            return redirect(url_for('client_profile'))
        
        factor = PROGRAMS.get(program_id, {}).get('factor', 25)
        calories = int(weight * factor) if weight else 0
        
        db = get_db()
        try:
            db.execute('''
                INSERT OR REPLACE INTO clients (name, age, height, weight, program, calories)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, age, height, weight, program_id, calories))
            db.commit()
            flash(f'Client {name} saved successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('client_profile'))
    
    return render_template('client.html', programs=PROGRAMS)


@app.route('/client/<name>')
def get_client(name):
    db = get_db()
    client = db.execute('SELECT * FROM clients WHERE name = ?', (name,)).fetchone()
    if not client:
        flash('Client not found', 'error')
        return redirect(url_for('clients_list'))
    return render_template('client_detail.html', client=dict(client), programs=PROGRAMS)


@app.route('/clients')
def clients_list():
    db = get_db()
    clients = db.execute('SELECT * FROM clients ORDER BY name').fetchall()
    return render_template('clients.html', clients=[dict(c) for c in clients], programs=PROGRAMS)


@app.route('/clients/export')
def export_clients_csv():
    db = get_db()
    clients = db.execute('SELECT * FROM clients').fetchall()
    
    if not clients:
        flash('No clients to export', 'error')
        return redirect(url_for('clients_list'))
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Age', 'Height', 'Weight', 'Program', 'Calories'])
    for client in clients:
        prog_name = PROGRAMS.get(client['program'], {}).get('name', client['program'])
        writer.writerow([client['name'], client['age'], client['height'], client['weight'], prog_name, client['calories']])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=clients.csv'}
    )


@app.route('/progress/<name>', methods=['POST'])
def save_progress(name):
    adherence = request.form.get('adherence', type=int, default=0)
    week = datetime.now().strftime("Week %U - %Y")
    
    db = get_db()
    db.execute('''
        INSERT INTO progress (client_name, week, adherence)
        VALUES (?, ?, ?)
    ''', (name, week, adherence))
    db.commit()
    flash(f'Progress saved for {name}', 'success')
    return redirect(url_for('get_client', name=name))


@app.route('/progress/<name>/chart')
def progress_chart(name):
    db = get_db()
    progress = db.execute('''
        SELECT week, adherence FROM progress 
        WHERE client_name = ? ORDER BY id
    ''', (name,)).fetchall()
    return render_template('progress_chart.html', 
                          client_name=name, 
                          progress=[dict(p) for p in progress])


@app.route('/workout/<name>', methods=['GET', 'POST'])
def log_workout(name):
    if request.method == 'POST':
        workout_date = request.form.get('date', date.today().isoformat())
        workout_type = request.form.get('type')
        duration = request.form.get('duration', type=int)
        notes = request.form.get('notes', '')
        
        db = get_db()
        db.execute('''
            INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, workout_date, workout_type, duration, notes))
        db.commit()
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('get_client', name=name))
    
    return render_template('log_workout.html', client_name=name)


@app.route('/workouts/<name>')
def workout_history(name):
    db = get_db()
    workouts = db.execute('''
        SELECT * FROM workouts WHERE client_name = ? ORDER BY date DESC
    ''', (name,)).fetchall()
    return render_template('workout_history.html', client_name=name, workouts=[dict(w) for w in workouts])


@app.route('/metrics/<name>', methods=['GET', 'POST'])
def log_metrics(name):
    if request.method == 'POST':
        metric_date = request.form.get('date', date.today().isoformat())
        weight = request.form.get('weight', type=float)
        waist = request.form.get('waist', type=float)
        bodyfat = request.form.get('bodyfat', type=float)
        
        db = get_db()
        db.execute('''
            INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, metric_date, weight, waist, bodyfat))
        db.commit()
        flash('Metrics logged successfully!', 'success')
        return redirect(url_for('get_client', name=name))
    
    return render_template('log_metrics.html', client_name=name)


# API Endpoints
@app.route('/api/programs')
def api_programs():
    return jsonify(PROGRAMS)


@app.route('/api/programs/<program_id>')
def api_program_detail(program_id):
    program = PROGRAMS.get(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify(program)


@app.route('/api/metrics')
def api_metrics():
    return jsonify(GYM_METRICS)


@app.route('/api/clients')
def api_clients():
    db = get_db()
    clients = db.execute('SELECT * FROM clients').fetchall()
    return jsonify([dict(c) for c in clients])


@app.route('/api/clients/<name>')
def api_client(name):
    db = get_db()
    client = db.execute('SELECT * FROM clients WHERE name = ?', (name,)).fetchone()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(dict(client))


@app.route('/api/progress/<name>')
def api_progress(name):
    db = get_db()
    progress = db.execute('''
        SELECT week, adherence FROM progress 
        WHERE client_name = ? ORDER BY id
    ''', (name,)).fetchall()
    return jsonify([dict(p) for p in progress])


@app.route('/api/bmi/<name>')
def calculate_bmi(name):
    db = get_db()
    client = db.execute('SELECT height, weight FROM clients WHERE name = ?', (name,)).fetchone()
    if not client or not client['height'] or not client['weight']:
        return jsonify({"error": "Height and weight required"}), 400
    
    height_m = client['height'] / 100
    bmi = round(client['weight'] / (height_m * height_m), 1)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return jsonify({"bmi": bmi, "category": category})


@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    data = request.get_json()
    weight = data.get('weight', 0)
    program_id = data.get('program')
    factor = PROGRAMS.get(program_id, {}).get('factor', 25)
    calories = int(weight * factor) if weight else 0
    return jsonify({'calories': calories})


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
