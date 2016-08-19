library(dplyr)
library(RPostgreSQL)

source("get_db.R")
source("escape_name.R")

db <- getDb()

teams <- tbl(db, sql("select * from team")) %>% collect()
players <- tbl(db, sql("select * from player")) %>% collect()
positions <- tbl(db, sql("select * from position")) %>% collect()

PLAYER_FILES <- c("data/offense.csv", "data/kicker.csv")

q <- lapply(PLAYER_FILES, function(f) {
  data <- read.csv(f)
  
  teamId <- teams$id[match(data$Team, teams$team_name)]
  posId <- positions$id[match(data$Position, positions$position_name)]
  lapply(seq_along(teamId), function(i) {
    idx <- players$team_id == teamId[i] & 
      players$position_id == posId[i] & 
      players$player_name == escapeName(data$Player[i])
    if (sum(idx) == 0) print(data$Player[i])
    else {
      dbGetQuery(db$con, sprintf("update player set projected_points = %s where id = %s", 
                                 data$Pts[i], players$id[idx]))
    }
  })
})

DEFENSE_FILE <- "data/defense.csv"

data <- read.csv(DEFENSE_FILE)

teamId <- teams$id[match(data$Team, teams$team_name)]
lapply(seq_along(teamId), function(i) {
  if (!is.na(teamId[i])) {
    dbGetQuery(db$con, sprintf("update team set projected_defense_points = %s where id = %s", 
                               data$Pts[i], teamId[i]))
  }
  else print(data$Player[i])
})

dbDisconnect(db$con)