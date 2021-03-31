import jwt
import os
import datetime


def generate_token(username, user_clinic):
    return jwt.encode({
                'user': username,
                'clinic': user_clinic,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            os.environ['API_SECRET'], algorithm="HS256")
