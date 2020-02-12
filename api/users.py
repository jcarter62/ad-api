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
        "select DisplayName, EmailAddress, SamAccountName | ConvertTo-Json -Compress "

    pscmd = 'powershell "' + cmd + '"'

    proc = subprocess.Popen(pscmd, stdout=subprocess.PIPE)
    output = proc.stdout.read().decode('ASCII')
    result = json.loads(output)

    return jsonify({'users': result}), 200


@users.route('/user-groups', methods=['POST'])
def route_user_groups():
    valid_identity = False
    try:
        key = request.form['key']
        expected = os.getenv('KEY')
        if key != expected:
            return jsonify({}), 204
    except Exception as e:
        return jsonify({}), 204
        
    try:
        identity = request.form['identity']
        if identity > '':
            valid_identity = True
        
    except Exception as e:
        return jsonify({}), 204

    if not valid_identity:
        return jsonify({}), 204 
    
    cmd = "Get-ADPrincipalGroupMembership -Identity " +\
        identity + " | " +\
        "select name | ConvertTo-Json -Compress "

    pscmd = 'powershell "' + cmd + '"'

    try:
        proc = subprocess.Popen(pscmd, stdout=subprocess.PIPE)
        output = proc.stdout.read().decode('ASCII')
        result = json.loads(output)

        return jsonify({'groups': result}), 200
    except Exception as e:
        return jsonify({'exception': 'Error obtaining user groups.' }), 500

