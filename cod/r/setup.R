
# Librerías ---------------------------------------------------------------

pacman::p_load(
  readr, 
  jsonlite, 
  lubridate,
  tidyverse,
  reticulate
)

# Scripts R ---------------------------------------------------------------

source("cod/r/scrapW.R")
source("cod/r/scrapT.R")

# Python ------------------------------------------------------------------

source_python("cod/python/setup.py")
