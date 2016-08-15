library(dplyr)
library(RPostgreSQL)

db <- src_postgres(dbname = "ffl",
                   host = "localhost",
                   port = 5432, user = "postgres", password = "7tiR9H0NR7Bq")

players <- tbl(db, sql("
                select *
                from player")) %>%
  collect()