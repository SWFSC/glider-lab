# Running imagery models through the OSI DAG

Extract image metadata, generate manifest JSON files, and
submit those manifests to the Optics SI (OSI) Airflow DAG in Cloud Composer.
Can be run before glider profiles are corrected;
scripts use imagery and image metadata rather than corrected profile files.

## Prerequisites

1. Complete [Linux workstation creation](./linux-workstation-creation.md).
2. Complete [Linux workstation provisioning](./linux-workstation-provision.md),
   including the Python environment and local `esdglider` installation.
3. Use conda environment in terminal or select it as editor's Python
   interpreter before running the scripts.
4. Ensure Google Application Default Credentials are configured and your
   account has access to the imagery, metadata, and logs buckets. Triggering
   runs also requires access to the configured Cloud Composer DAG and output
   bucket. The DAG's execution identity needs access to its inputs and outputs.

The commands below assume the `esdglider` repository is at `~/esdglider` but you can run
them from any working directory

## 1. Extract image metadata

Open
[`extract-image-metadata.py`](https://github.com/SWFSC/esdglider/blob/main/scripts/extract-image-metadata.py).

1. Set `deployment_name`, for example `"calanus-20261007"`.
2. Set `run_pipeline_bool = True` to generate metadata.
3. Run:

   ```bash
   python ~/esdglider/scripts/extract-image-metadata.py
   ```

With the default bucket settings, the script reads JPEG and PNG images under:

```text
gs://swfscesd-glider-imagery-data-in/{year}/{deployment_name}/images/
```

It writes these files through the mounted imagery-metadata bucket:

```text
gs://swfscesd-glider-imagery-metadata/{year}/{deployment_name}/{deployment_name}-deployment-metadata.json
gs://swfscesd-glider-imagery-metadata/{year}/{deployment_name}/{deployment_name}-image-metadata.jsonl
```

The run log is written to:

```text
gs://swfscesd-glider-logs/{deployment_name}-image-metadata-extraction.log
```

**Before rerunning:** if either metadata output already exists, extraction is
skipped. A failed run can leave partial outputs; inspect those before deciding
how to recover. The log is opened in write mode, replacing an existing log
with the same name.

Setting `run_pipeline_bool = False` skips metadata extraction, but *still mounts
buckets, scans image paths, and writes the log*. It is *not* write-free.

## 2. Generate OSI manifest JSON files

Open
[`generate-osi-json.py`](https://github.com/SWFSC/esdglider/blob/main/scripts/generate-osi-json.py).

1. Set `deployment_name` to the same deployment used in step 1.
2. Set `dir_chunk_size`, normally `50`. This is the number of image directories
   per manifest, not the number of images.
3. Leave `dir_filter = None` to include all image directories, or supply a list
   of directory names to process a subset.
4. Leave `use_tmp_dir = False` to write directly to the metadata bucket.
5. Run:

   ```bash
   python ~/esdglider/scripts/generate-osi-json.py
   ```

The script reads the image-metadata JSONL file from step 1 and writes manifests
such as:

```text
gs://swfscesd-glider-imagery-metadata/{year}/{deployment_name}/osi-manifests-050dirs/{deployment_name}-image-manifest-chunk01.json
```

`050dirs` reflects a chunk size of 50; the final chunk can contain fewer
directories. Existing manifests with the same filenames are overwritten.

If `use_tmp_dir = True`, manifests are instead written under
`/home/user/tmp-meta/{deployment_name}/osi-manifests-050dirs/`. The script prints
a suggested copy command but does not execute it. Upload the manifests to the
metadata bucket before proceeding.

## 3. Preview DAG submissions

Open
[`trigger-osi-dag.py`](https://github.com/SWFSC/esdglider/blob/main/scripts/trigger-osi-dag.py).

1. Set `DEPLOYMENT_NAME` to the same deployment used above.
2. Set `DIRECTORY_CHUNK_SIZE` to match `dir_chunk_size` from step 2.
   The script derives `DEPLOYMENT_YEAR`, `CHUNK_DIRECTORY`, `JSON_FOLDER_PATH`,
   and `OUTPUT_FOLDER_PATH`; do not edit the derived paths separately.
3. Confirm `COMPOSER_URL`, `DAG_ID`, `MODEL_TYPE`, `YAML_CONFIG_PATH`, and the
   input and output bucket names are appropriate for the intended run.
4. Explicitly set `DRY_RUN = True` before running. Do not assume it is enabled.
5. Leave `TEST_LIMIT = None` to preview all eligible manifests, or set a small
   number to preview only the first few.
6. Run:

   ```bash
   python ~/esdglider/scripts/trigger-osi-dag.py
   ```

For `calanus-20261007` and a chunk size of 50, verify that the printed payloads
use:

| Payload field | Expected value |
| --- | --- |
| `input_file` | A manifest under `gs://swfscesd-glider-imagery-metadata/2026/calanus-20261007/osi-manifests-050dirs/` |
| `output_bucket` | `ggn-nmfs-osi-dev-1-data` |
| `output_folder` | `SWFSC/glider/calanus-20261007/050dirs/01`, then `02`, etc. |

Dry-run mode obtains credentials and lists Cloud Storage objects, but does not
send DAG trigger requests or write model results. It does not validate DAG
submission permissions or prove that the configured model and YAML will run.

### Important rerun limitation

Do not rely on the current script to skip previously processed manifests.
Its exclusion check compares full manifest basenames, such as
`calanus-20261007-image-manifest-chunk01`, against output folder names, while
its payloads request numbered output folders such as `01`. The names do not
match. Folder-prefix handling also needs review before this check can be
relied on.

Output numbering is based on the position in the filtered submission list,
not a persistent manifest-to-output mapping. Before a live run or rerun,
inspect existing outputs and DAG runs to avoid duplicate processing or output
collisions. An existing output folder alone does not establish that a run
completed successfully.

## 4. Submit and monitor DAG runs

After reviewing the dry-run payloads and existing runs:

1. Set `DRY_RUN = False`.
2. Set `TEST_LIMIT` deliberately: a small number for an initial live test, or
   `None` for all eligible manifests.
3. Run the same trigger command from step 3.
4. Check each submission response. A successful trigger means Airflow accepted
   the request, not that image processing finished.
5. Monitor the DAG runs in the configured Cloud Composer Airflow UI and the
   [Batch job list](https://console.cloud.google.com/batch/jobs?cloudshell=false&project=ggn-nmfs-osi-dev-1).
6. Inspect results in the
   [output bucket](https://console.cloud.google.com/storage/browser/ggn-nmfs-osi-dev-1-data/SWFSC/glider).

For the example above, the requested output prefix for the first submission is:

```text
gs://ggn-nmfs-osi-dev-1-data/SWFSC/glider/calanus-20261007/050dirs/01/
```

The DAG and YAML pipeline determine the actual result files beneath the
requested output location. Restore `DRY_RUN = True` after submitting to reduce
the risk of accidentally triggering runs later.
