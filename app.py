from flask import Flask, jsonify
from api.users import users

app = Flask(__name__)
app.register_blueprint(users, url_prefix='/api')


@app.route('/', methods=['POST'])
def hello_world():
    return jsonify({}), 204


if __name__ == '__main__':
    app.run()
