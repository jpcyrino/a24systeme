from flask import Flask
from sys import exit
import a24s
from a24s.db import build_schema

if (__name__ == '__main__'):
	print("Criando o esquema de dados...")
	build_schema("schema.sql")
	exit()

app = Flask(__name__, instance_relative_config=True)
a24s.start(app)


