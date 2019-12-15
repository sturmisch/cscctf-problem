from flask import request, render_template, render_template_string, Response
from selenium.webdriver import Chrome
from app import app

app.config['FLAG'] = "CCC{a_journ3y_into_dnssssti}"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Bye for Admin..')

@app.route('/action/<path:action>')
def action(action):
    ref = request.remote_addr
    if ref != "127.0.0.1":
        return"Sorry. No remote access are allowed."
    def sanitize(data):
        data = data.replace('(', '').replace(')', '')
        banning = ['self', 'config']
        return ''.join(['{{% set {}="Hohoho. Happy Holiday, hekel."%}}'.format(ban) for ban in banning]) + data
    return render_template_string(sanitize(action))
