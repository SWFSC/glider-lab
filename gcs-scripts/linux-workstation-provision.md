# ESD Glider Data Processing on Linux Workstation

## Provisioning

Provision a linux workstation for ESD glider data processing. 

1) Run [`linux-workstation-provision.sh`](./linux-workstation-provision.sh) from `~/` using
```bash
bash /home/user/glider-lab/gcs-scripts/linux-workstation-provision.sh
```
(see [What the provisioning script does](#what-the-provisioning-script-does)). You will not need to run this script each time. However, you will need to run `~/install_gcsfuse.sh` (which `linux-workstation-provision.sh` will create) every time you restart the VM. 

2) Follow instructions from conda: "Please run: `source ~/.bashrc` (or restart your terminal) to start using conda." 

3) If necessary for development, configure git with user/email. Eg (replace with your GitHub username and email): 

``` shell
git config --global user.name "Sam Woodman"
git config --global user.email "sam.woodman@noaa.gov"
```

4) Build esdglider conda env to set up the Python environment:

``` shell
conda env create -f ~/esdglider/environment.yml
conda activate esdglider && pip install -e esdglider --config-settings editable_mode=compat
```

5) Select esdglider environment, and run some scripts

6) If necessary, upload "[ETOPO_2022_v1_15s_N45W135_erddap.nc](https://drive.google.com/file/d/1fcjT9_ksNK-qZECv0iVLmjac280fACfq/view?usp=drive_link)" file to your home directory
(*this is just a bathymetry file so don't worry if you don't need it*)

### What the provisioning script does

[`linux-workstation-provision.sh`](./linux-workstation-provision.sh):

- Installs [gcsfuse](https://cloud.google.com/storage/docs/gcsfuse) so applications can access Google Cloud Storage buckets as files
- installs Miniconda and configures it for Bash.
- clones `glider-processing`, `esdglider`, and `standard-glider-files` repos into home directory
- makes several directories under `mnt-gcs` for GCS-related data
- Starts Google Application Default Credentials login and sets the default Google Cloud project to `ggn-nmfs-swfscesd-prod-1`

The script stops if a command fails. It does not create or mount the GCS buckets; the directories are prepared locations only.