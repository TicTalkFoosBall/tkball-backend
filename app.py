from flask import Flask, request, jsonify, make_response, session
from jinja2 import escape
from account import Account
import os


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.session_cookie_name = 'encryptCookie'
app.after_request(after_request)
accountManager = Account()


@app.route('/welcome')
@app.route('/')
def index():
    return "<h> hello </h>"


@app.route('/get')
def testGet():
    """
    ex: http://localhost:5000/get?name=ice
    """
    # name = escape(request.args.get('name'))
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('account')
    if name:
        return 'name = {}'.format(escape(name))
    else:
        return jsonify(msg='name为空', code='404'), 404


@app.route('/cookie')
def testCookie():
    # 未加密
    # response = make_response(redirect(url_for('index')))
    response = make_response()
    response.set_cookie('account', 'ice')

    # 加密
    session['encryptAccount'] = 'encryptIce'
    # session.pop('encryptAccount')
    # abort(403)
    return response


@app.route('/account/register/<string:accountnumber>/<string:password>')
def register(accountnumber, password):
    return accountManager.register(accountnumber, password)


@app.route('/account/login/<string:accountnumber>/<string:password>')
def login(accountnumber, password):
    return accountManager.login(accountnumber, password)


if __name__ == '__main__':
    app.run()

#
#
# custom cli
import click


@app.cli.command()
def sayHello():
    """
    just say hello
    """
    click.echo('hello')
