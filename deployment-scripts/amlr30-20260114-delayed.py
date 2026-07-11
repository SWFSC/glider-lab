import logging
from pathlib import Path

# import numpy as np
import xarray as xr
from esdglider import gcp, imagery, paths, plots, utils # type: ignore
from esdglider.slocum import pipeline # type: ignore

### Variables for user to update
deployment_name = "amlr30-20260114"
mode = "delayed"
write_nc = True

### Consistent variables
# Define directories
home = Path.home()
mnt_path = home / "mnt-gcs"
cac_path = home / "standard-glider-files" / "Cache"
config_path = home / "glider-lab" / "deployment-configs"

# Bucket names and paths
logs_bucket_name = "swfscesd-glider-logs"
data_in_bucket_name = "swfscesd-glider-deployments-data-in"
data_out_bucket_name = "swfscesd-glider-deployments-data-out"
imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
imagery_in_path = mnt_path / imagery_in_bucket_name
imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).name}"
log_file_name = f"{deployment_name}-{mode}.log"

if __name__ == "__main__":
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

    # Generate timeseries netCDF files
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        file_info=file_info,
        shake=15,
        interrupt=500,
        length=16,
    )

    if write_nc:
        tsraw = xr.load_dataset(outname_dict_ts["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict_ts["outname_tseng"])
        tssci = xr.load_dataset(outname_dict_ts["outname_tssci"])

        # Adjust profile index
        logging.info("Correcting profile_index for raw, eng, and sci datasets")
        # tssci["profile_index"].loc[dict(time="2024-11-13 15:14:59")] = 590.5
        tsraw["profile_index"].loc[
            dict(time=slice("2026-02-01 09:05", "2026-02-01 09:16:10"))
        ] = 397
        tsraw["profile_index"].loc[
            dict(time=slice("2026-01-24 00:03:07", "2026-01-24 00:04:10"))
        ] = 167
        tsraw["profile_index"].loc[
            dict(time=slice("2026-01-25 01:51", "2026-01-25 01:55"))
        ] = 182
        
        # Finish raw dataset work
        prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(glider_paths["profsummpath"], index=False)
        utils.check_profiles(prof_summ)
        utils.to_netcdf_esd(tsraw, outname_dict_ts["outname_tsraw"])

        # Apply new profiles to sci and eng
        tseng = utils.join_profiles(tseng, prof_summ, shake=15, interrupt=500, length=16)
        tssci = utils.join_profiles(tssci, prof_summ, shake=15, interrupt=500, length=16)
        utils.to_netcdf_esd(tseng, outname_dict_ts["outname_tseng"])
        utils.to_netcdf_esd(tssci, outname_dict_ts["outname_tssci"])
        logging.info("Completed adjustments")


    # Generate gridded netCDF files
    outname_dict_gr = pipeline.generate_gridded(
        glider_paths=glider_paths,
        write_gridded=write_nc,
    )

    outname_dict = outname_dict_ts | outname_dict_gr

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    # Imagery
    img_paths = paths.get_path_imagery(
        deployment_name = deployment_name, 
        imagery_in_path = imagery_in_path, 
        imagery_meta_path = imagery_meta_path, 
        data_out_path = data_out_path, 
    )
    imagery.imagery_timeseries(tssci, img_paths)

    ### Plots
    plots.esd_all_plots(outname_dict, crs=None, base_path=glider_paths["plotdir"], max_workers=1)
    plots.sci_surface_map_loop(
        xr.load_dataset(outname_dict["outname_gr5m"]),
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        figsize_x=11,
        figsize_y=8.5,
        max_workers = 1
    )

    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     glider_paths['profdir'], 
    #     glider_paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
