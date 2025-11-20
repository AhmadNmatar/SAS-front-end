import os
import requests
import functools

from flask import Flask, render_template, url_for, request, redirect, session, jsonify, send_file
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),

    )
    BACKEND_URL= os.getenv("BACKEND_URL")
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if not session.get("access_token"):
                return redirect(url_for("login"))
            return view(**kwargs)
        return wrapped_view

    @app.route('/')
    def home():
        admin = session.get('admin')
        if not admin:
            return render_template('login.html')
        return redirect(url_for("dashboard"))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "GET":
            try:
                return render_template("login.html")
            except Exception as e:
                app.logger.exception("Template render error")
                return f"Template render error: {e}", 500
        
        if not BACKEND_URL:
            return render_template("login.html", error="Server misconfigured: BACKEND_URL is missing."), 500

        username = request.form.get("username")
        password = request.form.get("password")

        try:
            resp = requests.post(
                f"{BACKEND_URL}/admin/login",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
        except requests.RequestException:
            return render_template("login.html", error="Backend unreachable"), 503

        if resp.status_code != 200:
            return render_template("login.html", error="Invalid credentials"), 401

        data = resp.json()

        session["access_token"] = data.get("access_token")
        session["admin"] = data.get("admin")
        return redirect(url_for("dashboard"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/enrollment')
    @login_required
    def enrollment():
        return render_template('enrollment.html')
    
    @app.route('/enroll', methods=['POST'])
    @login_required
    def enroll():
        if not BACKEND_URL:
            return render_template("login.html", error="Server misconfigured: BACKEND_URL is missing."), 500

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        try:
            resp = requests.post(
                f"{BACKEND_URL}/attendance/enroll_camera",
                json={"first_name": first_name, "last_name": last_name},
            )
        except requests.RequestException as e:
            return render_template("enrollment.html", message=str(e)), 503
        if resp.status_code != 200:
            return render_template("enrollment.html", message="field to enroll"), 401
        
        data = resp.json()

        return render_template("enrollment.html", message=data["message"])

    
    @app.route('/attendance')
    @login_required
    def attendance():
        BACKEND_URL = os.getenv("BACKEND_URL")
        print(BACKEND_URL)
        access_token = session.get("access_token")
        return render_template('attendance.html', backend_url=BACKEND_URL, access_token=access_token)

    return app