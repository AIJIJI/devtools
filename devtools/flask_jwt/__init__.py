'''
    Simple and fixed jwt auth
    modified from flask-jwt

    Last Update: 2018/10/08 14:35
'''

from datetime import datetime, timedelta
from functools import wraps
import jwt
from werkzeug.local import LocalProxy
from flask import (
    current_app,
    request,
    jsonify,
    _request_ctx_stack,
    abort,
)
from devtools.web import merge_fields


current_identity = LocalProxy(lambda: getattr(
    _request_ctx_stack.top, 'current_identity', None))

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])

CONFIG_DEFAULTS = {
    'JWT_AUTH_URL_RULE': '/auth',
    'JWT_AUTH_ENDPOINT': 'jwt',
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY_CLAIMS': ['signature', 'exp', 'nbf', 'iat'],
    'JWT_REQUIRED_CLAIMS': ['exp', 'iat', 'nbf']
}


def jwt_payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + timedelta(seconds=3600)
    nbf = iat + timedelta(seconds=0)
    identity = getattr(identity, 'id') or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}


def jwt_encode_handler(identity):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    payload = _jwt.jwt_payload_callback(identity)
    missing_claims = list(set(required_claims) - set(payload.keys()))

    if missing_claims:
        raise RuntimeError('Payload is missing required claims: %s' %
                           ', '.join(missing_claims))

    return jwt.encode(payload, secret, algorithm=algorithm)


def jwt_decode_handler(token):
    secret = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    leeway = timedelta(seconds=10)

    verify_claims = current_app.config['JWT_VERIFY_CLAIMS']
    required_claims = current_app.config['JWT_REQUIRED_CLAIMS']

    options = {
        'verify_' + claim: True
        for claim in verify_claims
    }

    options.update({
        'require_' + claim: True
        for claim in required_claims
    })

    return jwt.decode(token, secret, options=options, algorithms=[algorithm], leeway=leeway)


def request_handler():
    auth_header_value = request.headers.get('Authorization', None)
    auth_header_prefix = ['JWT', 'BARE']
    if not auth_header_value:
        return
    parts = auth_header_value.split()
    if parts[0].upper() not in auth_header_prefix:
        abort(401, 'Invalid JWT header: Unsupported authorization type')
    elif len(parts) == 1:
        abort(401, 'Invalid JWT header: Token missing')
    elif len(parts) > 2:
        abort(401, 'Invalid JWT header: Token contains spaces')
    return parts[1]


def auth_request_handler():
    data = merge_fields(request)
    username = data.get('username')
    password = data.get('password')

    if not all([username, password, len(data) == 2]):
        abort(422, 'Invalid credentials')

    identity = _jwt.authentication_callback(username, password)

    if identity:
        access_token = _jwt.jwt_encode_callback(identity)
        return _jwt.auth_response_callback(access_token, identity)
    else:
        abort(401, 'Invalid credentials')


def auth_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8')})


def _jwt_required():
    """
        Does the actual work of verifying the JWT data in the current request.
        This is done automatically for you by `jwt_required()`
        but you could call it manually. Doing so would be useful in the context
        of optional JWT access in your APIs.
    """
    token = _jwt.request_callback()

    if token is None:
        abort(401, 'Request does not contain an access token')
    try:
        payload = _jwt.jwt_decode_callback(token)
    except jwt.InvalidTokenError as e:
        abort(401, f'Invalid token: {str(e)}')

    _request_ctx_stack.top.current_identity = identity = \
        _jwt.identity_callback(payload)

    if identity is None:
        abort(401, 'Invalid JWT: User does not exist')


def jwt_required(fn):
    """
    View decorator that requires a valid JWT token to be present in the request
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if current_app.testing:
            return fn(*args, **kwargs)
        else:
            _jwt_required()
            return fn(*args, **kwargs)
    return decorated_function


class JWTError(Exception):
    def __init__(self, error, description, status_code=401, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'JWTError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)


def encode_token():
    return _jwt.encode_callback(_jwt.header_callback(), _jwt.payload_callback())


class JWT(object):

    def __init__(self, app=None, authentication_handler=None, identity_handler=None):
        self.authentication_callback = authentication_handler
        self.identity_callback = identity_handler
        self.auth_response_callback = auth_response_handler
        self.auth_request_callback = auth_request_handler
        self.jwt_encode_callback = jwt_encode_handler
        self.jwt_decode_callback = jwt_decode_handler
        self.jwt_payload_callback = jwt_payload_handler
        self.request_callback = request_handler

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in CONFIG_DEFAULTS.items():
            app.config.setdefault(k, v)
        app.config.setdefault('JWT_SECRET_KEY', app.config['SECRET_KEY'])

        auth_url_rule = app.config.get('JWT_AUTH_URL_RULE', None)

        if auth_url_rule:
            if self.auth_request_callback == auth_request_handler:
                assert self.authentication_callback is not None, (
                    'an authentication_handler function must be defined when using the built in '
                    'authentication resource')

            auth_url_options = app.config.get(
                'JWT_AUTH_URL_OPTIONS', {'methods': ['POST']})
            auth_url_options.setdefault(
                'view_func', self.auth_request_callback)
            app.add_url_rule(auth_url_rule, **auth_url_options)
            app.add_url_rule('/api/v1'+auth_url_rule, **auth_url_options)

        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}

        app.extensions['jwt'] = self
