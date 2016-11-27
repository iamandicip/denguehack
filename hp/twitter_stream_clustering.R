
#install.packages("stream")
library(stream)

#install.packages("png")
#library(png)


#don't forget to set your working directory (Session->Set Working Directory)


#twitterData = read.csv("tweets_south_america_dengue_09-11 2.csv", stringsAsFactors=FALSE)
#twitterData = twitterData[nrow(twitterData):1, ]

twitterData = read.csv("bra_jan_tweets.csv", stringsAsFactors=FALSE)
twitterData = twitterData[nrow(twitterData):1, ]

tweetDate = as.data.frame(twitterData[, "date"])
tweetCoor = twitterData[, c("long","lat")]


# create stream with one value every ... minutes (if no tweet is in this interval, a dummy tweet is inserted)

#interval = as.difftime("10",format = "%M", units = "mins")
# interval_bounds = as.difftime(c(0,25), units = "mins")
# interval = interval_bounds[2]-interval_bounds[1]
# 
# begin = strptime(tweetDate[1,1], format="%Y-%m-%d  %H:%M:%S")
# end = strptime(tweetDate[nrow(tweetDate),1], format="%Y-%m-%d  %H:%M:%S")
# streamSamples = seq(begin, end, interval)
# dummyTweet = c("some date to be replaced", -1000 + runif(1, -500, 500), -1000 + runif(1, -500, 500)) #randomized non-existent position because they do not cluster then 
# 
# previousStreamIndex = 1
# for (index in 1:nrow(twitterData)){
#   for (streamIndex in previousStreamIndex:nrow(twitterData)){
#     streamDate = streamSamples[streamIndex]
#     currentTweetDate = strptime(twitterData[index,"date"], format="%Y-%m-%d  %H:%M:%S")
#     if (abs(difftime(currentTweetDate, streamDate)) < interval){
#       print(index)
#       print(twitterData[index,"date"])
#       print("mapped to ")
#       print(as.character(streamDate))
#       twitterData[index,"date"] = as.character(streamDate)
#       print("difference ")
#       print(difftime(currentTweetDate, streamDate))
#       previousStreamIndex = streamIndex
#       break;
#     } 
#   }
# }


stream <- DSD_Memory(tweetCoor) # used to perform the clustering on
streamCopy <- DSD_Memory(tweetCoor) # used to figure out the resulting assignments 
streamCopy2 <- DSD_Memory(tweetCoor)

# animate_data(stream,horizon = 10, n=400, , xlim=c(-80,-30), ylim=c(-40,15))
# animation::ani.options(interval = 0.1)
# saveHTML(ani.replay())

timespan_symptoms = 7 * 24 * 60 # concept of "half-life", days in minutes
data_period = 22 * 24 * 60 #days in minutes 
total_tweets = nrow(twitterData)
av_tweets_per_minute = total_tweets / data_period 
number_of_events_in_timespan = timespan_symptoms * av_tweets_per_minute 
lambda =  number_of_events_in_timespan

dstream <-DSC_DStream(gridsize=2, Cm = 1,  0.00001 *  lambda)



frames = 1
op <- par(no.readonly = TRUE)
layout(mat = matrix(1:frames, ncol = 3))
n = ceiling(total_tweets/frames)
for(frame in c(1:frames)) {
    
  update(dstream, stream, n )
  plot(dstream, streamCopy, n, type = "micro")
  
  centers = get_centers(dstream, type="micro")
  weights = get_weights(dstream, type="micro")
  n_clusters = nrow(centers)
  clusterStart = rep(twitterData[((frame-1)*n) + 1, "date"], n_clusters) 
  clusterEnd = rep(twitterData[(frame*n), "date"], n_clusters)
  clusters_df <- data.frame(centers,weights, clusterStart, clusterEnd)
  names(clusters_df) <- c("lon","lat", "weight", "clusterStart", "clusterEnd")
  
  points = get_points(streamCopy2, n)
  timestamps = as.data.frame(tweetDate[(((frame-1)*n) + 1) : (frame*n), 1])
  
  clusterStart = rep(twitterData[((frame-1)*n) + 1, "date"], n) 
  clusterEnd = rep(twitterData[(frame*n), "date"], n)
  
  assignments = get_assignment(dstream, points, type="micro", method = "model")  
  tweets_df <- data.frame(assignments, timestamps, points, clusterStart, clusterEnd)
  names(tweets_df) <- c("assigned_to_cluster", "timestamp", "lon", "lat", "clusterStart", "clusterEnd")
  
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





