CREATE TABLE "stock_portfolio" (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    users_id INTEGER NOT NULL,
       stock TEXT NOT NULL,
      shares INTEGER NOT NULL,
       price NUMERIC NOT NULL,
   timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY (users_id) REFERENCES users(id)
)