from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from api.users import users
from appsettings.appsetting_routes import appsetting_routes

app = Flask(__name__)
app.register_blueprint(users, url_prefix='/api')
app.register_blueprint(appsetting_routes, url_prefix='/settings')
Bootstrap(app)


@app.route('/', methods=['POST'])
def hello_world():
    return jsonify({}), 204


if __name__ == '__main__':
    app.run()
