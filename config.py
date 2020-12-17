import os

# Set environment variables
os.environ['DB_USER'] = 'ovepfsvxwtngti'
os.environ['DB_PASSWORD'] = '2b53033dc8588ef3829bbe579e1f3c5fef8f969c795ec61f9927b5bb650e06ca'
os.environ['DB_URI'] = 'ec2-18-233-207-22.compute-1.amazonaws.com:5432'
os.environ['DB_NAME'] = 'd8tem6ngbp77em'

os.environ['AUTH0_CLIENT_ID'] = 'W6nH6vK5zg9TveeDZQaAP8tybGrEeP3d'
os.environ['AUTH0_CLIENT_SECRET'] = 'CLN1xPvWGta_Txr0nqN7jyrk8n4KXm8tB3RgPqN_U-tvwafZMMvGXgfNS8Zy1abZ'
os.environ['AUTH0_CALLBACK_URL'] = 'http://localhost:5000/callback'
os.environ['AUTH0_DOMAIN'] = 'strudev-tn.eu.auth0.com'
os.environ['AUTH0_AUDIENCE'] = 'HikeTNAPI'

os.environ['CALLBACK_PATH'] = '{}/authorize?audience={}&response_type=token&client_id={}&redirect_uri={}'.format(
        os.getenv('AUTH0_DOMAIN'),
        os.getenv('AUTH0_AUDIENCE'),
        os.getenv('AUTH0_CLIENT_ID'),
        os.getenv('AUTH0_CALLBACK_URL')
    )