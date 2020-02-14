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


@users.route('/userinfo', methods=['POST'])
def route_user_info():
    result = {
        'authenticated': False,
        'parceldocs': False,
        'parceldocs-admin': False,
        'user': {}
    }

    try:
        key = request.form['key']
        expected = os.getenv('KEY')
        if key != expected:
            return jsonify({}), 204

        username = request.form['identity'].lower()
    except Exception as e:
        return jsonify({}), 204

    cmd = "Get-ADUser -filter {(enabled -eq $true) -and (emailaddress -ne 'null')} " +\
        "-properties DisplayName, EmailAddress | " +\
        "select DisplayName, EmailAddress, SamAccountName | ConvertTo-Json -Compress "

    pscmd = 'powershell "' + cmd + '"'

    proc = subprocess.Popen(pscmd, stdout=subprocess.PIPE)
    users = json.loads(proc.stdout.read().decode('ASCII'))
    thisuser = None
    for user in users:
        if is_in_user_record(username, user):
            thisuser = user
            result['user'] = user
            result['authenticated'] = True
            break

    if thisuser is None:
        return jsonify({}), 204

    identity = thisuser['SamAccountName']

    cmd = "Get-ADPrincipalGroupMembership -Identity " +\
        identity + " | " +\
        "select name | ConvertTo-Json -Compress "

    pscmd = 'powershell "' + cmd + '"'

    try:
        proc = subprocess.Popen(pscmd, stdout=subprocess.PIPE)
        groups = json.loads(proc.stdout.read().decode('ASCII'))

        isuser = False
        isadmin = False
        for group in groups:
            if group['name'].lower() == 'parceldocs':
                isuser = True
            elif group['name'].lower() == 'parceldocs-admin':
                isadmin = True

        result['parceldocs'] = (isuser or isadmin)
        result['parceldocs-admin'] = isadmin

    except Exception as e:
        return jsonify({'exception': 'Error obtaining user groups.'}), 500

    return jsonify(result), 200


def is_in_user_record(name, rec):
    result = False
    if not rec['DisplayName'] is None:
        if rec['DisplayName'].lower() == name:
            result = True

    if not rec['EmailAddress'] is None:
        if rec['EmailAddress'].lower() == name:
            result = True

    if not rec['SamAccountName'] is None:
        if rec['SamAccountName'].lower() == name:
            result = True

    return result

