import os, config
from flask import Blueprint, render_template, redirect, request, jsonify, Response

site = Blueprint('site', __name__, template_folder='templates')

AUTH0_BASE_URL = 'https://' + os.getenv('CALLBACK_PATH')

@site.route('/')
def index():
    return render_template('index.html')

@site.route('/login')
def login():
    return redirect(AUTH0_BASE_URL)

@site.route('/callback')
def callback():
    return '''
        <div id="token"></div>
        <script>
            const token = window.location.href.split('=')[1].split('&')[0];
            console.log(token);
            window.location.href = "https://hiketn.herokuapp.com/auth?token=" + token;
        </script>
    '''

@site.route('/auth')
def get_token():
    token = request.args.get('token')

    if not token:
        return jsonify({
            'success': False,
            'error': 'Token is missing'
        })
    return jsonify({
        'success': True,
        'token': token,
        'token_type': 'Bearer'
    })