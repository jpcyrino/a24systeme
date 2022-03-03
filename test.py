from a24s.users import exec_insert_users

J = {
	'name': 'João Paulo Lazzarini Cyrino', 
	'registry': 202218,
	'period': 20221, 
	'role': 'admin', 
	'created': '2022-03-02'
	}

E = {
	'name': 'Eudes Barletta Mattos', 
	'registry': 202202,
	'period': 20221, 
	'role': 'tutor', 
	'created': '2022-03-02'
	}

L = {
	'name': 'Larissa Santos', 
	'registry': 202212,
	'period': 20221, 
	'role': 'tutor', 
	'created': '2022-03-02'
	}

exec_insert_users([J,E,L])

