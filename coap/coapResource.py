import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


log = logging.getLogger('coapResource')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

import coapException        as e
import coapDefines          as d
import coapObjectSecurity   as oscoap


class coapResource(object):

    def __init__(self, path):

        assert type(path) == str

        # store params
        self.path = path

        self.securityBinding = None
        self.get_callback = None
        self.put_callback = None
        self.post_callback = None
        self.delete_callback = None

    # ======================== abstract methods ================================

    def GET(self, options=[]):
        if not self.get_callback:
            raise e.coapRcMethodNotAllowed()
        self.get_callback(options)

    def PUT(self, options=[], payload=None):
        if not self.put_callback:
            raise e.coapRcMethodNotAllowed()
        self.put_callback(options, payload, self.topo)

    def POST(self, options=[], payload=None):
        if not self.post_callback:
            raise e.coapRcMethodNotAllowed()
        self.post_callback(options, payload)

    def DELETE(self, options=[]):
        if not self.delete_callback:
            raise e.coapRcMethodNotAllowed()
        delete_callback(options)

    def add_delete_cb(self, cb):
        self.delete_callback = cb

    def add_post_cb(self, cb):
        self.post_callback = cb

    def add_put_cb(self, cb):
        self.put_callback = cb

    def add_get_cb(self, cb):
        self.get_callback = cb

    def add_topo(self, topo):
        self.topo = topo

    # ======================== public ==========================================

    def matchesPath(self, pathToMatch):
        log.debug('"{0}" matches "{1}"?'.format(pathToMatch, self.path))
        temp_path = self.path.lstrip('/').rstrip('/')
        temp_pathToMatch = pathToMatch.lstrip('/').rstrip('/')
        if temp_path == temp_pathToMatch:
            return True
        else:
            return False

    def addSecurityBinding(self, binding):
        (ctx, authorizedMethods) = binding
        assert isinstance(authorizedMethods, list)
        for method in authorizedMethods:
            assert method in d.METHOD_ALL

        log.debug('adding security binding for resource={0}, context={1}, authorized methods={2}'.format(self.path,
                                                                                                         ctx,
                                                                                                         authorizedMethods))
        self.securityBinding = binding

    def getSecurityBinding(self):
        if self.securityBinding:
            return self.securityBinding
        else:
            # if no context is bound to the resource, all methods are authorized
            return (None, d.METHOD_ALL)
