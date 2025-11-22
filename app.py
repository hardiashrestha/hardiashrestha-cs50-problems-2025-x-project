from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from dotenv import load_dotenv
import requests
import random
import re

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///f1users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize database tables
with app.app_context():
    db.create_all()

API_SPORTS_KEY = os.getenv("API_SPORTS_KEY")
API_SPORTS_HOST = os.getenv("API_SPORTS_HOST")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
WEATHER_OPTIONS = ["Sunny", "Rain", "Cloudy", "Storm", "Windy", "Foggy"]

DRIVERS = [
    {"name": "Max Verstappen", "price": 10},
    {"name": "Lewis Hamilton", "price": 10},
    {"name": "Charles Leclerc", "price": 9},
    {"name": "Lando Norris", "price": 8},
    {"name": "George Russell", "price": 8},
    {"name": "Carlos Sainz", "price": 7},
    {"name": "Oscar Piastri", "price": 6},
    {"name": "Fernando Alonso", "price": 6},
    {"name": "Sergio Perez", "price": 6},
    {"name": "Lance Stroll", "price": 4},
    {"name": "Esteban Ocon", "price": 4},
    {"name": "Pierre Gasly", "price": 4},
    {"name": "Yuki Tsunoda", "price": 3},
    {"name": "Daniel Ricciardo", "price": 3},
    {"name": "Valtteri Bottas", "price": 3},
    {"name": "Zhou Guanyu", "price": 2},
    {"name": "Alex Albon", "price": 3},
    {"name": "Logan Sargeant", "price": 1},
    {"name": "Kevin Magnussen", "price": 2},
    {"name": "Nico Hulkenberg", "price": 2},
    {"name": "Oliver Bearman", "price": 2},
    {"name": "Jack Doohan", "price": 1}]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    trophies = db.Column(db.Integer, default=0)
    races = db.Column(db.Integer, default=0)
    drivers = db.Column(db.String(512), default="")

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def api_sports_get(endpoint, params=None):
    url = f"https://{API_SPORTS_HOST}/{endpoint}"
    headers = {
        "X-RapidAPI-Key": API_SPORTS_KEY,
        "X-RapidAPI-Host": API_SPORTS_HOST
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API-SPORTS error {response.status_code}: {response.text}")
        return None

def query_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an expert F1 racing manager bot. Respond as an AI opponent in an F1 manager game."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def parse_bot_setup(bot_text):
    try:
        wing = int(re.search(r'Wing:\s*([+-]?\d+)', bot_text).group(1))
        brake = int(re.search(r'Brake Balance:\s*([+-]?\d+)', bot_text).group(1))
        suspension = int(re.search(r'Suspension:\s*([+-]?\d+)', bot_text).group(1))
        tyre = re.search(r'Tyre:\s*(Soft|Medium|Hard|Wet|Intermediate)', bot_text, re.IGNORECASE).group(1).capitalize()
        laps_match = re.search(r'Laps:\s*(\d+)', bot_text)
        laps = int(laps_match.group(1)) if laps_match else None
        return {"wing": wing, "brake": brake, "suspension": suspension, "tyre": tyre, "laps": laps}
    except Exception as e:
        print("Parse error:", e)
        return None

def simulate_race(user, bot, weather, track):
    score = 0
    if abs(int(user["wing"])) < abs(int(bot["wing"])):
        score += 1
    if user["tyre"] == ("Wet" if weather == "Rain" else "Soft"):
        score += 1
    if int(user["suspension"]) > int(bot["suspension"]):
        score += 1
    if score >= 2:
        result = "You win!"
    elif score == 1:
        result = "It's a tie!"
    else:
        result = "Bot wins!"
    return result

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return render_template('register.html')
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if not username or not password:
                flash('Username and password are required')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def root():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('welcome.html')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    bot_response = ""
    weather = "Sunny"
    race_result = ""
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        if request.form.get("generate_weather") == "1":
            weather = random.choice(WEATHER_OPTIONS)
            return render_template('index.html', bot_response=bot_response, weather=weather, race_result=race_result, user=user)
        else:
            track = request.form.get('track')
            weather = request.form.get('weather')
            wing = request.form.get('wing')
            brake = request.form.get('brake')
            suspension = request.form.get('suspension')
            tyre = request.form.get('tyre')
            laps = request.form.get('laps')
            user_setup = (
                f"Track: {track}, Weather: {weather}. "
                f"My car setup is: Wing={wing}, Brake Balance={brake}, "
                f"Suspension={suspension}, Tyre={tyre}, Laps={laps}. "
                "Please reply with your setup as my opponent in this format: "
                "Wing: <value>, Brake Balance: <value>, Suspension: <value>, Tyre: <value>, Laps: <value>, "
                "and a brief strategy."
            )
            bot_response = query_deepseek(user_setup)
            bot_setup = parse_bot_setup(bot_response)
            user_dict = {"wing": wing, "brake": brake, "suspension": suspension, "tyre": tyre, "laps": laps}
            session['user_setup'] = user_dict
            session['bot_setup'] = bot_setup
            session['track'] = track
            session['weather'] = weather
            if bot_setup:
                race_result = simulate_race(user_dict, bot_setup, weather, track)
                user.races += 1
                if race_result == "You win!":
                    user.trophies += 1
                db.session.commit()
            else:
                race_result = "Could not parse bot setup. Please try again."
            session['race_result'] = race_result
            return redirect(url_for('pitstop'))
    return render_template('index.html', bot_response=bot_response, weather=weather, race_result=race_result, user=user)

@app.route('/pitstop', methods=['GET', 'POST'])
@login_required
def pitstop():
    user_setup = session.get('user_setup')
    bot_setup = session.get('bot_setup')
    track = session.get('track')
    weather = session.get('weather')
    race_result = session.get('race_result')
    pit_result = ""
    bot_pit_response = ""
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        new_tyre = request.form.get('tyre')
        new_wing = request.form.get('wing')
        new_brake = request.form.get('brake')
        new_suspension = request.form.get('suspension')
        user_setup.update({
            "tyre": new_tyre,
            "wing": new_wing,
            "brake": new_brake,
            "suspension": new_suspension
        })
        pit_prompt = (
            f"We are at a pit stop on {track} with {weather} weather. "
            f"My new setup is: Wing={new_wing}, Brake Balance={new_brake}, Suspension={new_suspension}, Tyre={new_tyre}. "
            "What changes do you make at your pit stop? Please reply in format: "
            "Wing: <value>, Brake Balance: <value>, Suspension: <value>, Tyre: <value>, and a brief reason."
        )
        bot_pit_response = query_deepseek(pit_prompt)
        new_bot_setup = parse_bot_setup(bot_pit_response)
        if new_bot_setup:
            bot_setup.update(new_bot_setup)
            session['user_setup'] = user_setup
            session['bot_setup'] = bot_setup
            return redirect(url_for('match'))
        else:
            pit_result = "Could not parse bot's pit stop setup. Please try again."
            return render_template('pitstop.html', user_setup=user_setup, bot_setup=bot_setup, bot_pit_response=bot_pit_response, pit_result=pit_result, user=user)
    return render_template('pitstop.html', user_setup=user_setup, bot_setup=bot_setup, bot_pit_response=bot_pit_response, pit_result=pit_result, user=user)

@app.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.order_by(User.trophies.desc(), User.races.desc()).limit(20).all()
    user = User.query.get(session['user_id'])
    return render_template('leaderboard.html', users=users, user=user)
@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)
@app.route('/match')
@login_required
def match():
    user_setup = session.get('user_setup')
    bot_setup = session.get('bot_setup')
    track = session.get('track')
    weather = session.get('weather')
    laps = int(user_setup.get('laps', 5))
    user = User.query.get(session['user_id'])

    bot_details = (
        f"Wing: {bot_setup['wing']}, "
        f"Brake Balance: {bot_setup['brake']}, "
        f"Suspension: {bot_setup['suspension']}, "
        f"Tyre: {bot_setup['tyre']}, "
        f"Laps: {bot_setup['laps'] if bot_setup.get('laps') else laps}"
    )

    lap_leaders = []
    user_score = 0
    bot_score = 0
    max_streak_length = 3
    current_streak = 0
    current_leader = random.choice(["user", "bot"])
    for lap in range(1, laps + 1):
        if current_streak == 0:
            current_leader = random.choice(["user", "bot"])
            current_streak = random.randint(1, max_streak_length)
        lap_leaders.append({"lap": lap, "leader": current_leader})
        if current_leader == "user":
            user_score += 1
        else:
            bot_score += 1
        current_streak -= 1

    if user_score > bot_score:
        final_result = "You win!"
        user.trophies += 1
    elif user_score < bot_score:
        final_result = "Bot wins!"
    else:
        final_result = "It's a tie!"
    user.races += 1
    db.session.commit()
    return render_template(
        'match.html',
        user_setup=user_setup,
        bot_setup=bot_setup,
        bot_details=bot_details,
        lap_leaders=lap_leaders,
        final_result=final_result,
        user=user,
        laps=laps,
        track=track,
        weather=weather
    )
