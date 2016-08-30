library(dplyr)

calcExpectedPoints <- function(roster) {
  STARTERS_PER_POS <- list(QB=1, RB=2, WR=2, TE=1, FLEX=1, D=1, K=1)
  NUM_WEEKS <- 17
  PLAY_RATE <- list(QB=.8, RB=.8, WR=.8, TE=.8, K=1)
 
}

calcOpportunityCost <- function(rosters, freeAgents, index, dir, maxPicks) {
  
}

getNextDraftPosition <- function(rosters, freeAgents, index, dir) {
  MAX_PER_POS <- list(QB=4, RB=8, WR=8, TE=3, D=3, K=3)
  
  cost <- vapply(names(MAX_PER_POS), function(p) {
    calcOpportunityCost(rosters, filter(freeAgents, position == p), index, dir, MAX_PER_POS[[p]])
  }, .0)
  
  return(names(MAX_PER_POS)[which.max(cost)])
}