# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb change handler class.

Created on August 18, 2011

@author: jpoyau
'''


class BaseChangeHandler(object):
    def _canHandle(self, change, database):
        """Handler subclass must implement. Returns True if the handler object can or
        wants to handle the change. Otherwise returns False."""
        raise NotImplementedError, "Implement me"
        
    def preRunSetup(self):
        """Method allow setup on the monitoring thread.  Derived class that needs to 
        setup object or data the must be on the running monitoring thread.  this will
        call once  in the monitor thread"""
        pass
        
    def _handle(self, change, database):
        """Pass the database, since the handler code will be running
        in the same process as the monitor"""
        raise NotImplementedError, "Implement me"
        
    def handle(self, change, database):
        if self._canHandle(change, database):
            self._handle(change, database)
