library(dplyr)
library(RPostgreSQL)

source("get_db.R")

data <- read.csv("data/schedule.csv")

db <- getDb()

lapply(seq_len(nrow(df)), function(i) {
  bye <- which(vapply(1:17, function(j) {
    data[[paste0("wk", j)]][i] == "BYE"
  }, TRUE))
  dbGetQuery(db$con, sprintf("
                  insert into team (id, name, bye_week) 
                  values ('%s', '%s', '%s', '%s', '%s')", 
                             i, data[["shark_name"]][i], bye))
})

dbDisconnect(db$con)