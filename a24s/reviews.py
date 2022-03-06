from .db import DBFactory
from .users import user_column_names
from uuid import uuid4, UUID
from psycopg2.extras import register_uuid
from datetime import datetime
from werkzeug.exceptions import abort

def _get_tutor_with_least_fullfillments_to_review():
	register_uuid()
	query = """
			SELECT count(reviewer), users.id FROM review
			FULL OUTER JOIN users ON review.reviewer=users.id
			WHERE NOT users.role='student'
			GROUP BY users.id ORDER BY count ASC;
			"""
	_, fetch, _ = DBFactory().start()
	response = fetch(query)
	if len(response) < 2:
		return ('', 204)
	return response[1]

def exec_create_review_for_fullfillment(fullfillment_id):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	reviewer_id = _get_tutor_with_least_fullfillments_to_review()
	review_id = uuid4()
	query = """
			INSERT INTO review (id,fullfillment,reviewer,created) 
			VALUES (%s, %s, %s,%s);
			"""
	data = (review_id,fullfillment_id,reviewer_id,datetime.now())
	execute, *_ = DBFactory().start()
	execute(query, data)
	return { "id": review_id }

def exec_update_review(review_id, review_dict):
	register_uuid()
	if type(review_id) is not UUID:
		UUID(review_id)
	query = """
			UPDATE review SET content=%s, grade=%s
			WHERE id=%s;
			"""
	try:
		data = (
			review_dict["content"],
			review_dict["grade"],
			review_id
			)
	except:
		abort(400)
	execute, *_ = DBFactory().start()
	execute(query, data)
	return { "id": review_id, "content": review_dict["content"], "grade": review_dict["grade"]}

review_column_names = (
	"id",
	"fullfillment",
	"reviewer",
	"content",
	"grade",
	"created",
	"sent"
	)

def exec_get_reviews_by_reviewer_id(reviewer_id):
	register_uuid()
	if type(reviewer_id) is not UUID:
		UUID(reviewer_id)
	query = "SELECT * FROM review WHERE reviewer=%s;"
	data = (reviewer_id, )
	_,_,fetchall = DBFactory().start()
	response = fetchall(query,data)
	if response is None:
		return ('',204)
	return [dict(zip(review_column_names,r)) for r in response]

def exec_get_review_by_fullfillment_id(fullfillment_id):
	register_uuid()
	if type(fullfillment_id) is not UUID:
		UUID(fullfillment_id)
	query = "SELECT * FROM review WHERE fullfillment=%s;"
	data = (fullfillment_id, )
	_,fetch,_ = DBFactory().start()
	response = fetch(query,data)
	if response is None:
		return ('',204)
	return dict(zip(review_column_names,response))

def exec_send_review(review_id):
	register_uuid()
	if type(review_id) is not UUID:
		UUID(review_id)
	query = "UPDATE review SET sent=%s WHERE id=%s;"
	data = (True, review_id)
	execute, *_ = DBFactory().start()
	execute(query,data)
	return { "id": review_id }

def exec_delete_review(review_id):
	register_uuid()
	if type(review_id) is not UUID:
		UUID(review_id)
	query = "DELETE review WHERE id=%s;"
	data = (review_id, )
	execute, *_ = DBFactory().start()
	execute(query,data)
	return ('',204)

def exec_get_reviews():
	query = "SELECT * FROM review;"
	_,_,fetchall = DBFactory().start()
	response = fetchall(query)
	if response is None:
		return ('',204)
	return [dict(zip(review_column_names,r)) for r in response]

def exec_get_review(review_id):
	register_uuid()
	if type(review_id) is not UUID:
		UUID(review_id)
	query = "SELECT * FROM review WHERE id=%s;"
	data = (review_id, )
	_, fetch, _ = DBFactory().start()
	response = fetch(query, data)
	if response is None:
		return ('', 204)
	return dict(zip(review_column_names, result))