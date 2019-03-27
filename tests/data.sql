-- u1:111
INSERT INTO users_tbl (username, password_hash)
VALUES
  ('test', 'pbkdf2:sha256:50000$qakQcWaJ$8ebd2584ddee684b0650b1433f5c3c7e85e4532d4b0d427227a7ca3cbdebd853'),
  ('u1', 'pbkdf2:sha256:50000$5oKY3UYR$5d8e2aa1d560c68471c2a69b480e665639a2ea3cddb426c0b532e73bc3501a64');

INSERT INTO posts_tbl (title, body, author_id, username, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1,  'u1', '2018-01-01 00:00:00');
