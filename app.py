'''
the startup script to run on render
'''

from safety_app import create_app # factory

app = create_app('config.ConfigRemoteDev')
