import psycopg2 as psql
from werkzeug.exceptions import abort

class Postgres():
	def __init__(self,connection_conf):
		self.db_name = connection_conf["db_name"] 
		self.user = connection_conf["user"]

	def _connect(self):
		return psql.connect(f"dbname={self.db_name} user={self.user}")

	def fetch(self,*query):
		try:
			with self._connect() as conn:
				with conn.cursor() as cur:
					cur.execute(*query)
					data = cur.fetchone()
			return data
		except:
			abort(500)
		finally:
			conn.close()

	def fetchall(self,*query):
		try:
			with self._connect() as conn:
				with conn.cursor() as cur:
					cur.execute(*query)
					data = cur.fetchall()
			return data
		except:
			abort(500)
		finally:
			conn.close()

	def execute(self,*query):
		try:
			with self._connect() as conn:
				with conn.cursor() as cur:
					cur.execute(*query)
		except:
			abort(500)
		finally:
			conn.close()
				

standard_connection = {"db_name" : "a24systeme", "user" : "postgres"}

class DBFactory():

	def __init__(self, Database=Postgres, conf=standard_connection):
		self.db = Database(conf)
		
	def start(self):
		return (self.db.execute, self.db.fetch, self.db.fetchall)


def build_schema(sql_file):
	execute, *_ = DBFactory().start()
	try: 
		execute(open(sql_file,"r").read())
		print("Esquema de dados criado com sucesso...")
	except: 
		print("Falha na criação do esquema de dados")
	





