try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Consul',
    'author': 'Ben Belchak',
    'url': 'https://github.com/bbelchak/python-consul',
    'author_email': 'ben@belchak.com',
    'version': '0.1',
    'install_requires': ['nose', 'requests', 'simplejson'],
    'packages': ['consul'],
    'scripts': [],
    'name': 'python-consul',
}

setup(**config)