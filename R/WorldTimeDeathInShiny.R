# remotes::install_github("joachim-gassen/tidycovid19")
# plot reported time, death using shiny
#
suppressPackageStartupMessages({
  library(tidycovid19)
  library(dplyr)
  library(ggplot2)  
  library(ggrepel)
  library(ggplot2)
  library(gridExtra)
  library(ggpubr)
  library(shiny)
})

# setup plot area as a table of plots
# grid <- matrix(c(1,1,2,3), nrow=2, ncol=2, byrow=TRUE)
# layout(grid)
# par(mfrow=c(2.2))

merged_dta <- download_merged_data(cached = TRUE)
## Downloading cached version of merged data...done. Timestamp is 2020-03-30 06:43:14
merged_dta %>%
  group_by(country) %>%
  mutate(
    reported_deaths = max(deaths),
    soc_dist_measures = max(soc_dist)
  ) %>%
  select(country, iso3c, reported_deaths, soc_dist_measures) %>%
  distinct() %>%
  ungroup() %>%
  arrange(-reported_deaths) %>%
  head(20) -> df

#
#ggarrange(df, merged_dta, 
#         labels = c("A", "B"),
#         ncol = 2, nrow = 2)
#
# ggplot(df, aes(x = reported_deaths, y = soc_dist_measures)) +
#   geom_point() +
#   geom_label_repel(aes(label = iso3c)) +
#   theme_minimal() +
#   scale_x_continuous(trans='log10', labels = scales::comma) + 
#   labs(x = "Reported deaths (logarithmic scale)",
#        y = "Number of governmental social distancing measures",
#        annotation = "Data from JHU CSSE and ACAPS.")

#plot_covid19_spread(merged_dta, highlight = c("ITA", "ESP", "FRA", "DEU", "USA"), 
#                  intervention = "lockdown")

shiny_covid19_spread() 
