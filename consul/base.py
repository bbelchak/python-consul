class BaseAPI(object):
    endpoint = None

    def __init__(self, host='localhost', port=8500, version='v1'):
        self._host = host
        self._port = port
        self._url = 'http://{0}:{1}/{2}/{3}'.format(
            self._host, self._port, version, self.endpoint)