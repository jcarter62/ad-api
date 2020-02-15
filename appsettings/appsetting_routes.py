from flask import Blueprint, render_template, jsonify, redirect, request, g
from .settings import Settings

appsetting_routes = Blueprint('appsetting_routes', __name__, static_folder='static', template_folder='templates')


@appsetting_routes.route('/setup', methods=['GET', 'POST'])
def route_setup():
    if request.method == 'GET':
        settings = Settings()
        context = {
            'settings': settings.items
        }
        return render_template('setup.html', context=context)
    else:
        # Extract each item from form, and save back to settings.
        settings = Settings()
        for item in settings.items:
            formitem = request.form[item['name']]
            item['value'] = formitem
        settings.save_config()
        return redirect('/settings/setup')
