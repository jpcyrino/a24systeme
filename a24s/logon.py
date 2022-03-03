from .db import DBFactory
from .users import user_column_names
from uuid import uuid4, UUID
from psycopg2.extras import register_uuid
from datetime import datetime
from werkzeug.exceptions import abort


def create_access_key(registry, skip_check=False):
	register_uuid()
	if (not skip_check) and check_access_key_exists(registry):
		return False
	execute, *_ = DBFactory().start()
	access_key = uuid4()
	query = "UPDATE users SET access_key = %s, access_key_updated = %s WHERE registry = %s;"
	try:
		data = (access_key, datetime.now(), registry)
		execute(query, data)
		return access_key
	except: 
		abort(500)

def check_access_key_exists(registry):
	register_uuid()
	_, fetch, _ = DBFactory().start()
	query = "SELECT access_key FROM users WHERE registry = %s;"
	data = (registry, )
	try:
		response = fetch(query,data)
		if (response == (None, )) or (response is None):
			return False
		return True
	except:
		abort(500)

def get_user_by_access_key(access_key):
	register_uuid()
	if type(access_key) is not UUID:
		try: 
			access_key = UUID(access_key)
		except: 
			abort(400)
	_, fetch, _ = DBFactory().start()
	query = "SELECT * FROM users WHERE access_key = %s;"
	data = (access_key, )
	try:
		response = fetch(query, data)
		if response is None:
			return False
		return dict(zip(user_column_names, response))
	except:
		abort(500)


