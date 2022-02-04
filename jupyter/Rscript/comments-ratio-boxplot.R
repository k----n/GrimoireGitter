library(ggplot2)

# File downloaded from https://github.com/Hareem-E-Sahar/gitter/blob/master/2-CombineCommentsForBoxplot-v3.csv
# Change to correct path
data<-read.csv("~/Downloads/2-CombineCommentsForBoxplot-v3.csv",header=TRUE)
df<-data[data$project=="aws-sdk-go" | data$project=="Perfect" | data$project=="JTAppleCalendar" | data$project=="amber" | data$project=="shuup" | data$project=="react-starter-kit",]

# File generated to output/gitter_comments_count_1_week.csv by running "Preliminary Results.ipynb"
# Change to correct path
df2<-read.csv("~/Downloads/gitter_comments_count_1_week.csv",header=TRUE)
newdf<-data.frame("project"=df$project, "ratio" = df$ratio, approach="Previous")

newdf2<-data.frame("project"=df2$project, "ratio"=df2$ratio , approach="GrimoireLab")
final<-rbind(newdf,newdf2)

ggplot(final, aes(x=project, y=(ratio))) + aes(type=approach )+
  geom_boxplot(aes(fill=approach), colour="black")  + theme_light()+ 
  theme(legend.position = c(.85, .85),legend.title  = element_blank(),axis.text.x = element_text(angle = 60,hjust=1), 
        axis.text=element_text(size=10), axis.title =element_text(size=12), 
        panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  xlab(element_blank()) +
  ylab("Comments Change Ratio") + geom_hline(yintercept=1.0,color='red') 
  
