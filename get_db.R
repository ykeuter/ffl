library(dplyr)
library(RPostgreSQL)

getDb <- function() {
  src_postgres(dbname = "ffl",
               host = "localhost",
               port = 5432, user = "postgres", password = "7tiR9H0NR7Bq")
}