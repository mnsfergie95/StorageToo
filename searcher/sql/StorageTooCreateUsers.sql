--
--  Create users
--
CREATE user 'stoadmin'@'localhost' IDENTIFIED BY 'jikl1234';
CREATE user 'stouser'@'localhost' IDENTIFIED BY 'jikl1234';

--
--  Grant privileges
--

--
--  admin
--

GRANT ALL PRIVILEGES ON storagetoo.* TO 'stoadmin'@'localhost';

--
--  user
--

GRANT SELECT, INSERT, UPDATE, DELETE ON storagetoo.lessee TO 'stouser'@'localhost';
GRANT SELECT ON storagetoo.sizes TO 'stouser'@'localhost';
GRANT SELECT ON storagetoo.unit TO 'stouser'@'localhost';
GRANT SELECT ON storagetoo.pricing TO 'stouser'@'localhost';
GRANT SELECT, INSERT ON storagetoo.payment TO 'stouser'@'localhost';
GRANT SELECT ON storagetoo.users TO 'stouser'@'localhost';
GRANT SELECT, UPDATE ON storagetoo.login_attempts TO 'stouser'@'localhost';

FLUSH PRIVILEGES;

