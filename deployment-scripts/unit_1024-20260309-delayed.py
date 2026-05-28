import logging
# import os
from pathlib import Path

import xarray as xr
from esdglider import gcp, imagery, paths, plots, slocum # type: ignore
#acoustics, imagery, plots, slocum

### Variables for user to update
deployment_name = "unit_1024-20260309"
mode = "delayed"
write_nc = True

### Consistent variables
# Define directories
home = Path.home()
mnt_path = home / "gcs-mnt"
cac_path = home / "standard-glider-files" / "Cache"
config_path = home / "glider-lab" / "deployment-configs"

# Bucket names and paths
logs_bucket_name = "swfscesd-glider-logs"
data_in_bucket_name = "swfscesd-glider-deployments-data-in"
data_out_bucket_name = "swfscesd-glider-deployments-data-out"
# acoustics_bucket = "amlr-gliders-acoustics-dev"
imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
# acoustics_path = f"{base_path}/{acou
# stics_bucket}"
imagery_in_path = mnt_path / imagery_in_bucket_name
imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
# deployment_info = {
#     "deploymentyaml": (config_path / f"{deployment_name}.yml"), 
#     "mode": mode,
# }
# file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).name}"
log_file_name = f"{deployment_name}-{mode}.log"


if __name__ == "__main__":
    # Mount the buckets
    gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)
    gcp.gcs_mount_bucket(imagery_in_bucket_name, imagery_in_path, ro=True)
    gcp.gcs_mount_bucket(imagery_meta_bucket_name, imagery_meta_path, ro=True)

    logging.basicConfig(
        filename=logs_path / log_file_name,
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
    logging.info("Beginning scheduled processing for %s", file_info)

    # Generate glider paths
    glider_paths = paths.get_path_glider(
        deployment_name = deployment_name, 
        mode = mode, 
        config_path = config_path, 
        data_in_path = data_in_path, 
        data_out_path = data_out_path, 
        cac_path = cac_path, 
    )

    # Generate timeseries and gridded netCDF files
    outname_dict = slocum.binary_to_nc(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        # write_gridded=write_nc,
        write_gridded=True,
        binary_search="*.[de]cd", 
        file_info=file_info,
    )

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

#     # Acoustics
#     a_paths = acoustics.get_path_acoustics(deployment_info, acoustics_path)
#     acoustics.echoview_metadata(tssci, a_paths)

    # Imagery
    img_paths = paths.get_path_imagery(
        deployment_name = deployment_name, 
        imagery_in_path = imagery_in_path, 
        imagery_meta_path = imagery_meta_path, 
        data_out_path = data_out_path, 
    )
    imagery.imagery_timeseries(tssci, img_paths)

    ### Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=etopo_path,
    )

#     # ### Generate profile netCDF files for the DAC
#     # glider.ngdac_profiles(
#     #     outname_dict["outname_tssci"], paths['profdir'], paths['deploymentyaml'],
#     #     force=True)

#     logging.info("Completed scheduled processing")
