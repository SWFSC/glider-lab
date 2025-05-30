library(stringr)
library(tidyr)
library(dplyr)

#set your working directory to the folder that has all sample87.ma, proglets.dat, solocam.cfg, and solocam.ini files
setwd("C:/Users/jen.walsh/Documents/GitHub/glider-lab/deployment-reports/Data/risso-20250414/file-archive")

#for each file type (.ma, .cfg, .ini, .dat), create a list of file names
listma<-list.files(pattern="*_sample*")
#listsgcfg<-list.files(pattern="*_solocam*")
#listaacfg<-list.files(pattern="*_ad2cp*")
listpacfg<-list.files(pattern="*_wispr*")

#read each line of the list as a separate character string
all.ma<-lapply(listma,readLines) 
#sg.cfg<-lapply(listsgcfg,readLines)
#aa.cfg<-lapply(listaacfg,readLines)
pa.cfg<-lapply(listpacfg,readLines)

#unlist the list so that individual strings can be selected
all.ma<-unlist(all.ma)
#sg.cfg<-unlist(sg.cfg)
#aa.cfg<-unlist(aa.cfg)
pa.cfg<-unlist(pa.cfg)

#get rid of leading white spaces by left-justifying text (only an issue for .ma and .dat files)
all.ma<-str_trim(all.ma,"left")

#select strings that start with "b_arg:" (ma files),"$" (cfg files), a capital letter (ini files), or that don't start with "#" (proglets)
ma.args<-all.ma[grep("^b_arg:*",all.ma)]
#sg.cfg.args<-sg.cfg[grep("^\\$,.*",sg.cfg)] #solocam
pa.cfg.args<-pa.cfg[grep("^\\$ADC,.*",pa.cfg)] #wispr

####for .ma and .dat files only#########################
#get rid of white space between b_arg and #, proglets commands and #
ma.args<-str_squish(ma.args)

#split character string at "#" (for .ma files only)
ma.args<-str_split(ma.args,"#")

#unlist ma.args to be able to get rid of everything after the "#"
ma.args<-unlist(ma.args)

#get rid of everything behind the "#"
ma.args<-ma.args[c(TRUE,FALSE)]

######################################################

#create a dataframe so that a column with date/time stamp can be added
ma.args<-as.data.frame(ma.args)
#sg.cfg.args<-as.data.frame(sg.cfg.args)
#aa.cfg.args<-as.data.frame(aa.cfg.args)
pa.cfg.args<-as.data.frame(pa.cfg.args)

#split the original file names to isolate the date/time string
x1<-str_split(listma,"_")
x2<-str_split(listpacfg,"_")
#x3<-str_split(listaacfg,"_")
#x4<-str_split(listsgcfg,"_")

#unlist the list so that individual strings can be selected
x1<-unlist(x1)
x2<-unlist(x2)
#x3<-unlist(x3)
#x4<-unlist(x4)

#just select the date/time strings
x1<-x1[c(TRUE,FALSE)]
x2<-x2[c(TRUE,FALSE)]
#x3<-x3[c(TRUE,FALSE)]
#x4<-x4[c(TRUE,FALSE)]

#create objects that repeat the date/time string for the number of arguments per file
a1<-nrow(ma.args)/length(listma)
x1<-rep(x1,each=a1)

#not sure these next four lines are necessary
#a3<-nrow(aa.cfg.args)/length(listaacfg)
#x3<-rep(x3,each=a3)
#a4<-nrow(sg.cfg.args)/length(listsgcfg)
#x4<-rep(x4,each=a4)

#get rid of wispr.ini. FIX THIS CODE TO MAKE IT WORK ACROSS THE BOARD
x2<-x2[-2]

#create new columns with date and time for each data frame
ma.args<-cbind(ma.args,x1)
pa.cfg.args<-cbind(pa.cfg.args,x2)
#aa.cfg.args<-cbind(aa.cfg.args,x3,f3)
#sg.cfg.args<-cbind(sg.cfg.args,x4,f4)

#create new data frame with all args
new.col.names<-c("arg","date.time")
colnames(ma.args)<-new.col.names
colnames(pa.cfg.args)<-new.col.names
#colnames(aa.cfg.args)<-new.col.names
#colnames(sg.cfg.args)<-new.col.names

#split "args" column into multiple columns for ma files
ma.args<-ma.args %>%
  separate(arg,c("delete","parameter","value")," ")

#delete column "b_arg" (not necessary)
ma.args<-ma.args[-1]

#create a sensor column for ma.args
ma.args<-ma.args %>%
  select(parameter:value,date.time) %>%
  mutate(
    Sensor = case_when(
      parameter == "sensor_type(enum)" & value == 1 ~ "CTD",
      parameter == "sensor_type(enum)" & value == 48 ~ "ECO Puck",
      parameter == "sensor_type(enum)" & value == 54 ~ "Optode",
      parameter == "sensor_type(enum)" & value == 56 ~ "PAR"
    )
  )

#create an "on/off" column"
ma.args<-ma.args %>%
  select(parameter:value,date.time,Sensor) %>%
  mutate(
    On.Off = case_when(
      parameter == "state_to_sample(enum)" & value == 1 ~ "On",
      parameter == "state_to_sample(enum)" & value == 0 ~ "Off"
    )
  )

# shift on.off up by 1
ma.args$On.Off<-lead(ma.args$On.Off,n=1)

#get rid of NAs
ma.args<-na.omit(ma.args)

#split date and time into two columns
ma.args<-ma.args %>% separate_wider_delim(date.time,"T",names=c("Date","Time"))
ma.args<-as.data.frame(ma.args)

#get rid of first two columns
ma.args<-ma.args[,-c(1:2)]

#reformat date
ma.args$Date<-strptime(ma.args$Date,format="%Y%m%d",tz="UTC")

#reformat time
ma.args$Time<-strptime(ma.args$Time,format="%H%M%S")
ma.args$Time<-strftime(ma.args$Time,"%H:%M:%S")


#rename columns for cfg files
pa.cfg.args<-as.data.frame(pa.cfg.args)
pa.cfg.args<-pa.cfg.args %>%
  rename(
    Value=arg
  )


#splitting date and time
pa.cfg.args<-pa.cfg.args %>% separate_wider_delim(date.time,"T",names=c("Date","Time"))
pa.cfg.args<-as.data.frame(pa.cfg.args)

#reorder columns
pa.cfg.args<-pa.cfg.args[,c(2,3,1)]
