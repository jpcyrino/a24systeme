@echo off
psql -U postgres -d postgres -c "DROP DATABASE a24systeme"
psql -U postgres -d postgres -c "CREATE DATABASE a24systeme"
psql -U postgres -d postgres -f schema.sql
echo "TUDO OK!"