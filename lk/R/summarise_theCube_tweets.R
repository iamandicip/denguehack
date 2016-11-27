library(tidyr)

sheetz <- NULL
for(fajl in dir(pattern="export.*.csv")) {
    sht <- paste(strsplit(fajl, split="[_\\.]")[[1]][2:4], collapse="_")
    sheetz[[sht]] <- read.csv(fajl)
}
sheetz$Dengue_Twitter_all <- NULL

allSAm <- do.call(what="rbind", args=sheetz)

# Add country names
allSAm$country <- sapply(strsplit(row.names(allSAm), "[_\\.]"), function(x) x[3])

# Remove columns 2-6
allSAm2 <- cbind(allSAm[1], allSAm[7:dim(allSAm)[2]])

# Reshape data
allSAm3<- gather(data=allSAm2, Labels, country)

# rename columns
names(allSAm3) <- c("adminLvl1", "country", "date", "count")

# format time
allSAm3$date <- sub("X(.*)\\.00\\.00\\.00", "\\1", allSAm3$date)

allSAm3$date <- strptime(allSAm3$date, "X%d.%m.%y",tz="UTC")

headrz <- strptime(names(allSAm2)[2:48], "X%d.%m.%y.00.00.00", tz="UTC")
names(allSAm2)[2:48] <- strftime(headrz)

write.csv(allSAm3, file="export_Dengue_Twitter_all.csv", row.names=F)
write.csv(allSAm2, file="export_Dengue_Twitter_all_b.csv", row.names=F)
