-- Supprimer les dernières tables 
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS fullfillment;
DROP TABLE IF EXISTS assignment;
DROP TABLE IF EXISTS users;

-- Le schéma de données
CREATE TABLE users (
	id UUID NOT NULL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	registry INTEGER NOT NULL,
	period INTEGER NOT NULL,
	role VARCHAR(10) NOT NULL,
	access_key UUID,
	access_key_updated TIMESTAMP,
	created TIMESTAMP,
	UNIQUE(registry)
);

CREATE TABLE assignment (
	id UUID NOT NULL PRIMARY KEY,
	expiry DATE NOT NULL,
	active BOOLEAN NOT NULL,
	content TEXT,
	creator UUID REFERENCES users (id),
	created TIMESTAMP,
	updated TIMESTAMP,
	UNIQUE (creator)
);

CREATE TABLE fullfillment (
	id UUID NOT NULL PRIMARY KEY,
	assignment UUID REFERENCES assignment (id),
	student UUID REFERENCES users (id),
	content TEXT,
	created TIMESTAMP,
	updated TIMESTAMP
);

CREATE TABLE review (
	id UUID NOT NULL PRIMARY KEY,
	fullfillment UUID REFERENCES fullfillment (id),
	reviewer UUID REFERENCES users (id),
	content TEXT,
	grade INTEGER,
	created TIMESTAMP,
	sent BOOLEAN
);