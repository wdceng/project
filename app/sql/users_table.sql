CREATE TABLE "users" (
        id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
      hash TEXT NOT NULL
)