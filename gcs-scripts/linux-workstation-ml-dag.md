# Running the imagery pipeline on a Linux workstation

Use the [`esdglider`](https://github.com/SWFSC/esdglider/) imagery pipeline to extract image metadata, generate OSI
manifests, and submit model runs to the Optics SI Airflow DAG.

## Prepare the workstation

1. Complete [workstation creation](./linux-workstation-creation.md).
2. Complete [workstation provisioning](./linux-workstation-provision.md),
   including `gcsfuse`, Google Application Default Credentials, and the local
   `esdglider` git clone.
3. Activate the provisioned Python conda environment and use the scripts from the `esdglider` repo (the imagery CLI scripts).

## Run the pipeline

Follow the
[imagery pipeline guide in esdglider](https://github.com/SWFSC/esdglider/blob/main/docs/imagery-pipeline.md).
In a local checkout, it is located at `docs/imagery-pipeline.md`.

That guide covers the shared deployment YAML, recommended single-command
workflow, optional individual stages, bucket inputs and outputs, preview and
live-submission modes, and recovery safeguards.
