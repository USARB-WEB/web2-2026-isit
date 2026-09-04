-- Creates a dedicated database for the automated test suite so that running
-- pytest never touches (and never wipes) the learning_db development data.
CREATE DATABASE IF NOT EXISTS learning_test_db;
GRANT ALL PRIVILEGES ON learning_test_db.* TO 'learning_user'@'%';
FLUSH PRIVILEGES;
