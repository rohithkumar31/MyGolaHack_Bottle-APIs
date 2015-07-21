import os
from bottle import Bottle

app = Bottle(__name__)

@app.route('/')
def hello():
	return "Hello Polling Cube!!"