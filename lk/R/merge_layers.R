a <- read.csv("Brazil_cases_January_2016_1.csv")
b <- read.csv("adm1_layers.csv")

sapply(a$RegionsOfBrazil, function(x) x %in% b$NAME_1)
b[b$NAME_0=="Brazil","NAME_1"]

names(a) <- c("RegionsOfBrazil", "casesJan")

c <- merge(b, a, all.x=T, by.x="NAME_1", by.y="RegionsOfBrazil")

write.csv(c, "adm1_layers_cases.csv", row.names=F)
