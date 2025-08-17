'''
the startup script to run on render
'''

from safety_app import create_app # factory

app = create_app('config.ConfigRemoteDev')
print(f"Configured with db: {app.config.get('MONGODB_SETTINGS')['db']}")

@app.route('/')
def hello_world():
    return 'Hello, World!'
