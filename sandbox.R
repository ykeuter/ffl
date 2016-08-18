library(dplyr)
library(RPostgreSQL)

db <- src_postgres(dbname = "ffl",
                   host = "localhost",
                   port = 5432, user = "postgres", password = "7tiR9H0NR7Bq")

players <- tbl(db, sql("
                select *
                from player")) %>%
  collect()

lapply(seq_len(nrow(df)), function(i) {
  dbGetQuery(db$con, sprintf("
                  insert into pricing_parameters (product_id, cost_type_id, advertiser_type_id, order_type, parameters) 
                  values ('%s', '%s', '%s', '%s', '%s')", 
                             input$product, 
                             cId, 
                             df$advertiser_type_id[i],
                             df$order_type[i],
                             toJSON(list(arrivalRate=df$arrivalRate[i],
                                         priceSensitivity=df$priceSensitivity[i],
                                         timeScale=df$timeScale[i]), auto_unbox = TRUE)))
})

dbDisconnect(db$con)