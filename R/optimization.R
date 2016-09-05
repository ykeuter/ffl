calcExpectedPoints <- function(roster) {
  # STARTERS_PER_POS <- list(QB=1, RB=2, WR=2, TE=1, FLEX=1, D=1, K=1)
  # NUM_WEEKS <- 17
  # browser()
  roster <- dplyr::arrange(roster, desc(points))
  
  qb <- calcExpectedSlotPoints(dplyr::filter(roster, position == "QB"))
  rb1 <- calcExpectedSlotPoints(dplyr::filter(roster, position == "RB"))
  rb2 <- calcExpectedSlotPoints(removeFirst(dplyr::filter(roster, position == "RB")))
  wr1 <- calcExpectedSlotPoints(dplyr::filter(roster, position == "WR"))
  wr2 <- calcExpectedSlotPoints(removeFirst(dplyr::filter(roster, position == "WR")))
  te <- calcExpectedSlotPoints(dplyr::filter(roster, position == "TE"))
  def <- calcExpectedSlotPoints(dplyr::filter(roster, position == "D"))
  kick <- calcExpectedSlotPoints(dplyr::filter(roster, position == "K"))
  
  players <- rbind(
    removeFirst(dplyr::filter(roster, position == "RB"), 2),
    removeFirst(dplyr::filter(roster, position == "WR"), 2),
    removeFirst(dplyr::filter(roster, position == "TE"), 1)
  ) %>%
    arrange(desc(points))
  flex <- calcExpectedSlotPoints(players)
 
  return(qb + rb1 + rb2 + wr1 + wr2 + te + def + kick + flex)
}

calcExpectedSlotPoints <- function(players) {
  PLAY_RATE <- list(QB=.8, RB=.5, WR=.5, TE=.5, K=.7, D=.7)
  
  if (nrow(players) == 0) return(0)
  
  weights1 <- vapply(players$position, function(p) PLAY_RATE[[p]], .0)
  weights2 <- Reduce(function(x, y) x - x * (1 - y), (1 - weights1), accumulate = TRUE)
  weights2 <- c(1, weights2[-length(weights2)])
  weights <- weights2 * weights1
  # print(weights)
  
  return(sum(weights * players$points))
}

distributeAgents <- function(pos, freeAgents, rosters, index, direction) {
  # MAX_PER_POS <- list(QB=4, RB=8, WR=8, TE=3, D=3, K=3)
  MAX_PER_POS <- list(QB=0, RB=0, WR=0, TE=0, D=0, K=0)
  
  maxPicks <- MAX_PER_POS[[pos]]
  
  freeAgents <- dplyr::filter(freeAgents, position == pos) %>%
    dplyr::arrange(dplyr::desc(points))
  
  while (!all(vapply(rosters, function(r) sum(r$position == pos) >= maxPicks, TRUE)) && 
          nrow(freeAgents) != 0) {
    if (sum(rosters[[index]]$position == pos) < maxPicks) {
      r <- rosters[[index]]
      r <- rbind(r, dplyr::slice(freeAgents, 1))
      freeAgents <- removeFirst(freeAgents)
      rosters[[index]] <- r
    }
    nextTurn <- getNextSnakeTurn(index, direction, length(rosters))
    index <- nextTurn$index
    direction <- nextTurn$direction
  }
  return(rosters)
}

calcOpportunityCost <- function(pos, freeAgents, rosters, index, direction) {
  # browser()
  rosters1 <- distributeAgents(pos, freeAgents, rosters, index, direction)
  
  nextTurn <- getNextSnakeTurn(index, direction, length(rosters))
  index2 <- nextTurn$index
  direction2 <- nextTurn$direction
  rosters2 <- distributeAgents(pos, freeAgents, rosters, index2, direction2)
  
  if (pos == 'K') {
    print(filter(rosters1[[index]], position == 'K'))
    print(filter(rosters2[[index]], position == 'K'))
  }
  
  return(calcExpectedPoints(rosters1[[index]]) - calcExpectedPoints(rosters2[[index]]))
}

getNextDraftPosition <- function(rosters, freeAgents, index, dir) {
  POSITIONS <- c("QB", "RB", "WR", "TE", "D", "K")
  
  cost <- vapply(POSITIONS, function(p) {
    calcOpportunityCost(p, freeAgents, rosters, index, dir)
  }, .0)
  
  print(cost)
  
  return(POSITIONS[which.max(cost)])
}

getNextDraftPick <- function(rosters, freeAgents, index, dir) {
  # browser()
  pos <- getNextDraftPosition(rosters, freeAgents, index, dir)
  pick <- dplyr::filter(freeAgents, position == pos) %>%
    dplyr::arrange(desc(points)) %>%
    slice(1)
  return(pick)
}










