"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
from routes.util import URLGenerator
from webtest import TestApp,AppError
from datetime import datetime
import pylons.test
import logging
from nose.tools import raises
log = logging.getLogger(__name__)
__all__ = ['environ', 'url', 'TestController']
time_format = '%Y-%m-%d %H:%M:%SZ'
# Invoke websetup with the current config file
SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

environ = {}

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)
        self.from_date = datetime(1990,1,1).isoformat() + "Z"
        self.until_date = datetime.utcnow().isoformat()+"Z"
    @raises(AppError)
    def test_error(self):    	
		resp = self.app.get(url(controller='foo'))
		assert resp.headers['Content-Type'] == 'text/html'

