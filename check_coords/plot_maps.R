library(ggplot2)
library(dplyr)
library(lubridate)
#library("mclust")
library(maps)
library(mapdata)
library(dplyr)
library(RSQLite,quietly = T)
library(DBI,quietly = T)

library(tibble,quietly = T)

dbase <- "stations_dk.sqlite"
table <- "stations_dk"
db <- dbConnect(SQLite(), dbase)
dbListTables(db)

out <- tbl(db, table)
locations <- data.frame(out)

# Get a world map
world_map <- map_data("world")[map_data("world")$region=="Denmark",] # Create a plot



# Create a plot
map_plot <- ggplot() +
  geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue") +
  geom_point(data = locations, aes(x = lon, y = lat), size = 3) +
  
  #geom_point(data = locations, aes(x = lon, y = lat, color = station), size = 3) +
  theme_void() +
  labs(title = "Locations on Map")

# Display the plot
print(map_plot)



