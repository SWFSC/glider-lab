#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Write gcsfuse install to a file to run
cat << 'EOF' > ~/install_gcsfuse.sh
#!/bin/bash

# # Lazy (ie, force unmount) unmount of all gcsfuse mounts
# for dir in /home/user/mnt-gcs/*/; do fusermount -uz "$dir"; done

sudo apt-get update
sudo apt-get install -y curl lsb-release

echo "Starting installation of gcsfuse"
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc

sudo apt-get update
sudo apt-get install -y gcsfuse
EOF
sudo chmod 755 ~/install_gcsfuse.sh

# Install gcsfuse
~/install_gcsfuse.sh

##### Install miniconda

# ==========================================
# CONFIGURATION
# ==========================================
# Choose your target OS installer URL (Uncomment the one you need)
# Linux x86_64 (Standard 64-bit Linux)
MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
INSTALL_DIR="$HOME/miniconda3"
INSTALLER_NAME="miniconda_installer.sh"

# ==========================================
# EXECUTION
# ==========================================

echo "Downloading Miniconda..."
# -L follows redirects, -o specifies output filename
curl -L "$MINICONDA_URL" -o "$INSTALLER_NAME"

echo "Installing Miniconda silently..."
# Flags explained: 
# -b : Batch mode (silent, accepts license agreement automatically)
# -u : Update/overwrite existing installation if it exists
# -p : Path prefix where Miniconda should be installed
bash "$INSTALLER_NAME" -b -u -p "$INSTALL_DIR"

echo "Cleaning up installer script..."
rm "$INSTALLER_NAME"

echo "Initializing conda for the current shell..."
# Initialize conda for bash (change 'bash' to 'zsh' if using Zsh)
"$INSTALL_DIR/bin/conda" init bash

echo "=================================================="
echo "Miniconda installation complete!"
echo "Please run: 'source ~/.bashrc' (or restart your terminal) to start using conda."
echo "=================================================="


##### Other VM things
git clone https://github.com/SWFSC/glider-processing.git
git clone https://github.com/SWFSC/esdglider.git
git clone https://github.com/SWFSC/standard-glider-files.git

# 
# git config --global user.name "Sam Woodman"
# git config --global user.email "sam.woodman@noaa.gov"

MNT_PATH=mnt-gcs
mkdir -p $MNT_PATH/swfscesd-glider-logs
mkdir $MNT_PATH/swfscesd-glider-deployments-data-in
mkdir $MNT_PATH/swfscesd-glider-deployments-data-out
mkdir $MNT_PATH/swfscesd-glider-aa-data-in
mkdir $MNT_PATH/swfscesd-glider-imagery-data-in
mkdir $MNT_PATH/swfscesd-glider-imagery-metadata

gcloud auth application-default login
gcloud config set project ggn-nmfs-swfscesd-prod-1
gcloud auth application-default set-quota-project ggn-nmfs-swfscesd-prod-1
