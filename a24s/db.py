import psycopg2 as psql

class Postgres():
	def __init__(self,connection_conf):
		self.db_name = connection_conf["db_name"] 
		self.user = connection_conf["user"]
		self.connection = None

	def connect(self):
		if self.connection is None:
			try:
				self.connection = psql.connect(f"dbname={self.db_name} user={self.user}")
			except:
				# S'occuper des erreurs d'une manière meilleure
				return False
		return True

	def disconnect(self):
		if self.connection is not None:
			try:
				self.connection.close()
			except:
				# S'occuper des erreurs d'une manière meilleure
				return False
		return True

	def execute(self,*query):
		if self.connection is None:
			if not self.connect(): 
				return False
		with self.connection.cursor() as cur:
			try: 
				cur.execute(*query)
				self.connection.commit()
			except: 
				return False 
		return True


standard_connection = {"db_name" : "a24systeme", "user" : "postgres"}

class DBFactory():

	def __init__(self, Database=Postgres, conf=standard_connection):
		self.db = Database(conf)
		

	def start(self):
		try:
			self.db.connect()
			return (self.db.execute, self.db.disconnect)
		except:
			return False 


def build_schema(sql_file, Database=Postgres, conf=standard_connection):
	db = Database(conf)
	if db.connect():
		if db.execute(open(sql_file,"r").read()):
			print("Esquema de dados criado com sucesso...")
		else: 
			print("Falha na criação do esquema de dados")
	db.disconnect()





