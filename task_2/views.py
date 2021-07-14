from flask import request, jsonify, make_response
from app import app, db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from validator import validate
from schema import USER_CREATE, ADVERTISEMENT_CREATE, ADVERTISEMENT_EDIT
import jwt
import datetime
from functools import wraps
from models import User, Advertisement


@app.route('/')
def index():
    return "Welcome to advertise"


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY']
                           )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/v1/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []

    for user in users:
        user_data = {'public_id': user.public_id,
                     'username': user.username,
                     'email': user.email,
                     'password': user.password}
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/api/v1/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user_data = {'public_id': user.public_id,
                 'username': user.username,
                 'email': user.email,
                 'password': user.password}

    return jsonify({'user': user_data})


@app.route('/api/v1/user', methods=['POST'])
@validate('json', USER_CREATE)
@token_required
def create_user(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'],
                    email=data['email'],
                    password=hashed_password
                    )
    new_user.add()
    return jsonify({'message': 'New user created!'})


@app.route('/api/v1/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user.delete()
    return jsonify({'message': 'The user has been deleted!'})


@app.route('/api/v1/advertisement', methods=['GET'])
@token_required
def get_all_advertisements(current_user):
    advertisements = Advertisement.query.all()
    output = []

    for advertisement in advertisements:
        advertisement_data = {'id': advertisement.id,
                              'title': advertisement.title,
                              'slug': advertisement.slug,
                              'text': advertisement.text,
                              'user_id': advertisement.user_id
                              }
        output.append(advertisement_data)

    return jsonify({'advertisements': output})


@app.route('/api/v1/advertisement/<advertisement_id>', methods=['GET'])
@token_required
def get_one_advertisement(current_user, advertisement_id):
    advertisement = Advertisement.query.filter_by(id=advertisement_id).first()

    if not advertisement:
        return jsonify({'message': 'No advertisement found'})

    advertisement_data = {'id': advertisement.id,
                          'title': advertisement.title,
                          'slug': advertisement.slug,
                          'text': advertisement.text,
                          'user_id': advertisement.user_id
                          }
    return jsonify({'advertisement': advertisement_data})


@app.route('/api/v1/advertisement', methods=['POST'])
@validate('json', ADVERTISEMENT_CREATE)
@token_required
def create_advertisement(current_user):
    data = request.get_json()
    new_advertisement = Advertisement(title=data['title'],
                                      slug=data['slug'],
                                      text=data['text'],
                                      user_id=current_user.id
                                      )
    new_advertisement.add()
    return jsonify({'message': 'New advertisement created!'})


@app.route('/api/v1/advertisement/<advertisement_id>', methods=['PUT'])
@validate('json', ADVERTISEMENT_EDIT)
@token_required
def edit_advertisement(current_user, advertisement_id):
    advertisement = Advertisement.query.filter_by(id=advertisement_id).first()

    if not advertisement:
        return jsonify({'message': 'No advertisement found'})

    if advertisement.user_id == current_user.id:

        title = request.json['title']
        slug = request.json['slug']
        text = request.json['text']

        advertisement.title = title
        advertisement.slug = slug
        advertisement.text = text

        db.session.commit()
        return jsonify({'message': 'The advertisement has been edited!'})
    else:
        return jsonify({'message': 'Forbidden'}), 403


@app.route('/api/v1/advertisement/<advertisement_id>', methods=['DELETE'])
@token_required
def delete_advertisement(current_user, advertisement_id):
    advertisement = Advertisement.query.filter_by(id=advertisement_id).first()

    if not advertisement:
        return jsonify({'message': 'No advertisement found'})

    if advertisement.user_id == current_user.id:
        advertisement.delete()
        return jsonify({'message': 'The advertisement has been deleted!'})
    else:
        return jsonify({'message': 'Forbidden'}), 403
