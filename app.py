from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aceest-fitness-secret-key'

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

# In-memory client storage
clients = []


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
        weight = request.form.get('weight', type=float)
        program_id = request.form.get('program')
        adherence = request.form.get('adherence', type=int, default=0)
        
        if not name or not program_id:
            flash('Name and Program are required', 'error')
            return redirect(url_for('client_profile'))
        
        # Calculate calories
        factor = PROGRAMS.get(program_id, {}).get('factor', 25)
        calories = int(weight * factor) if weight else 0
        
        client = {
            'name': name,
            'age': age,
            'weight': weight,
            'program': program_id,
            'program_name': PROGRAMS[program_id]['name'],
            'adherence': adherence,
            'calories': calories
        }
        clients.append(client)
        flash(f'Client {name} saved successfully! Adherence: {adherence}%', 'success')
        return redirect(url_for('client_profile'))
    
    return render_template('client.html', programs=PROGRAMS)


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


@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    data = request.get_json()
    weight = data.get('weight', 0)
    program_id = data.get('program')
    factor = PROGRAMS.get(program_id, {}).get('factor', 25)
    calories = int(weight * factor) if weight else 0
    return jsonify({'calories': calories})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
