import os

# Set environment variables
os.environ['DB_USER'] = 'your_db_user'
os.environ['DB_PASSWORD'] = 'your_db_password'
os.environ['DB_URI'] = 'your_db_uri'
os.environ['DB_NAME'] = 'your_db_name'

os.environ['AUTH0_CLIENT_ID'] = 'your_auth0_client_id'
os.environ['AUTH0_CLIENT_SECRET'] = 'your_auth0_client_secret'
os.environ['AUTH0_CALLBACK_URL'] = 'your_auth0_callback_url'
os.environ['AUTH0_DOMAIN'] = 'your_auth0_domain'
os.environ['AUTH0_AUDIENCE'] = 'your_auth0_audience'

os.environ['CALLBACK_PATH'] = '{}/authorize?audience={}&response_type=token&client_id={}&redirect_uri={}'.format(
        os.getenv('AUTH0_DOMAIN'),
        os.getenv('AUTH0_AUDIENCE'),
        os.getenv('AUTH0_CLIENT_ID'),
        os.getenv('AUTH0_CALLBACK_URL')
    )
