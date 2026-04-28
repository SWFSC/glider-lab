import logging
# import os
from pathlib import Path

import xarray as xr
from esdglider import gcp, paths, slocum # type: ignore
#acoustics, imagery, plots, slocum

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "amlr08-20220513"
mode = "delayed"
write_nc = True

# Define directories
home = Path.home()
mnt_path = home / "gcs-mnt"
cac_path = home / "standard-glider-files" / "Cache"
config_path = home / "glider-lab" / "deployment-configs"

# Consistent variables
logs_bucket = "swfscesd-glider-logs"
data_in_bucket = "swfscesd-glider-deployments-data-in"
data_out_bucket = "swfscesd-glider-deployments-data-out"
# acoustics_bucket = "amlr-gliders-acoustics-dev"
# imagery_bucket = "amlr-gliders-imagery-raw-dev"

logs_path = mnt_path / logs_bucket
data_in_path = mnt_path / data_in_bucket
data_out_path = mnt_path / data_out_bucket
# acoustics_path = f"{base_path}/{acoustics_bucket}"
# imagery_path = f"{base_path}/{imagery_bucket}"

deployment_info = {
    "deploymentyaml": (config_path / f"{deployment_name}.yml"), 
    "mode": mode,
}
# file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).name}"
log_file_name = f"{deployment_name}-{mode}2.log"


if __name__ == "__main__":
    # Mount the buckets
    gcp.gcs_mount_bucket(logs_bucket, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket, data_out_path, ro=False)
    # gcp.gcs_mount_bucket(imagery_bucket, imagery_path, ro=False)

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
        write_gridded=write_nc,
        # write_gridded=False,
        file_info=file_info,
    )

#     ### Sensor-specific processing
#     tssci = xr.load_dataset(outname_dict["outname_tssci"])

#     # Acoustics
#     a_paths = acoustics.get_path_acoustics(deployment_info, acoustics_path)
#     acoustics.echoview_metadata(tssci, a_paths)

#     # Imagery
#     i_paths = imagery.get_path_imagery(deployment_info, imagery_path)
#     imagery.imagery_timeseries(tssci, i_paths)

#     ### Plots
#     etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
#     plots.esd_all_plots(
#         outname_dict,
#         crs="Mercator",
#         base_path=paths["plotdir"],
#         bar_file=etopo_path,
#     )

#     # ### Generate profile netCDF files for the DAC
#     # glider.ngdac_profiles(
#     #     outname_dict["outname_tssci"], paths['profdir'], paths['deploymentyaml'],
#     #     force=True)

#     logging.info("Completed scheduled processing")
