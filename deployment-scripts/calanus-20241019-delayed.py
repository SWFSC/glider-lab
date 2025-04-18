# This script expects to be run in the glider-utils Instance in GCP

import logging
import math
import os

from esdglider import acoustics, config, gcp, glider, plots, utils

# Variables for user to update
deployment_info = {
    "deployment": "calanus-20241019",
    "project": "ECOSWIM",
    "mode": "delayed",
    "min_dt": "2024-10-19 17:37:00",
}
write_raw = False
write_nc = True

# Consistent variables
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
deployment_bucket = "amlr-gliders-deployments-dev"
acoustics_bucket = "amlr-gliders-acoustics-dev"
deployments_path = os.path.join(base_path, deployment_bucket)
acoustics_path = f"{base_path}/{acoustics_bucket}"
log_file = os.path.join(
    deployments_path,
    "logs",
    f"{deployment_info['deployment']}-{deployment_info['mode']}.log",
)
db_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-utils/db/glider-db-prod.txt"
config_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-lab/deployment-configs"

if __name__ == "__main__":
    logging.basicConfig(
        # filename=log_file,
        # filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # # Create config file - one-time, local run
    # with open(db_path_local, "r") as f:
    #     conn_string = f.read()
    # config.make_deployment_config(
    #     deployment_info,
    #     config_path_local,
    #     conn_string,
    # )

    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployment_bucket, deployments_path, ro=False)
    gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)

    paths = glider.get_path_deployment(
        deployment_info=deployment_info,
        deployments_path=deployments_path,
        config_path=config_path,
    )

    # Generate timeseries and gridded netCDF files
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_raw,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
        stall=20,
        shake=20,
        inversion=math.inf,
        interrupt=math.inf,
    )

    # #--------------------------------------------------------------------------
    # # Science dataset trimming
    # if write_nc:
    #     outname_tssci = outname_dict["outname_tssci"]
    #     deploymentyaml = paths["deploymentyaml"]
    #     griddir = paths["griddir"]
    #     mode = deployment_info["mode"]

    #     # Bad sci values: trim from 2024-11-01 18:24:37 to 2024-11-01 20:37:48
    #     tssci = xr.load_dataset(outname_tssci)
    #     tssci = tssci.where(
    #         (tssci.time <= np.datetime64("2024-11-01T18:24:37"))
    #         | (tssci.time >= np.datetime64("2024-11-01T20:37:48")),
    #         drop=True
    #     )
    #     logging.info(f"Max depth sanity check: {np.max(tssci.depth.values)}")

    #     # TODO: trim points identified in folium map

    #     # Write to Netcdf, and rerun gridding
    #     utils.to_netcdf_esd(tssci, outname_tssci)

    #     logging.info("ReGenerating 1m gridded data")
    #     outname_1m = pgncprocess.make_gridfiles(
    #         outname_tssci,
    #         griddir,
    #         deploymentyaml,
    #         dz=1,
    #         fnamesuffix=f"-{mode}-1m",
    #     )

    #     logging.info("ReGenerating 5m gridded data")
    #     outname_5m = pgncprocess.make_gridfiles(
    #         outname_tssci,
    #         griddir,
    #         deploymentyaml,
    #         dz=5,
    #         fnamesuffix=f"-{mode}-5m",
    #     )
    # --------------------------------------------------------------------------

    # tssci = xr.load_dataset(outname_tssci)
    # tseng = xr.load_dataset(outname_tseng)
    # g5sci = xr.load_dataset(outname_5m)

    # # Acoustics
    # a_paths = acoustics.get_path_acoutics(project, deployment, acoustics_path)
    # acoustics.echoview_metadata(tssci, a_paths)

    # # Plots
    # etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    # plots.all_loops(tssci, tseng, g5sci,
    #                 ccrs.Mercator(), paths['plotdir'], etopo_path)

    # # Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)
