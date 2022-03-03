from .db import DBFactory
from .users import user_column_names
from uuid import uuid4, UUID
from psycopg2.extras import register_uuid
from datetime import datetime
from werkzeug.exceptions import abort


def exec_create_assignment(assignment_dict):
	register_uuid()
	query = """
			INSERT INTO assignment (id,expiry,active,content,creator,created)
			VALUES (%s,%s,%s,%s,%s,%s);
			"""
	assignment_id = uuid4()
	try: 
		data=(
			assignment_id,
			assignment_dict["expiry"],
			False,
			assignment_dict["content"],
			assignment_dict["creator"],
			datetime.now()
			)
	except:
		abort(400)
	execute, *_ = DBFactory().start()
	execute(query,data)
	return {"id": str(assignment_id)}

assignment_columns = (
	"id",
	"expiry",
	"active",
	"content",
	"creator",
	"created",
	"updated"
	)

def exec_get_assignments():
	query = "SELECT * FROM assignment;"
	_, _, fetchall = DBFactory().start()
	response = fetchall(query)
	if response is None:
		return ('',204)
	return [dict(zip(assignment_columns,r)) for r in response]

def exec_get_assignment(assignment_id):
	register_uuid()
	if type(assignment_id) is not UUID:
		UUID(assignment_id)
	query = "SELECT * FROM assignment WHERE id = %s;"
	data = (assignment_id, )
	_,fetch,_ = DBFactory().start()
	response = fetch(query,data)
	if response is None:
		return ('',204)
	return dict(zip(assignment_columns,response))

def exec_delete_assignment(assignment_id):
	register_uuid()
	if type(assignment_id) is not UUID:
		UUID(assignment_id)
	query = "DELETE FROM assignment WHERE id = %s;"
	data = (assignment_id, )
	execute, *_ = DBFactory().start()
	execute(query, data)
	return ('',204)

def exec_update_assignment(assignment_id, assignment_dict):
	register_uuid()
	if type(assignment_id) is not UUID:
		UUID(assignment_id)
	updated = datetime.now()
	try:
		data=(
			assignment_dict["expiry"],
			assignment_dict["content"],
			updated,
			assignment_id
			)
	except:
		abort(400)
	query = """
			UPDATE assignment SET expiry=%s, content=%s, updated=%s
			WHERE id = %s;
			"""
	execute, *_ = DBFactory().start()
	execute(query,data)
	return { "updated" : updated }

def exec_activate_assignment(assignment_id, active=True):
	register_uuid()
	if type(assignment_id) is not UUID:
		UUID(assignment_id)
	updated = datetime.now()
	query = "UPDATE assignment SET active=%s,updated=%s WHERE id=%s;"
	data = (active, updated, assignment_id)
	execute, *_ = DBFactory().start()
	execute(query,data)
	return { "active": active, "updated" : updated }

