import os

from flask import Flask, render_template, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('login.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/enrollment')
    def enrollment():
        return render_template('enrollment.html')
    
    @app.route('/attendance')
    def attendance():
        return render_template('attendance.html')

    return app