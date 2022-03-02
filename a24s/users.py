from .db import DBFactory
from uuid import uuid4

def query_insert_user(user_dict):
	query = """
			INSERT INTO users (id,name,registry,period,role,created) 
			VALUES (%s,%s,%s,%s,%s,%s);
			"""

	data = (
		str(uuid4()),
		user_dict['name'],
		user_dict['registry'],
		user_dict['period'],
		user_dict['role'],
		user_dict['created']
		)

	return (query, data)



def exec_insert_user(user_dict):
	query, data = query_insert_user(user_dict)
	execute, disconnect = DBFactory().start()
	execute(query,data)
	disconnect()

def exec_insert_users(user_list):
	execute, disconnect = DBFactory().start()
	for user in user_list:
		query, data = query_insert_user(user)
		execute(query,data)
	disconnect()




