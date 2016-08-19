library(dplyr)
library(RPostgreSQL)

source("get_db.R")

NWEEKS <- 17
BYE_STR <- "BYE"
FREE_AGENT_STR <- "FA"
SCHEDULE_FILE <- "data/schedule.csv"

data <- read.csv(SCHEDULE_FILE)

db <- getDb()

q <- lapply(seq_len(nrow(data)), function(i) {
  bye <- which(vapply(seq_len(NWEEKS), function(j) {
    data[[paste0("wk", j)]][i] == BYE_STR
  }, TRUE))
  dbGetQuery(db$con, sprintf("insert into team (team_name, bye_week) values ('%s', '%s')", 
                             data[["db_team_name"]][i], bye))
})
dbGetQuery(db$con, sprintf("insert into team (team_name) values ('%s')", FREE_AGENT_STR))

teams <- tbl(db, sql("select * from team")) %>% collect()

homeId <- teams$id[match(data$db_team_name, teams$team_name)]
q <- lapply(seq_len(NWEEKS), function(i) {
  visitingId <- homeId[match(data[[paste0("wk", i)]], data$team)]
  lapply(seq_along(homeId), function(j) {
    if (!is.na(visitingId[j])) {
      dbGetQuery(db$con, sprintf("insert into game (home_team_id, visiting_team_id, season_week) 
                                 values ('%s', '%s', '%s')", 
                                 homeId[j], visitingId[j], i))
    }
  })
})

dbDisconnect(db$con)