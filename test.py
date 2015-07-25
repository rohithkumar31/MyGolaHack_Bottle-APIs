import os
import psycopg2
import urlparse
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