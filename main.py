from sqlite3 import IntegrityError

import flask
from flask import Flask, jsonify, request, Response
from flask.views import MethodView

from models import Session

from models import User

app = Flask('Flask_hm')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def get_user_by_id(author_id: int):
    author = request.session.query(User).get(author_id)
    if author is None:
        raise HttpError(404, 'user not found')
    return author


@app.errorhandler(HttpError)
def error_handler(error:HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "can't change or add tittle")


class UserView(MethodView):

    def get(self, author_id: int):
        author = get_user_by_id(author_id)
        return jsonify(author.create_dict)

    def post(self):
        data = request.json
        author = add_user(**data)
        return jsonify(author.create_dict)

    def patch(self, author_id: int):
        data = request.json
        author = get_user_by_id(author_id)
        for field, value in data.items():
            setattr(author, field, value)
        add_user(author)
        return jsonify(author.create_dict)

    def delete(self, author_id: int):
        author = get_user_by_id(author_id)
        request.session.delete(author)
        request.session.commit()
        return jsonify({'Complete': 'OK'})


user_view = UserView.as_view('user_view')

app.add_url_rule('/user', view_func=user_view, methods=['POST'])
app.add_url_rule('/user/<int:author_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