@app.route('/f1/live')
def f1_live():
    standings = [
        {"position": 1, "driver": "Max Verstappen", "team": "Red Bull Racing", "points": 255},
        {"position": 2, "driver": "Lando Norris", "team": "McLaren", "points": 190},
        {"position": 3, "driver": "Charles Leclerc", "team": "Ferrari", "points": 172},
        {"position": 4, "driver": "Lewis Hamilton", "team": "Mercedes", "points": 160},
        {"position": 5, "driver": "Carlos Sainz", "team": "Ferrari", "points": 145},
        {"position": 6, "driver": "Oscar Piastri", "team": "McLaren", "points": 120},
        {"position": 7, "driver": "Sergio Perez", "team": "Red Bull Racing", "points": 110},
        {"position": 8, "driver": "George Russell", "team": "Mercedes", "points": 101},
        {"position": 9, "driver": "Fernando Alonso", "team": "Aston Martin", "points": 90},
        {"position": 10, "driver": "Lance Stroll", "team": "Aston Martin", "points": 52},
    ]
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('f1_live.html', standings=standings, user=user)

@app.route('/f1/history')
def f1_history():
    standings = [
        {"position": 1, "driver": "Max Verstappen", "nationality": "Dutch", "team": "Red Bull Racing", "points": 575},
        {"position": 2, "driver": "Sergio Perez", "nationality": "Mexican", "team": "Red Bull Racing", "points": 285},
        {"position": 3, "driver": "Lewis Hamilton", "nationality": "British", "team": "Mercedes", "points": 234},
        {"position": 4, "driver": "Fernando Alonso", "nationality": "Spanish", "team": "Aston Martin", "points": 206},
        {"position": 5, "driver": "Charles Leclerc", "nationality": "Monégasque", "team": "Ferrari", "points": 206},
        {"position": 6, "driver": "Lando Norris", "nationality": "British", "team": "McLaren", "points": 205},
        {"position": 7, "driver": "Carlos Sainz", "nationality": "Spanish", "team": "Ferrari", "points": 200},
        {"position": 8, "driver": "George Russell", "nationality": "British", "team": "Mercedes", "points": 175},
        {"position": 9, "driver": "Oscar Piastri", "nationality": "Australian", "team": "McLaren", "points": 97},
        {"position": 10, "driver": "Lance Stroll", "nationality": "Canadian", "team": "Aston Martin", "points": 74},
    ]
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('f1_history.html', standings=standings, user=user)
@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    user = User.query.get(session['user_id'])
    user_drivers = user.drivers.split(',') if user.drivers else []
    message = ""

    if request.method == 'POST':
        action = request.form.get('action')
        driver = request.form.get('driver')
        driver_obj = next((d for d in DRIVERS if d['name'] == driver), None)
        if not driver_obj:
            message = "Driver not found."
        elif action == "buy":
            if driver in user_drivers:
                message = "You already own this driver."
            elif user.trophies >= driver_obj['price']:
                user.trophies -= driver_obj['price']
                user_drivers.append(driver)
                message = f"Bought {driver}!"
            else:
                message = "Not enough trophies."
        elif action == "release":
            if driver in user_drivers:
                user_drivers.remove(driver)
                user.trophies += driver_obj['price']
                message = f"Released {driver}!"
            else:
                message = "You don't own this driver."
        user.drivers = ','.join(user_drivers)
        db.session.commit()

    return render_template(
        'transfer.html',
        user=user,
        user_drivers=user_drivers,
        drivers=DRIVERS,
        message=message
    )
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        old = request.form['old_password']
        new = request.form['new_password']
        if not check_password_hash(user.password_hash, old):
            flash('Old password incorrect.')
        elif len(new) < 4:
            flash('New password too short.')
        else:
            user.password_hash = generate_password_hash(new)
            db.session.commit()
            flash('Password changed successfully.')
            return redirect(url_for('index'))
    return render_template('change_password.html', user=user)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(session['user_id'])
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Account deleted.')
    return redirect(url_for('register'))
@app.route('/rename', methods=['GET', 'POST'])
@login_required
def rename():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        new_username = request.form['new_username'].strip()
        if not new_username:
            flash('Username cannot be empty.')
        elif User.query.filter_by(username=new_username).first():
            flash('Username already exists.')
        else:
            old_username = user.username
            user.username = new_username
            db.session.commit()
            session['username'] = new_username
            flash(f'Username changed from {old_username} to {new_username}.')
            return redirect(url_for('index'))
    return render_template('rename.html', user=user)
