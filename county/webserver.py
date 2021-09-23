import cherrypy


class Freezy(object):
    @cherrypy.expose
    def index(self):
        return "Freezy backend API"

    # TODO more DB calls
    # TODO build api structure