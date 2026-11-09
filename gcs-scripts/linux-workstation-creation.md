# Linux Workstation Creation for ESD Glider Data Processing

Create a linux workstation for ESD glider data processing.

1) Go to [https://console.cloud.google.com/workstations/list?project=ggn-nmfs-wsent-prod-1](https://console.cloud.google.com/workstations/list?project=ggn-nmfs-wsent-prod-1) and select 'Create workstation'

2) Choose a display name (i.e. kburger-gliders), select oss-medium configuration, and click 'Create'

## (recommended but optional) Automating connection to the Workstation with Positron or VSCode
*note: this is useful for users with a Windows 11 setup but not strictly necessary*

The following steps automate starting the GCP workstation and opening an SSH connection to it via Positron or VSCode. The `workstation-startup-remotessh.bat` script also checks Google auth, opens an SSH TCP tunnel, and launches the user into /home/user/ on the remote machine.

*warning: [the automated connection script](https://github.com/SWFSC/esd-gcp-scripts/blob/main/workstation-startup-remotessh.bat) recommends that you disable host-key checking which is nice because when you stop and start a workstation it changes keys, but this is also potentially dangerous so just remember that you did it*

1) Clone [esd-gcp-scripts](https://github.com/SWFSC/esd-gcp-scripts) repo to your *local computer* (**not to the workstation you just created!**)

2) Open a new  file and enter the following, replacing the path with your cloned repo path and workstation ID (w-kourtneyburger-mucsysq2)

``` shell
@echo off
call C:\Users\kourtney.burger\Documents\GitHub\esd-gcp-scripts\workstation-startup-remotessh.bat w-kourtneyburger-mucsysq2 oss-medium
pause
```

3) Save this file to your desktop as `glider-workstation-startup.bat`

4) Double click the bat file to start the remotessh startup

5) A popup command prompt window will appear and you may be prompted to enter you password for GCP credentials. Type your password in the window and press enter, note: you will not see your password print to screen

6) The workstation will then open a VSCode or Positron window

## Initializing codebase in newly created Workstation

1) Clone the glider-lab repo to your VM. In the terminal window run `git clone https://github.com/SWFSC/glider-lab.git`

2) Continue with directions [here](https://github.com/SWFSC/glider-lab/blob/main/gcs-scripts/linux-workstation-provision.md)
