#!/usr/bin/env Rscript

print("##### main.R #####")

suppressPackageStartupMessages(library(jsonlite))

DATASETS_BASE_URI <- "http://archive.ics.uci.edu/ml/machine-learning-databases"

parse_params <- function() {
   args <- commandArgs(trailingOnly = TRUE)
    if (length(args) != 1) {
        stop("Usage: Rscript script.R {json}'", call. = FALSE)
    }
    params <- fromJSON(args[1])
    print("params", params)
    return(params)
}


params <- parse_params()
dataset_file_path <- params$filepath
data <- read.csv(file.path(DATASETS_BASE_URI, filepath), sep = ";")
results <- toJSON(head(data, 5), pretty = TRUE, auto_unbox = TRUE)

cat(results)


# send params
# log to dagster
# recieve results
# persist data
