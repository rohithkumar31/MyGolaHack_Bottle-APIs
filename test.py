import os
import time
import psycopg2
import urlparse
import hashlib
from bottle import Bottle

app = Bottle(__name__)
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

@app.route('/signup/<username>/<email>/<phone_no>/<passwd>')
def signup(username,email,phone_no,passwd):
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

@app.route('/login/<username>/<passwd>')
def signup(username,passwd):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = username
	var2 = passwd

	hash_object = hashlib.sha256(str(var2))
	new_passwd = str(hash_object.hexdigest())

	sql = "SELECT passwd FROM public.\"User\" WHERE username='"+str(var1)+"'"

	cur.execute(sql)

	res = cur.fetchone()
	res = str(res[0])

	if new_passwd == res :
		return "1"
	else :
		return "0"

@app.route('/new_poll/<p_user>/<p_name>/<p_location>')
def new_poll(p_user,p_name,p_location):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	image_url = "http://kqulo.com/poll_images/"

	cur = conn.cursor()

	var1 = p_user
	var2 = p_name
	var3 = p_location

	
	sql = "SELECT COUNT(*) FROM public.\"Polls\" WHERE p_user='"+str(var1)+"'"

	cur.execute(sql)

	res = cur.fetchone()
	res = res[0]

	p_id = str(var1)+"_"+str(res + 1)
	p_image = image_url+p_id+".jpg"

	os.environ['TZ'] = 'Asia/Calcutta'
	time.tzset()

	p_date = str(time.strftime("%d-%m-%Y"))
	p_time = str(time.strftime("%H:%M:%S"))

	sql = "INSERT INTO public.\"Polls\" VALUES ('"+p_id+"','"+str(var1)+"','"+str(var2)+"','"+str(p_location)+"','"+p_image+"',0,0,'"+p_date+"','"+p_time+"')"

	cur.execute(sql)

	conn.commit()
	cur.close()
	conn.close()

	return "Poll Inserted!! :-D"


	