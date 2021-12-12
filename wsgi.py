import cherrypy
import cherrypy_cors
import backend.database as database
import backend.webserver as server
import backend.card_reader as reader
import backend.models as models

debug = False
app = cherrypy.tree.mount(server.Freezy(), '/api/')
app.toolboxes['cors'] = cherrypy_cors.tools

if __name__ == '__main__':
    cherrypy.config.update({
        'cors.expose.on': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })

    try:
        reader.start(debug=debug)
        models.cache_data()
        cherrypy.quickstart(app)
    finally:
        database.close()
        print("closing db connection")