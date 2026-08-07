# Terminal code for mounting Google Cloud Buckets to Google Cloud Workstations
# Adapted from NMFS Open Sci workstation tutorial, https://nmfs-opensci.github.io/CloudComputingSetup/content/code-and-data/code-and-data.html

# UPDATES
# 6/3/2026: KBurger edited to mount multiple buckets with one script and changed 
# mount_point to match other cloud processing scripts developed by Sam

# Run this script as a .sh file by copying and pasting this code in your bash 
# terminal:  
#bash $HOME/glider-lab/gcs-scripts/mount_bucket_folder.sh


# --- Bucket Setup ---
# Define your buckets and the root mount directory
BUCKETS=("swfscesd-glider-deployments-data-in" "swfscesd-glider-deployments-data-out" "swfscesd-glider-imagery-data-in" "swfscesd-glider-imagery-metadata")

# Defining the root mount folder to match Sam's setup
MNT_ROOT="$HOME/gcs-mnt"


# --- Authentication ---
# Add the Google Cloud GPG key to your system's trusted keys.
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/gcsfuse.gpg

# Add the GCS FUSE repository to your system's sources list.
echo "deb [signed-by=/etc/apt/trusted.gpg.d/gcsfuse.gpg] https://packages.cloud.google.com/apt gcsfuse-`lsb_release -c -s` main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list > /dev/null

# Update the package list to include the new repository.
echo "Updating package list..."
sudo apt-get update

# Install gcsfuse.
echo "Installing gcsfuse..."
sudo apt-get install -y gcsfuse

# Load linux libraries for spatial R packages
sudo apt install libnetcdf-dev libudunits2-dev libgdal-dev


# --- Mounting the Buckets ---  
# This loop goes through every bucket defined in the BUCKETS array above.
for BUCKET_NAME in "${BUCKETS[@]}"; do
    MOUNT_POINT="$MNT_ROOT/$BUCKET_NAME"
    
    echo "--------------------------------------------"
    echo "Processing bucket: $BUCKET_NAME"
    echo "Target mount point: $MOUNT_POINT"
    echo "--------------------------------------------"

    # Create the mount point folder if it doesn't exist.
    if [ ! -d "$MOUNT_POINT" ]; then
        mkdir -p "$MOUNT_POINT"
    fi

    # Use gcsfuse to mount the specific bucket.
    echo "Mounting $BUCKET_NAME..."
    gcsfuse --implicit-dirs --only-dir "$FOLDER_NAME" "$BUCKET_NAME" "$MOUNT_POINT"

    echo "Mounting complete for $BUCKET_NAME."
done

echo "All buckets processed!"