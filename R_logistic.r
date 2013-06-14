library(pscl)
data <- read.csv('/home/yang/GraduationProject/data/features/feature_col.csv',header=T,sep='\t')
train = data[1:60000,]
test = data[60000:87610,]
log=glm(target~url+sent+general+length+category,family=binomial(link='logit'),data=data)
summary(log)
pre <- predict(log, type="response")
phat <- predprob(log,test)
rid_origion <- data.frame(rid=data[1],target=data[7])

pre_target = c()
for (i in 1:length(pre)){
  if(pre[i] > 0.1){
  pre_target[i] = 1
  }else{
    pre_target[i] = 0
  }
}
rid_result <- data.frame(rid=data[1],target=pre_target)
target <- data$target

count = 0
for (i in 1:length(pre_target)){
  if(pre_target[i] == 1 && target[i] == 1 ){
    count = count +1
    print(count)
}
}
  
detected_fake = length(rid_result[rid_result[2] == 1])
annotation_fake = length(rid_origion[rid_origion[2] == 1])