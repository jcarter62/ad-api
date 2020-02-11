from flask import Blueprint, jsonify, json, request
import subprocess
import os

users = Blueprint('users', __name__, static_folder='static', template_folder='templates')




@users.route('/users', methods=['POST'])
def route_users():
    try:
        key = request.form['key']
        expected = os.getenv('KEY')
        if key != expected:
            return jsonify({}), 204
    except Exception as e:
        return jsonify({}), 204

    cmd = "Get-ADUser -filter {(enabled -eq $true) -and (emailaddress -ne 'null')} " +\
        "-properties DisplayName, EmailAddress | " +\
        "select DisplayName, EmailAddress | ConvertTo-Json -Compress "

    pscmd = 'powershell "' + cmd + '"'

    proc = subprocess.Popen(pscmd, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('ASCII')
    result = json.loads(output)

    return jsonify({'users': result}), 200

