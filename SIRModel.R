#
# Code and Explanation: https://cran.r-project.org/web/packages/shinySIR/vignettes/Vignette.html
#
install.packages("shinySIR")
install.packages("devtools")
#
# 
# githubinstall("shinySIR")
library(shinySIR)
library(devtools)
#
# 1. Basic SIR model without parameters specified:  
# run_shiny(model = "SIR")
# 2. User-Defined Model
#
mySIRS <- function(t, y, parms) {
  
  with(as.list(c(y, parms)),{
    
    # Change in Susceptibles
    dS <- - beta * S * I + delta * R
    
    # Change in Infecteds
    dI <- beta * S * I - gamma * I
    
    # Change in Recovereds
    dR <- gamma * I - delta * R
    
    return(list(c(dS, dI, dR)))
  })
}

run_shiny(model = "SIRS (w/out demography)", 
          neweqns = mySIRS,
          ics = c(S = 9999, I = 1, R = 0),
          parm0 = c(beta = 5e-5, gamma = 1/7, delta = 0.1),
          parm_names = c("Transmission rate", "Recovery rate", "Loss of immunity"),
          parm_min = c(beta = 1e-5, gamma = 1/21, delta = 1/365),
          parm_max = c(beta = 9e-5, gamma = 1 , delta = 1))
