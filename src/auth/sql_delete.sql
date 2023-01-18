-- -------------------------------------------------
-- DELETES the DATBASE and any created USERs
--
-- Run this SQL script from terminal: 
--   $ mysql --user=root --password=Tarmslyng_112 < sql_delete.sql
-- -------------------------------------------------

DROP USER 'auth_user@localhost';

DROP DATABASE auth;

COMMIT;
