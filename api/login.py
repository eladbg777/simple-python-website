from bottle import get, post, route, request, response, view, template
from datastore import users
from data.config import Config


def check_login(db, username, password):
    row = db.execute('SELECT username, password from users where username=?', (username,)).fetchone()
    if row:
        return users.verify_hash(Config.config, password, row['password'])
    return False


#@view('login_result')
@post('/login')
def do_login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    name = None
    if check_login(db, username, password):
        name = users.get_user_name(db, username)
        cookie_content = {
            'username': username,
            'client-ip': request.remote_addr,
            'real-name': name
        }
        print('setting cookie')
        print(cookie_content)
        response.set_cookie("account", cookie_content, secret=Config.config.cookie_secret, max_age=10)
    else:
        username = None

    return template('login_result', dict(username=username, name=name))


@get('/login')
def login():
    return template('login_form')


@route('/restricted')
@view('restricted')
def restricted_area():
    cookie_content = request.get_cookie("account", secret=Config.config.cookie_secret)
    print('reading cookie')
    print(cookie_content)
    name = None
    client_ip = None
    username = None
    if cookie_content:
        username = cookie_content['username']
        client_ip = cookie_content['client-ip']
        name = cookie_content['real-name']

    return dict(name=name, username=username, ip=client_ip)

