from flask import Blueprint, jsonify, json, request
import os
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
from appsettings import Settings


users = Blueprint('users', __name__, static_folder='static', template_folder='templates')


@users.route('/userinfo', methods=['POST'])
def route_user_info():
    s = Settings()

    results = {
        'name': '',
        'admin': False,
        'user': False,
        'msg': ''
    }

    try:
        key = request.form['key']
        expected = s.get('api-key')
        if key != expected:
            return jsonify({}), 204

        username = request.form['identity'].lower()
    except Exception as e:
        return jsonify({}), 204

    ad_controller = s.get('ad_controller')
    ad_domain = s.get('ad_domain')
    ad_acct = s.get('ad_svc_acct')
    ad_acct_password = s.get('ad_svc_acct_pw')
    ad_admin_group = s.get('ad_admin_group')
    ad_user_group = s.get('ad_user_group')

    server = Server(ad_controller, get_info=ALL)
    searchstr = '(&(objectCategory=user)(objectClass=user)(mail=*)(cn = %s*))' % username

    conn = Connection(server, user='{}\\{}'.format(ad_domain, ad_acct), password=ad_acct_password, authentication=NTLM,
                      auto_bind=True)
    conn.search('dc={},dc=local'.format(ad_domain), searchstr,
                attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES], )

    groups = ''
    for e in conn.entries:
        try:
            if 'Person' in e.objectCategory[0]:
                if str(e.name).lower() == username or str(e.mail).lower() == username:
                    groups = str(e.memberOf)

            is_admin = False
            is_user = False

            if groups.__len__() > 0:
                if groups.__contains__(ad_admin_group):
                    is_admin = True
                    is_user = True
                elif groups.__contains__(ad_user_group):
                    is_user = True

            results['name'] = username
            results['admin'] = is_admin
            results['user'] = is_user
            return jsonify(results), 200
        except Exception as e:
            results['name'] = username
            results['msg'] = str(e)
            return jsonify(results), 500

