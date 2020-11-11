import os

PROJECT_PATH = os.path.dirname(__file__)
os.makedirs(os.path.join(PROJECT_PATH, 'logs'), exist_ok=True)

port = os.environ.get('CUSTOM_PORT', '11563')

bind = "{host}:{port}".format(host='127.0.0.1', port=int(port))

workers = 1
# worker_class = 'eventlet'
proc_name = "darioCV"
errorlog = os.path.join(PROJECT_PATH, 'logs', 'gerror.log')
accesslog = os.path.join(PROJECT_PATH, 'logs', 'gaccess.log')
