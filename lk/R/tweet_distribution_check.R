a <- read.csv(file="tweets_south_america_approx.csv")
b <- strptime(a$date, format="%Y-%m-%d %H:%M:%S", tz="UTC")
plot(hist(as.numeric(strftime(b, "%H")), breaks=24))


library(ggplot2)
qplot(b, geom="density")

View(read.csv("tweets_south_america_dengue_09-11.csv"))