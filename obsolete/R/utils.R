library(dplyr)
library(RPostgreSQL)

getDb <- function() {
  src_postgres(dbname = "ffl",
               host = "localhost",
               port = 5432, user = "postgres", password = "7tiR9H0NR7Bq")
}

escapeName <- function(name) {
  gsub("'", " ", name)
}

getNextSnakeTurn <- function(index, direction, size) {
  index <- index + direction
  if (index < 1) {
    index <- 1
    direction <- -direction
  } else if (index > size) {
    index <- size
    direction <- -direction
  }
  return(list(index=index, direction=direction))
}

removeFirst <- function(df, num=1) {
  if (nrow(df) <= num) return(dplyr::filter(df, FALSE))
  else return(slice(df, (num + 1):nrow(df)))
}

renderVector <- function(title, v) {
  lst <- do.call(c, lapply(v, function(e) list(e, br())))
  args <- c(list(title=title, width=NULL), lst)
  do.call(box, args)
}
