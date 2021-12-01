import cherrypy
import cherrypy_cors

from backend import core, models


class Freezy(object):

    @cherrypy.expose
    def index(self):
        return "Freezy backend API"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_drinks(self):
        # TODO return drinks
        return core.get_drinks_json()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_users(self):
        return core.get_users_json()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_current_user(self):
        return core.get_current_user().to_json() if core.get_current_user() else None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def purchase(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        elif cherrypy.request.method == 'POST':
            json_in = cherrypy.request.json

            unsafe_user_id = json_in['user_id']
            unsafe_total_price = json_in['total_price']
            unsafe_drinks: dict = json_in['drinks']

            current_user = core.get_current_user()
            if current_user and current_user.user_id == unsafe_user_id:
                if unsafe_drinks:
                    total = 0
                    for drink_index, amount in unsafe_drinks.items():
                        drink = models.get_drink_by_id(int(drink_index) + 1)
                        if drink:
                            total += drink.price * amount
                        else:
                            return {'error': 'drink not found', 'status': 'error', 'msg': 'hm.'}
                    if total == unsafe_total_price:
                        if current_user.credit - total >= -50:
                            core.purchase(current_user, total, unsafe_drinks)
                            return {'status': 'ok'}
                        else:
                            return {'error': 'not enough money', 'status': 'error',
                                    'msg': 'du kannst dein konto um maximal 50 geld überziehen'}
                    else:
                        return {'error': 'invalid price', 'status': 'error',
                                'msg': 'cheatet hier jemand?'}
            else:
                return {'error': 'invalid user', 'status': 'error', 'msg': 'okeee. was hast du gemacht?'}
        return {'error': 'invalid request'}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def logout(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        elif cherrypy.request.method == 'POST':
            json_in = cherrypy.request.json
            print(type(json_in))
            user_id = json_in.get('user_id')
            current_user = core.get_current_user()
            if current_user and user_id == current_user.user_id:
                core.logout()
                return {"status": "ok"}
