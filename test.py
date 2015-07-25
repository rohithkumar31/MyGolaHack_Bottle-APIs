import os
import psycopg2
import urlparse
import hashlib
from bottle import Bottle

app = Bottle(__name__)
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

@app.route('/test')
def login():
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	sql = "SELECT * FROM public.\"User\""

	cur.execute(sql)

	records = cur.fetchall()

	return str(records)

@app.route('/signup/<username>/<email>/<phone_no>/<passwd>')
def login(username,email,phone_no,passwd):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = username
	var2 = email
	var3 = phone_no
	var4 = passwd

	hash_object = hashlib.sha256(str(var4))
	new_passwd = str(hash_object.hexdigest())

	sql = "INSERT INTO public.\"User\" VALUES ('"+str(var1)+"','"+str(var2)+"','"+str(var3)+"','"+new_passwd+"')"

	cur.execute(sql)

	conn.commit()
	cur.close()
	conn.close()

	return "1"