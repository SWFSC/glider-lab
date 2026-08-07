---
editor_options: 
  markdown: 
    wrap: 72
---

1.  Follow NMFS Open Science Intro to Workstations [Tutorial: Getting
    Started on Google
    Workstations](https://nmfs-opensci.github.io/CloudComputingSetup/content/intro/intro.html#tutorial-getting-started-on-google-workstations)

    a.  If setting this up for processing deployment reports, a small
        RStudio configuration should be enough processing power

    b.  Change configuration for other processes as needed

2.  Follow NMFS Open Science [Connecting Workstations to Code and Data
    tutorial](https://nmfs-opensci.github.io/CloudComputingSetup/content/code-and-data/code-and-data.html)
    to connect GitHub to your workstation and clone relevant glider
    repositories 

    a.  If running deployment reports, clone [glider-lab
        repo](https://github.com/SWFSC/glider-lab)

    b.  Complete step three to mount glider data buckets to workstation

3.  When you get to [Cloud Data in Workstations: Google Buckets
    section](https://nmfs-opensci.github.io/CloudComputingSetup/content/code-and-data/code-and-data.html#cloud-data-in-workstations-google-buckets),
    do not run the terminal code provided. This will only mount one
    bucket

    a.  Within the glider-lab repo, open the
        gcs-scripts/mount_bucket_folder.sh

    b.  Edit line 15 to include any additional buckets you want to mount

    c.  In the terminal, run
        `bash $HOME/glider-lab/gcs-scripts/mount_bucket_folder.sh` .
        This will mount the buckets you selected and install spatial
        package dependencies for completing deployment reports

**You will need to run the \`mount_bucket_folder.sh\` script every time
you restart your workstations to reestablish the mounts**
