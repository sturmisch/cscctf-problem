from flask import request, render_template, Response
from selenium.webdriver import Firefox
from app import app
from pyvirtualdisplay import Display
import socket
import re
from urllib.parse import urlparse
import time

FLAG = "SG9ob2hvLiBIYXBweSBIb2xpZGF5Lg=="

def valid_target(url):
    ip = ""
    try:
        url = urlparse(url).netloc
        url = url.split(':')[0]
        ip = socket.gethostbyname(url)
        print("IP: ", ip)
    except Exception as e:
        print(e)
        return False
    for ban in ["localhost", "127.0.0.1", "::1", "0.0.0.0"]:
        if str(ip) == "127.0.0.1":
            return False
        if ban in url:
            return False
    return True

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Bye..')

@app.route('/snapshot', methods=['POST'])
def request_snapshot():
    url = request.form.get('url', "https://petircysec.com/")
    timeout = request.form.get('timeout', 3)

    if url == "":
        return "Oops, please check your input?", 400

    if not valid_target(url):
        return "Wow jimbo: %s" % FLAG, 400

    try:
        timeout = int(timeout)
    except Exception as e:
        timeout = 3

    # sanity check
    if timeout > 150: timeout = 30
    if timeout < 0: timeout = 3
    
    print("Start Sleeping #1")

    time.sleep(timeout)

    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = Firefox(service_log_path='/var/log/challenges/geckodriver.log')
    driver.set_window_position(0, 0)

    driver.set_page_load_timeout(20)
    driver.implicitly_wait(20)
    
    print("Sending GET request")
    driver.get(url)
    
    print("Start Sleeping #2")
    time.sleep(10)

    png = driver.get_screenshot_as_base64()
    driver.quit()
    display.stop()

    return Response(png, mimetype='application/base64')
