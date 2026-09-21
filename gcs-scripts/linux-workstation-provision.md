# ESD Glider Data Processing on Linux Workstation

Provision a linux workstation for ESD glider data processing. 

1) Run `linux-workstation-provision.sh`

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
