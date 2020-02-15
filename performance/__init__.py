import datetime


class Performance:

    def __init__(self, module, func):
        self.mod = module
        self.func = func

    def msg(self):
        return self.mod + ':' + self.func + ':'

    def output(self, msg):
        print('%s - %s : %s' % (self.msg(), msg, datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S") ))

    def start(self):
        self.output('start')

    def end(self):
        self.output('end')

    def log(self, msg):
        self.output(msg)
