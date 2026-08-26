import logging
from pathlib import Path

import numpy as np
import xarray as xr
from esdglider import aa, gcp, paths, plots
import esdglider.profiles as prof
from esdglider.slocum import pipeline

logger = logging.getLogger(__name__)

### Variables for user to update
deployment_name = "calanus-20241019"
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
aa_in_bucket_name = "swfscesd-glider-active-acoustics-data-in"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
aa_in_path = mnt_path / aa_in_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"{Path(__file__).stem}.log"

#------------------------------------------------------------------------------
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
    logger.info("Beginning scheduled processing for %s", file_info)
    
    logger.info("Generating glider paths")
    glider_paths = paths.get_path_glider(
        deployment_name = deployment_name, 
        mode = mode, 
        config_path = config_path, 
        data_in_path = data_in_path, 
        data_out_path = data_out_path, 
        cac_path = cac_path, 
    )

    #--------------------------------------------------------------------------
    ### Timeseries and gridded netCDF generation
    logger.info("Generating timeseries netCDF files---------------------")
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        file_info=file_info,
        stall=2,
        interrupt=120,
    )


    # Recalculate flbbcd values and correct cdom, if necessary
    if write_nc:
        logger.info("Correcting data---------------------")
        pipeline.correct_cdom_raw_sci(glider_paths=glider_paths)


    # Correct profiles, and make other adjustments to netCDF files
    if write_nc:
        logger.info("Adjusting datasets, after review---------------------")
        outname_tsraw = outname_dict_ts["outname_tsraw"]
        outname_tseng = outname_dict_ts["outname_tseng"]
        outname_tssci = outname_dict_ts["outname_tssci"]

        tsraw = xr.load_dataset(outname_tsraw)
        tseng = xr.load_dataset(outname_tseng)
        tssci = xr.load_dataset(outname_tssci)

        # Adjust profile index
        logger.info("Correcting profile_index for raw, eng, and sci datasets")
        # tssci["profile_index"].loc[dict(time="2024-11-13 15:14:59")] = 590.5
        tsraw["profile_index"].loc[
            {"time": slice("2024-11-01 18:18", "2024-11-01 18:19")}
        ] = 356.5
        tseng["profile_index"].loc[
            {"time": slice("2024-11-01 18:18", "2024-11-01 18:19")}
        ] = 356.5
        tssci["profile_index"].loc[
            {"time": slice("2024-11-01 18:18", "2024-11-01 18:19")}
        ] = 356.5
        
        # Finish raw dataset work
        prof_summ = prof.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(glider_paths["profsummpath"], index=False)
        prof.check_profiles(prof_summ)
        tsraw.to_netcdf(
            outname_tsraw, 
            encoding={'time': pipeline.time_encoding}
        )

        # Drop specific bogus sci values, from when sci computer reset
        timesci_bad_start = np.datetime64("2024-11-01 18:25:00")
        timesci_bad_end = np.datetime64("2024-11-01 20:30:00")
        tssci = tssci.where(
            # (tssci["time"] != np.datetime64("2024-11-01 18:58:36.312000")),
            (tssci["time"] < timesci_bad_start) | (tssci["time"] > timesci_bad_end),
            drop=True,
        )

        # Drop time ranges with bogus lat/lons
        logger.info(
            "Dropping time ranges with bogus lat/lons from eng and sci datasets",
        )
        drop_ranges = [
            ("2024-10-21 14:26:50", "2024-10-21 19:52:30"),
            ("2024-11-09 13:15", "2024-11-09 18:10"),
            ("2024-11-14 01:00", "2024-11-14 01:10:20"),
        ]
        tseng = pipeline.drop_ts_ranges(
            tseng, 
            drop_ranges, 
            "eng", 
            plotdir=glider_paths["plotdir"], 
            profsummdir=glider_paths["profsummpath"], 
            outname=outname_tseng, 
        )
        tssci = pipeline.drop_ts_ranges(
            tssci, 
            drop_ranges, 
            "sci", 
            plotdir=glider_paths["plotdir"], 
            profsummdir=glider_paths["profsummpath"], 
            outname=outname_tssci, 
        )
        
        # Write to Netcdf, and rerun gridding
        logger.info("Write timeseries to netcdf")
        tseng.to_netcdf(
            outname_tseng, 
            encoding={'time': pipeline.time_encoding}
        )        
        tssci.to_netcdf(
            outname_tssci, 
            encoding={'time': pipeline.time_encoding}
        )
        del tsraw, tssci, tseng, prof_summ

    logger.info("Generating gridded netCDF files---------------------")
    outname_dict_gr = pipeline.generate_gridded(
        glider_paths=glider_paths,
        write_gridded=write_nc,
    )

    outname_dict = outname_dict_ts | outname_dict_gr

    #--------------------------------------------------------------------------
    ### Ancillary data products
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    logger.info("Active Acoustics---------------------")
    aa_paths = paths.get_path_aa(
        deployment_name, 
        mode, 
        aa_in_path=aa_in_path, 
        data_out_path=data_out_path, 
    )
    aa.ancillary_echoview(tssci, aa_paths)

    #--------------------------------------------------------------------------
    ### Plots
    logger.info("Generating plots---------------------")
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=str(etopo_path),
    )
    
    #--------------------------------------------------------------------------
    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    #--------------------------------------------------------------------------
    logger.info("Completed scheduled processing")
