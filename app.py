import settings
from flask import Flask, render_template, \
    session, redirect, url_for, request, abort
from functools import wraps

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loggedin = session.get('loggedin', False)
        if not loggedin:
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)
    return wrapper


@app.route('/')
def main():
    loggedin = session.get('loggedin', False)
    if not loggedin:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('manage'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.methods == 'GET':
        return render_template('login.html')
    elif request.methods == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == settings.USERNAME and password == settings.PASSWORD:
            session['loggedin'] = True
        else:
            abort(401)
    else:
        abort(405)


@app.route('/manage/')
@login_required
def manage():
    return render_template('manage.html')


if __name__ == '__main__':
    app.run(debug=settings.DEBUG, host=settings.HOST, port=settings.PORT)
