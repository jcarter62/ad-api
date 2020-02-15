import copy
import json


class Defaults:

    def __init__(self):
        self.values = [
            {'name': 'appname', 'value': 'ad-api'},

            {'name': 'ad_controller', 'value': ''},
            {'name': 'ad_domain', 'value': ''},
            {'name': 'ad_svc_acct', 'value': ''},
            {'name': 'ad_svc_acct_pw', 'value': ''},
            {'name': 'ad_admin_group', 'value': ''},
            {'name': 'ad_user_group', 'value': ''},
        ]
        return

    def get(self, name):
        result = ''
        try:
            for v in self.values:
                if v['name'].lower() == name.lower():
                    result = v['value']
                    break
        except KeyError as e:
            result = str(e)

        return result


class Settings:

    def __init__(self):
        import copy
        defaults = Defaults()
        # make a non-referenced copy of the defaults.
        self.items = copy.deepcopy(defaults.values)
        self.load_config()

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), self.get('appname'))
        else:
            _data_folder = os.path.join(os.getenv('HOME'), self.get('appname'))

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings.json')
        return filename

    def load_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                self.items = json.load(f)
        except OSError as e:
            print(str(e))
        #
        # add any missing items
        #
        for i in Defaults().values:
            def_name = i['name']
            found = False
            for item in self.items:
                if item['name'] == def_name:
                    found = True
                    break
            if not found:
                new_item = {'name': i['name'], 'value': i['value']}
                self.items.append(new_item)
        # completed with adding missing items.

    def save_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'w') as output_file:
                json.dump(self.items, output_file)
        except Exception as e:
            print(str(e))

    def get(self, name: str = ''):
        result = ''
        for item in self.items:
            if name == item['name']:
                result = item['value']
                break
        return result

    def set(self, name: str = '', value: str = ''):
        item_found = False
        for item in self.items:
            if name == item['name']:
                item['value'] = value
                item_found = True
                break
        if not item_found:
            item = { 'name': name, 'value': value }
            self.items.append(item)

        return

    def __str__(self):
        return json.dumps(self.items)

