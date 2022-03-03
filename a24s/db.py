import psycopg2 as psql

class Postgres():
	def __init__(self,connection_conf):
		self.db_name = connection_conf["db_name"] 
		self.user = connection_conf["user"]
		self.connection = None

	def connect(self):
		if self.connection is None:
			self.connection = psql.connect(f"dbname={self.db_name} user={self.user}")

	def fetch(self,*query):
		if self.connection is None:
			self.connect()
		with self.connection.cursor() as cur:
			cur.execute(*query)
			data = cur.fetchone()
		return data

	def fetchall(self,*query):
		if self.connection is None:
			self.connect()
		with self.connection.cursor() as cur:
			cur.execute(*query)
			data = cur.fetchall()
		return data

	def disconnect(self):
		if self.connection is not None:
			self.connection.close()

	def execute(self,*query):
		if self.connection is None:
			self.connect()
		with self.connection.cursor() as cur:
			cur.execute(*query)
			self.connection.commit()

standard_connection = {"db_name" : "a24systeme", "user" : "postgres"}

class DBFactory():

	def __init__(self, Database=Postgres, conf=standard_connection):
		self.db = Database(conf)
		

	def start(self):
		self.db.connect()
		return (self.db.execute, self.db.disconnect, self.db.fetch, self.db.fetchall)


def build_schema(sql_file, Database=Postgres, conf=standard_connection):
	db = Database(conf)
	if db.connect():
		if db.execute(open(sql_file,"r").read()):
			print("Esquema de dados criado com sucesso...")
		else: 
			print("Falha na criação do esquema de dados")
	db.disconnect()





