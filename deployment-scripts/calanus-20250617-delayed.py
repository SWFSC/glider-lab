import logging
from pathlib import Path

import xarray as xr
from esdglider import aa, gcp, paths, plots, slocum, utils # type: ignore

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "calanus-20250617"
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
aa_in_bucket_name = "swfscesd-glider-active-acoustics-data-in"
# imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
# imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
aa_in_path = mnt_path / aa_in_bucket_name
# imagery_in_path = mnt_path / imagery_in_bucket_name
# imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"{Path(__file__).stem}.log"

if __name__ == "__main__":
    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)
   
    logging.basicConfig(
        filename=logs_path / log_file_name,
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
    logging.info("Beginning scheduled processing for %s", file_info)

    logging.info(
        "Removed file 01490000.ebd due to error from dbdreader:"
        + "'UnicodeDecodeError: 'ascii' codec can't decode byte 0xaa in "
        + "position 14: ordinal not in range(128)'. "
        + "Associated log note from acossio: "
        + "'ABORT: abort for no input- nlg showed that the Nortek wasn't "
        + "talking. So I commented out the Nortek out of proglets. "
        + "Did an exit reset.'"
        + "SMW thus judged it unlikley removing 01490000.ebd would cause "
        + "any meaningful data loss"
    )

    # Generate glider paths
    glider_paths = paths.get_path_glider(
        deployment_name = deployment_name, 
        mode = mode, 
        config_path = config_path, 
        data_in_path = data_in_path, 
        data_out_path = data_out_path, 
        cac_path = cac_path, 
    )

    ## Generate netCDF files and plots
    # Generate timeseries and gridded netCDF files
    outname_dict = slocum.binary_to_nc(
        deployment_name=deployment_name, 
        mode=mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
        binary_search="*.[DEde][Bb][Dd]", 
    )

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    # Acoustics
    aa_paths = paths.get_path_aa(
        deployment_name, 
        mode, 
        aa_in_path=aa_in_path, 
        data_out_path=data_out_path, 
    )
    aa.ancillary_echoview(tssci, aa_paths)

    ### Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=etopo_path,
    )
    
    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
