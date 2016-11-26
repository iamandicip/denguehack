
#install.packages("stream")
library(stream)

#install.packages("png")
#library(png)


#don't forget to set your working directory (Session->Set Working Directory)


twitterData = read.csv("tweets_south_america_approx.csv")

tweetCoor = twitterData[, c("lat","long")]
stream <- DSD_Memory(tweetCoor)

#stream <- DSD_Benchmark(1)


# animate_data(stream,horizon = 10, n=400, , xlim=c(-80,-30), ylim=c(-40,15))
# animation::ani.options(interval = 0.1)
# saveHTML(ani.replay())



dstream <-DSC_DStream(gridsize=1, Cm = 1, lambda = 0.01)
update(dstream, stream, n = 100)
dstream

#dstream <-DSC_DStream(gridsize=0.05, Cm = 10, lambda = 0.1)

# update(dstream, stream, n = 100)
# 
# dstream
# 
# reset_stream(stream)
# 
# plot(dstream, stream, n = 100, grid = TRUE)
# 
# reset_stream(stream)


#update(dstream, stream, n = 100)
#plot(dstream, stream, n = 100, grid = TRUE)


#reset_stream(stream)


saveHTML(animate_cluster(dstream, stream, horizon = 100, n = 2300, type = "macro", assign="macro", measure = "numMicroClusters", plot.args = list(xlim=c(-80,-30), ylim=c(-40,15))))
animation::ani.options(interval = 0.1)
saveHTML(ani.replay())
ani.replay()











#animate_cluster(dstream, stream, horizon = 50, n=400, measure="g2")
#evaluate(dstream, stream, horizon = 50, n=400, measure="g2")
#animation::ani.options(interval = 0.1)
#saveHTML(ani.replay())

#plot(dstream, stream, type="both")



