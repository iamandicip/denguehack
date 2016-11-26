
#install.packages("stream")
library(stream)

#install.packages("png")
#library(png)


#don't forget to set your working directory (Session->Set Working Directory)


twitterData = read.csv("tweets_south_america_approx.csv")
tweetDate = as.data.frame(twitterData[, "date"])
tweetCoor = twitterData[, c("long","lat")]
stream <- DSD_Memory(tweetCoor) # used to perform the clustering on
streamCopy <- DSD_Memory(tweetCoor) # used to figure out the resulting assignments 
streamCopy2 <- DSD_Memory(tweetCoor)

# animate_data(stream,horizon = 10, n=400, , xlim=c(-80,-30), ylim=c(-40,15))
# animation::ani.options(interval = 0.1)
# saveHTML(ani.replay())


dstream <-DSC_DStream(gridsize=5, Cm = 5, lambda = 0.001)
#update(dstream, stream, n = 100)
#dstream

#dstream <-DSC_DStream(gridsize=0.05, Cm = 10, lambda = 0.1)


frames = 6
op <- par(no.readonly = TRUE)
layout(mat = matrix(1:frames, ncol = 2))
reset_stream(stream)
n = ceiling(2300/frames)
for(frame in c(1:frames)) {
  
  update(dstream, stream, n )
  plot(dstream, streamCopy, n, type = "micro", assignment=TRUE)
  
  centers = get_centers(dstream, type="micro")
  weights = get_weights(dstream, type="micro")
  clusters_df <- data.frame(centers,weights)
  names(clusters_df) <- c("long","lat", "weight")
  
  points = get_points(streamCopy2, n)
  print((frame-1)*n + 1)
  print(frame*n)
  timestamps = as.data.frame(tweetDate[(((frame-1)*n) + 1) : (frame*n), 1])
  assignments = get_assignment(dstream, points, type="micro", method = "model")  
  tweets_df <- data.frame(assignments, timestamps)
  names(tweets_df) <- c("assigned_to_cluster", "timestamp")
    
  write.csv(clusters_df, file = paste(as.character(frame),"_centers.csv"))
  write.csv(tweets_df, file = paste(as.character(frame),"_tweets.csv"))
}
par(op)





#reset_stream(stream)


#saveHTML(animate_cluster(dstream, stream, horizon = 200, n = 2300, type = "macro", assign="macro", measure = "numMicroClusters"), plot.args = list(xlim = c(-60, 20), ylim = c(-100, -30)))
#dstream
#animation::ani.options(interval = 0.1)
#saveHTML(ani.replay())
#ani.replay()





