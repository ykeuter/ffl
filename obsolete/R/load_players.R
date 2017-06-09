library(dplyr)
library(RPostgreSQL)

source("R/utils.R")

db <- getDb()

teams <- tbl(db, sql("select * from team")) %>% collect()
positions <- tbl(db, sql("select * from position")) %>% collect()

PLAYER_FILES <- c("data/offense.csv", "data/kicker.csv")

q <- lapply(PLAYER_FILES, function(f) {
  data <- read.csv(f)
  
  teamId <- teams$id[match(data$Team, teams$team_name)]
  posId <- positions$id[match(data$Position, positions$position_name)]
  lapply(seq_along(teamId), function(i) {
    if (!is.na(teamId[i]) && !is.na(posId[i])) {
      dbGetQuery(db$con, sprintf("insert into player (player_name, team_id, position_id) values ('%s', '%s', '%s')", 
                                 escapeName(data$Player[i]), teamId[i], posId[i]))
    }
    else print(data$Player[i])
  })
})

dbDisconnect(db$con)