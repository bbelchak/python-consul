import json
import requests
from consul.base import BaseAPI


class Agent(BaseAPI):
    endpoint = 'agent'

    def _make_url(self, path):
        return '{0}/{1}'.format(self._url, path)

    def checks(self):
        return requests.get(self._make_url('checks')).json()

    def services(self):
        return requests.get(self._make_url('services')).json()

    def members(self):
        return requests.get(self._make_url('members')).json()

    def join(self, address):
        return requests.get(self._make_url('join/{0}'.format(address))).json()

    def force_leave(self, node):
        requests.get(self._make_url('force-leave/{0}'.format(node)))

    def register_check(self, check_data):
        return requests.put(self._make_url('check/register'),
                            data=json.dumps(check_data))

    def deregister_check(self, check_id):
        url = self._make_url('check/deregister/{0}'.format(check_id))
        return requests.get(url)