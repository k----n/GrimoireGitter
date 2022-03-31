library (ggplot2)

# File downloaded from https://raw.githubusercontent.com/Hareem-E-Sahar/gitter/master/ResolutionTime_AllGitterBugReports.csv and modified to have correct project names by running "Preliminary Results.ipynb"
# Change to correct path
df<-read.csv("/home/ubuntu/github/GrimoireGitter/jupyter/output/previous_pipeline_time_to_close_hours.csv",header = TRUE)

# File generated to output/grimoire_time_to_close_hours.csv by running "Preliminary Results.ipynb"
# Change to correct path
grimoire<-read.csv("/home/ubuntu/github/GrimoireGitter/jupyter/output/grimoire_time_to_close_hours.csv",header=TRUE)

previous<-data.frame("resolution time"=df$resolution_time, "project"=df$name, "approach"="Previous")
grimoirelab<-data.frame("resolution time"=grimoire$time_to_close_hours, "project"=grimoire$short_name, "approach"="GrimoireLab")

final<-rbind(previous,grimoirelab)

ggplot(final, aes(x=project, y=resolution.time, fill=(approach))) +
  geom_boxplot()  + theme_light()+
  theme(legend.position =  c(.89, 0.15),legend.title  = element_blank(),axis.text.x = element_text(angle = 60,hjust=1), 
        axis.text=element_text(size=10), axis.title =element_text(size=12), 
        panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  xlab(element_blank()) + scale_y_log10()+
  ylab("Resolution Time in Hours (log scale)") +
  scale_fill_manual(values=c( "bisque2", "cyan3"))


ggsave("time_to_close_comparison.pdf", height = 4, width = 7)