# ESD Glider Data Processing on Linux Workstation

## Provisioning

Provision a linux workstation for ESD glider data processing. 

1) Run `linux-workstation-provision.sh`. You will not need to run this script each time. However, you will need to run `~/install_gcsfuse.sh` every time you restart the VM. 

2) Follow instructions from conda: "Please run: 'source ~/.bashrc' (or restart your terminal) to start using conda." 

3) If necessary for development, configure git with user/email. Eg (replace with your GitHub username and email): 

``` shell
git config --global user.name "Sam Woodman"
git config --global user.email "sam.woodman@noaa.gov"
```

4) Build esdglider conda env:

``` shell
conda env create -f ~/esdglider/environment.yml
conda activate esdglider && pip install -e esdglider --config-settings editable_mode=compat
```

5) Select esdglider environment, and run some scripts

6) If necessary, upload "[ETOPO_2022_v1_15s_N45W135_erddap.nc](https://drive.google.com/file/d/1fcjT9_ksNK-qZECv0iVLmjac280fACfq/view?usp=drive_link)" file to your home directory
