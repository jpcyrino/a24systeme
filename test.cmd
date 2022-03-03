curl ^
-H "Authorization: Bearer 0cdbe7fe-4bae-4b82-9f4a-4d8718c344a6" ^
-H "Content-Type: application/json" ^
-d "@test.json" ^
-X GET http://localhost:5000/assignments

curl ^
-H "Authorization: Bearer 0cdbe7fe-4bae-4b82-9f4a-4d8718c344a6" ^
-H "Content-Type: application/json" ^
-X GET http://localhost:5000/logon/0cdbe7fe-4bae-4b82-9f4a-4d8718c344a6