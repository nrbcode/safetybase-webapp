from os import environ
from safety_app import create_app # factory

app = create_app('config.ConfigRemoteDev')
print(f"Configured with db: {app.config.get('MONGODB_SETTINGS')['db']}")

@app.route('/')
def hello_world():
    return 'Hello, World!'

# *********************************************************

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

