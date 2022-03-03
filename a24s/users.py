from .db import DBFactory
from uuid import uuid4, UUID
from psycopg2.extras import register_uuid
from werkzeug.exceptions import abort

user_column_names = (
	'id',
	'name',
	'registry',
	'period',
	'role',
	'access_key',
	'access_key_updated',
	'created'
	)

def query_insert_user(user_dict):
	query = """
			INSERT INTO users (id,name,registry,period,role,created) 
			VALUES (%s,%s,%s,%s,%s,%s);
			"""
	try:
		data = (
			str(uuid4()),
			user_dict['name'],
			user_dict['registry'],
			user_dict['period'],
			user_dict['role'],
			user_dict['created']
			)
	except:
		abort(400)

	return (query, data)

def exec_insert_user(user_dict):
	query, data = query_insert_user(user_dict)
	execute, *_ = DBFactory().start()
	execute(query,data)

def exec_insert_users(user_list):
	execute, *_ = DBFactory().start()
	for user in user_list:
		query, data = query_insert_user(user)
		execute(query,data)
		
def exec_get_user(user_id):
	register_uuid()
	if type(user_id) is not UUID:
		user_id = UUID(user_id)
	query = "SELECT * FROM users WHERE id=%s;"
	_, fetch, _ = DBFactory().start()
	data = fetch(query, (user_id, ))
	return dict(zip(user_column_names,data))

def exec_get_users():
	register_uuid()
	query = "SELECT * FROM users;"
	_, _, fetchall = DBFactory().start()
	data = fetchall(query)
	return [dict(zip(user_column_names,d)) for d in data]


