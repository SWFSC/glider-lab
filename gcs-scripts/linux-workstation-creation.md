# Linux Workstation Creation for ESD Glider Data Processing

Create a linux workstation for ESD glider data processing. This workstation is run through VScode or Positron and you should already have one of these installed. 

1) Go to [https://console.cloud.google.com/workstations/list?project=ggn-nmfs-wsent-prod-1](https://console.cloud.google.com/workstations/list?project=ggn-nmfs-wsent-prod-1) and select 'Create workstation'

2) Choose a display name (i.e. kburger-gliders), select oss-medium configuration, and click 'Create'

3) Clone esd-gcp-scripts repo locally

4) Open a new text file and enter the following, replacing the path with your cloned repo path and workstation ID (w-kourtneyburger-mucsysq2)

``` shell
@echo off
call C:\Users\kourtney.burger\Documents\GitHub\esd-gcp-scripts\workstation-startup-remotessh.bat w-kourtneyburger-mucsysq2 oss-medium
pause
```

6) Save this file to your desktop as `glider-workstation-startup.bat`

7) Double click the bat file to start the remotessh startup

8) A popup command prompt window will appear and you may be prompted to enter you password for GCP credentials. Type your password in the window and press enter, note: you will not see your password print to screen

9) The workstation will then open a VSCode or Positron window

10) Clone the glider-lab repo to your VM. In the terminal window run `git clone https://github.com/SWFSC/glider-lab.git`

11) Continue with directions [here](https://github.com/SWFSC/glider-lab/blob/main/gcs-scripts/linux-workstation-provision.md)
