import os
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
NAMESPACE = os.environ.get('NAMESPACE', 'default')
REFRESH_INTERVAL = os.environ.get('INTERVAL', 60)