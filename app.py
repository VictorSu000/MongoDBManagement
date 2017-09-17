import settings
import time
import os
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
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == settings.USERNAME and password == settings.PASSWORD:
            session['loggedin'] = True
            return redirect(url_for('manage'))
        else:
            abort(401)
    else:
        abort(405)


@app.route('/manage/')
@login_required
def manage():
    return render_template('manage.html')


@app.route('/migrate/', methods=['POST'])
@login_required
def migrate():
    if request.method == 'POST':
        js = request.form.get('migrationsjs', '')
        if js == '':
            abort(400)
        else:
            jsFileName = time.strftime(
                '%Y-%m-%d_%H:%M:%S', time.localtime(time.time())) +\
                '_ip:' + request.remote_addr
            jsFileFullPath = settings.MIGARTEJSSCRIPTBASEPATH + jsFileName
            with open(jsFileFullPath, 'w') as jsFile:
                jsFile.write(js)
            result = os.popen('source ' + settings.MIGRATEBASHSCRIPTPATH +
                              ' ' + settings.BACKUPBASEPATH +
                              ' ' + jsFileName)
        return result.read()
    else:
        abort(405)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG, host=settings.HOST, port=settings.PORT)
