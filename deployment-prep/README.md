# Glider Deployment Prep Folder

All glider deployment prep files (including ballasting sheets, functional checkouts, sensor config files, etc.) are available in the associated deployment folder above. Completed deployments will be moved into the associated year folder.

All past glider deployment folders (2023-May 2026) are available on the [AMLR Gliders Google Drive folder](https://drive.google.com/drive/folders/1qfKMxXH0hUhbmOp8aESidz-YO3IPxWM3?usp=drive_link).

***Follow the steps below to create new deployment prep folder or edit existing folders.***

## Prerequisites

- GitHub Enterprise account with access to SWFSC organization

- GitHub Desktop installed on local computer

- `glider-lab` repository main branch cloned to local computer

## Steps for setting up a new deployment prep folder 

1.  Open GitHub Desktop and pull any recent changes from the `glider-lab` repo by clicking on 'Fetch origin'

2.  Open repo in file explorer and navigate to `glider-lab/deployment-prep`

3.  Copy the `glider-YYYYmmdd-prep` folder and rename it with your glider name and deployment date (e.g. 'calanus-20261019-prep')

4.  Download and save the [ballast sheet](https://swfsc.github.io/glider-lab-manual/content/documents/Glider-Ballasting-Template.xls) and [functional checkout procedure](https://swfsc.github.io/glider-lab-manual/content/documents/4095-FCP%20Functional%20Checkout%20Procedure.xlsx) to the `glider-YYYYmmdd-prep/glider-prep` folder.

    a.  Rename the ballast sheet to include the glider name and ballast date (`glider-YYYYmmdd_Glider-Ballasting.xls`).

    b.  Rename the functional sheet to include the glider name and functional date (`glider-YYYYmmdd_FCP.xlsx`).

5.  Edit and upload files as needed

6.  Push changes back to GitHub when you are done working on a file (i.e. at the end of the day)

    a.  Save all files and open GitHub desktop, you should see a list of changes.

    b.  Select all changes, write a brief summary starting with your initials (ex. "KB - updated ballast sheet") and add a detailed description if needed.

    c.  Click `Commit to main` and `Push origin`

## Steps to edit an existing folder

