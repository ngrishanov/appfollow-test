CREATE TABLE posts (
  id INTEGER UNIQUE,
  title TEXT,
  url TEXT,
  created TIMESTAMPTZ
)