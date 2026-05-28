import logging
from pathlib import Path

import numpy as np
import xarray as xr
from esdglider import aa, gcp, paths, plots, slocum, utils # type: ignore

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "calanus-20241019"
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
        deployment_name=deployment_name, 
        mode=mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=False,
        file_info=file_info,
        stall=2,
        interrupt=120,
    )

    # --------------------------------------------------------------------------
    # Science dataset trimming
    if write_nc:
        logging.info("Adjusting datasets after review")
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict["outname_tseng"])
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        # Adjust profile index
        logging.info("Correcting profile_index for raw, eng, and sci datasets")
        # tssci["profile_index"].loc[dict(time="2024-11-13 15:14:59")] = 590.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5
        tseng["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5
        tssci["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5
        
        # Finish raw dataset work
        prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(glider_paths["profsummpath"], index=False)
        utils.check_profiles(prof_summ)
        utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])

        # Drop a specific sci value - confirmed ok in raw/eng
        tssci = tssci.where(
            (tssci["time"] != np.datetime64("2024-11-01 18:58:36.312000")),
            drop=True,
        )

        # Drop time ranges with bogus lat/lons
        logging.info(
            "Dropping time ranges with bogus lat/lons from eng and sci datasets",
        )
        drop_ranges = [
            ("2024-10-21 14:26:50", "2024-10-21 19:52:30"),
            ("2024-11-09 13:15", "2024-11-09 18:10"),
            ("2024-11-14 01:00", "2024-11-14 01:10:20"),
        ]
        tseng = slocum.drop_ts_ranges(
            tseng, 
            drop_ranges, 
            "eng", 
            plotdir=glider_paths["plotdir"], 
            profsummdir=glider_paths["profsummpath"], 
            outname=outname_dict["outname_tseng"], 
        )
        tssci = slocum.drop_ts_ranges(
            tssci, 
            drop_ranges, 
            "sci", 
            plotdir=glider_paths["plotdir"], 
            profsummdir=glider_paths["profsummpath"], 
            outname=outname_dict["outname_tssci"], 
        )
        
        # Profile checks - done in drop_ts_ranges
        # utils.check_profiles(utils.calc_profile_summary(tseng, "depth"))
        # utils.check_profiles(utils.calc_profile_summary(tssci, "depth"))

        # Write to Netcdf, and rerun gridding
        # logging.info("Write timeseries to netcdf")
        # utils.to_netcdf_esd(tseng, outname_dict["outname_tseng"])
        # utils.to_netcdf_esd(tssci, outname_dict["outname_tssci"])
        del tsraw, tssci, tseng, prof_summ

        logging.info("Gridding corrected science data")
        outname_dict = slocum.binary_to_nc(
            deployment_name=deployment_name, 
            mode=mode, 
            glider_paths=glider_paths,
            write_raw=False,
            write_timeseries=False,
            write_gridded=True,
            file_info=file_info,
        )
    # --------------------------------------------------------------------------

    # Acoustics
    tssci = xr.load_dataset(outname_dict["outname_tssci"])
    aa_paths = paths.get_path_aa(
        deployment_name, 
        mode, 
        aa_in_path=aa_in_path, 
        data_out_path=data_out_path, 
    )
    aa.ancillary_echoview(tssci, aa_paths)

    # Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=etopo_path,
    )

    # # Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
