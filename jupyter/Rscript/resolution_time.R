library (ggplot2)

# File downloaded from https://raw.githubusercontent.com/Hareem-E-Sahar/gitter/master/Scripts_Graphs/ResolutionTime_GitterIssues.csv
# Change to correct path
df<-read.csv("~/Downloads/ResolutionTime_GitterIssues.csv",header = TRUE)
df2<-df[df$project=="amber" | df$project=="aws-sdk-go" | df$project=="JTAppleCalendar" | df$project=="Perfect" | df$project=="shuup.csv" | df$project=="mailboxer" | df$project=="react-starter-kit",]

# File generated to output/grimoire_time_to_close_hours.csv by running "Preliminary Results.ipynb"
# Change to correct path
grimoire<-read.csv("~/Downloads/grimoire_time_to_close_hours.csv",header=TRUE)

previous<-data.frame("resolution time"=grimoire$time_to_close_hours,"project"=grimoire$project,"approach"="GrimoireLab")
grimoirelab<-data.frame("resolution time"=df2$resolutiontime,"project"=df2$project, "approach"="Previous")

final<-rbind(previous,grimoirelab)

ggplot(final, aes(x=project, y=resolution.time, fill=(approach))) +
  geom_boxplot()  + theme_light()+
  theme(legend.position =  c(.85, .9),legend.title  = element_blank(),axis.text.x = element_text(angle = 60,hjust=1), 
        axis.text=element_text(size=10), axis.title =element_text(size=12), 
        panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  xlab(element_blank()) + scale_y_log10()+
  ylab("Resolution Time in Hours (log scale)") +
  scale_fill_manual(values=c( "bisque2", "cyan3"))

    