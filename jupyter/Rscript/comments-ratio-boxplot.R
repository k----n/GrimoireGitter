library(ggplot2)

# File downloaded from https://github.com/Hareem-E-Sahar/gitter/blob/master/2-CombineCommentsForBoxplot-v3.csv and modified to have correct project names by running "Preliminary Results.ipynb"
# Change to correct path
df<-read.csv("/home/ubuntu/github/GrimoireGitter/jupyter/output/previous_comments_count_1_week.csv",header=TRUE)

# File generated to output/gitter_comments_count_1_week.csv by running "Preliminary Results.ipynb"
# Change to correct path
df2<-read.csv("/home/ubuntu/github/GrimoireGitter/jupyter/output/gitter_comments_count_1_week.csv",header=TRUE)

newdf<-data.frame("project"=df$project, "ratio" = df$ratio, approach="Previous")
newdf2<-data.frame("project"=df2$short_name, "ratio"=df2$ratio , approach="GrimoireLab")

final<-rbind(newdf,newdf2)

ggplot(final, aes(x=project, y=(ratio))) + aes(type=approach )+
  geom_boxplot(aes(fill=approach), colour="black")  + theme_light()+ 
  theme(legend.position = c(.85, .85),legend.title  = element_blank(),axis.text.x = element_text(angle = 60,hjust=1), 
        axis.text=element_text(size=10), axis.title =element_text(size=12), 
        panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  xlab(element_blank()) +
  ylab("Comments Change Ratio") + geom_hline(yintercept=1.0,color='red')
  
ggsave("comments_ratio_comparison.pdf", height = 4, width = 7)