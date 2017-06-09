library(shiny)
library(shinydashboard)
library(RPostgreSQL)
library(magrittr)
library(dplyr)

source("utils.R")
source("optimization.R")

ui <- dashboardPage(
  dashboardHeader(disable=T),
  dashboardSidebar(disable=T),
  dashboardBody(
    fluidRow(column(width=4,
                    uiOutput("bestPick"),
                    uiOutput("index"),
                    selectInput("pick", "Choose player:", ""), 
                    actionButton("go", "Pick"),
                    uiOutput("freeAgents")),
             column(width=4, uiOutput("picks")),
             column(width=4, uiOutput("roster")))
  )
)

server <- function(input, output, session) {
  NUM_TEAMS <- 8
  MY_POS <- 7
  POSITIONS <- c("QB", "RB", "WR", "TE", "D", "K")
  
  db <- getDb()
  
  players <- tbl(db, sql(
    "select player_name, team_name, position_name as position, projected_points as points, bye_week
  from player
  join team on player.team_id = team.id
  join position on player.position_id = position.id
  union
  select team_name, team_name, 'D', projected_defense_points as points, bye_week
  from team
  where projected_defense_points is not null"
  )) %>% collect() %>%
    arrange(desc(points)) %>%
    mutate(id=paste(player_name, team_name, position, points, bye_week, sep="/"))
  
  dbDisconnect(db$con)
  
  bestPick <- getNextDraftPick(
    lapply(seq(NUM_TEAMS), function(i) dplyr::filter(players, FALSE)), players, 1, 1)$id
  
  updateSelectInput(session, "pick", choices=players$id, selected=bestPick)
  
  rv <- reactiveValues()
  rv$direction <- 1
  rv$index <- 1
  rv$freeAgents <- players
  rv$rosters <- lapply(seq(NUM_TEAMS), function(i) dplyr::filter(players, FALSE))
  rv$picks <- dplyr::filter(players, FALSE)
  rv$bestPick <- bestPick
  
  observe({
    req(input$go)
    isolate({
      pick <- dplyr::filter(rv$freeAgents, id == input$pick)
      rv$picks <- rbind(pick, rv$picks)
      rv$freeAgents <- dplyr::filter(rv$freeAgents, id != input$pick)
      rv$rosters[[rv$index]] <- rbind(rv$rosters[[rv$index]], pick)
      nextTurn <- getNextSnakeTurn(rv$index, rv$direction, NUM_TEAMS)
      rv$direction <- nextTurn$direction
      rv$index <- nextTurn$index
      rv$bestPick <- getNextDraftPick(rv$rosters, rv$freeAgents, rv$index, rv$direction)$id
      updateSelectInput(session, "pick", choices=rv$freeAgents$id, selected = rv$bestPick)
    })
  })
  
  output$roster <- renderUI({
    r <- rv$rosters[[MY_POS]]
    
    positions <- lapply(POSITIONS, function(p) {
      renderVector(p, dplyr::filter(r, position == p)$id)
    })
    args <- c(list(width=NULL, title="My roster"), positions)
    do.call(box, args)
  })
  
  output$bestPick <- renderUI({
    # browser()
    renderVector("Best pick", rv$bestPick)
  })
  
  output$index <- renderUI({
    # browser()
    renderVector("Index", rv$index)
  })
  
  output$freeAgents <- renderUI({
    renderVector("Free agents", rv$freeAgents$id)
  })
  
  output$picks <- renderUI({
    renderVector("Picks", rv$picks$id)
  })
}

shinyApp(ui, server)