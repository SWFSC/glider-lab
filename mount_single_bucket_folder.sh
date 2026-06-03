# Terminal code for mounting Google Cloud Buckets to Google Cloud Workstations
# Author: Alexandra Norelli with Gemini assistance for R to BASH translations.  
# Run the .sh file with the code commented below and follow the instructions to 
# authenticate your google account.  

# Run this script as a .sh file by copying and pasting this code in your bash 
# terminal:  
#bash mount_single_bucket_folder.sh

# Define your bucket and the mount point.
# replace "nmfs-opensci" with your bucket name
# add the path to folder within the bucket for FOLDER_NAME
# make sure to put a / at the end of the folder path
# The `$HOME` symbol is a shortcut for your home directory, so this will
# create the folder at /home/your_username/my_gcs_bucket.
BUCKET_NAME="swfscesd-glider-deployments-data-in"
FOLDER_NAME="/"
MOUNT_POINT="$HOME/gcs-mnt"

# --- Authentication ---
# This command authenticates your user account with Google Cloud.
# You'll be prompted to open a browser to complete the login process.
echo "Running gcloud authentication. Please follow the instructions to log in in your browser."
gcloud auth application-default login --no-launch-browser

# --- Installation and Setup (Run only once) ---
# Create the mount point if it doesn't exist.
# Since this directory is in your home folder, you don't need `sudo` to create it.
if [ ! -d "$MOUNT_POINT" ]; then
    mkdir -p "$MOUNT_POINT"
fi

# Add the Google Cloud GPG key to your system's trusted keys.
# This is a critical step to verify the authenticity of the packages.
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/gcsfuse.gpg

# Add the GCS FUSE repository to your system's sources list.
echo "deb [signed-by=/etc/apt/trusted.gpg.d/gcsfuse.gpg] https://packages.cloud.google.com/apt gcsfuse-`lsb_release -c -s` main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list > /dev/null

# Update the package list to include the new repository.
echo "Updating package list..."
sudo apt-get update

# Install gcsfuse.
echo "Installing gcsfuse..."
sudo apt-get install -y gcsfuse

# --- Mounting the Bucket ---  you might only need to run this if restarting a workstation
# Use the gcsfuse tool to mount the bucket to the specified mount point.
# The mount point is in your home directory, so `sudo` is no longer needed.
echo "Mounting the bucket..."
gcsfuse --implicit-dirs --only-dir "$FOLDER_NAME" "$BUCKET_NAME" "$MOUNT_POINT"

echo "Mounting complete. You can now access the bucket contents at $MOUNT_POINT"

# Optional: List the contents to verify the mount was successful.
ls -l "$MOUNT_POINT"