from .db import DBFactory
from .users import user_column_names
from .reviews import exec_create_review_for_fullfillment
from uuid import uuid4, UUID
from psycopg2.extras import register_uuid
from datetime import datetime
from werkzeug.exceptions import abort


fullfillment_columns = (
	"id",
	"assignment",
	"student",
	"content",
	"created",
	"updated"
	)

def exec_create_fullfillment(fullfillment_dict):
	register_uuid()
	query = """
			INSERT INTO fullfillment (id,assignment,student,content,created)
			VALUES (%s,%s,%s,%s,%s);
			"""
	fullfillment_id = uuid4()
	try: 
		data=(
			fullfillment_id,
			fullfillment_dict["assignment"],
			fullfillment_dict["student"]
			fullfillment_dict["content"],
			datetime.now()
			)
	except:
		abort(400)
	execute, *_ = DBFactory().start()
	execute(query,data)
	exec_create_review_for_fullfillment(fullfillment_id)
	return {"id": str(fullfillment_id)}

def exec_get_fullfillments():
	query = "SELECT * FROM fullfillment;"
	_, _, fetchall = DBFactory().start()
	response = fetchall(query)
	if response is None:
		return ('',204)
	return [dict(zip(fullfillment_columns,r)) for r in response]

def exec_get_fullfillments_by_user_id(user_id):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	query = "SELECT * FROM fullfillment WHERE student=%s;"
	data = (user_id, )
	_, _, fetchall = DBFactory().start()
	response = fetchall(query, data)
	if response is None:
		return ('',204)
	return [dict(zip(fullfillment_columns,r)) for r in response]

def exec_get_fullfillment(fullfillment_id):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	query = "SELECT * FROM fullfillment WHERE id = %s;"
	data = (fullfillment_id, )
	_,fetch,_ = DBFactory().start()
	response = fetch(query,data)
	if response is None:
		return ('',204)
	return dict(zip(fullfillment_columns,response))

def exec_delete_fullfillment(fullfillment_id):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	query = "DELETE FROM fullfillment WHERE id = %s;"
	data = (fullfillment_id, )
	execute, *_ = DBFactory().start()
	execute(query, data)
	return ('',204)

def exec_update_fullfillment(fullfillment_id, fullfillment_dict):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	updated = datetime.now()
	try:
		data=(
			fullfillment_dict["content"],
			updated,
			fullfillment_id
			)
	except:
		abort(400)
	query = """
			UPDATE fullfillment SET content=%s, updated=%s
			WHERE id = %s;
			"""
	execute, *_ = DBFactory().start()
	execute(query,data)
	return { "updated" : updated }