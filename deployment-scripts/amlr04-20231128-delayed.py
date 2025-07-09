# This script expects to be run in the glider-utils Instance in GCP

# NOTE: removed 02070294.EBD due to the following error:
# File "/opt/conda/envs/esdglider/lib/python3.12/site-packages/dbdreader/dbdreader.py", line 953, in _get
#     raise DbdError(DBD_ERROR_NO_TIME_VARIABLE)

import logging
import os

import numpy as np
import xarray as xr
from esdglider import acoustics, imagery, gcp, glider, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "amlr04-20231128"
mode = "delayed"
write_nc = True

# Consistent variables
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)
acoustics_bucket = "amlr-gliders-acoustics-dev"
acoustics_path = f"{base_path}/{acoustics_bucket}"
imagery_bucket = "amlr-gliders-imagery-raw-dev"
imagery_path = f"{base_path}/{imagery_bucket}"

deployment_info = {
    "deploymentyaml": os.path.join(config_path, f"{deployment_name}.yml"), 
    "mode": mode,
}
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
log_file_name = f"{deployment_name}-{mode}.log"

if __name__ == "__main__":
    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployments_bucket, deployments_path, ro=False)
    gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)
    gcp.gcs_mount_bucket(imagery_bucket, imagery_path, ro=False)
    paths = glider.get_path_deployment(deployment_info, deployments_path)

    logging.basicConfig(
        filename=os.path.join(paths["logdir"], log_file_name),
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Beginning scheduled processing for %s", file_info)

    # Generate timeseries and gridded netCDF files
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=False,
        file_info=file_info,
    )

    # Make any adjustments to netCDF files
    if write_nc:
        logging.info("Adjusting datasets, after review")
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        logging.info("Removing bogus points from timeseries dataset")
        # The bogus points appears to be because the science computer reset, 
        # which took eg3 minutes, and this point logged the previous values 
        # before collecting new ones. No need to rerun profiles, etc. See:
        # 'glider-lab/deployment-scripts/notebooks/amlr04-20231128-delayed.ipynb'
        times_todrop = np.array([
            '2023-11-28T22:10:49.251434240', '2023-11-29T06:10:54.020294144',
            '2023-11-29T15:33:10.920379648', '2023-11-29T23:54:31.435516416',
            '2023-11-30T02:49:44.635254016', '2023-11-30T12:26:01.345428480',
            '2023-11-30T13:57:39.851592960', '2023-11-30T17:13:05.463623168',
            '2023-11-30T22:02:17.223785472', '2023-12-01T03:16:39.983062784',
            '2023-12-01T09:13:32.987426816', '2023-12-01T19:01:31.347961344',
            '2023-12-01T23:08:49.339874304', '2023-12-02T06:36:10.718902528',
            '2023-12-02T14:17:18.784057600', '2023-12-02T16:16:14.320037888',
            '2023-12-02T17:47:19.856201216', '2023-12-03T05:34:44.405487104',
            '2023-12-03T16:05:46.832885760', '2023-12-03T17:55:15.642852864',
            '2023-12-03T19:14:24.122589184', '2023-12-04T09:00:58.429901056',
            '2023-12-04T12:44:58.327667200', '2023-12-05T02:49:18.434295552',
            '2023-12-05T13:11:56.089538560', '2023-12-05T18:05:32.308868352',
            '2023-12-05T23:48:32.127563520', '2023-12-07T11:43:48.641357312',
            '2023-12-08T13:31:35.615417600', '2023-12-08T20:20:00.470764288',
            '2023-12-09T07:33:06.596832256', '2023-12-09T12:42:51.621643008',
            '2023-12-10T08:10:27.838439936', '2023-12-10T14:18:49.686981120',
            '2023-12-10T19:56:25.514312704', '2023-12-11T01:40:31.322601216',
            '2023-12-11T16:46:16.394836480', '2023-12-12T10:53:00.884643584',
            '2023-12-12T22:52:52.985870336', '2023-12-13T18:20:45.020996096',
            '2023-12-14T00:31:43.072174080', '2023-12-14T06:55:51.096832256',
            '2023-12-14T13:33:07.697936896', '2023-12-14T16:48:53.281067008',
            '2023-12-14T19:40:49.542785536', '2023-12-15T07:41:47.097442560',
            '2023-12-15T19:04:30.661926144', '2023-12-15T23:51:29.179443456',
            '2023-12-16T04:18:08.286529536', '2023-12-16T07:37:02.992614656',
            '2023-12-16T21:46:28.429412864', '2023-12-16T21:49:48.932434176',
            '2023-12-17T02:58:56.758819584', '2023-12-17T15:02:02.564208896',
            '2023-12-18T15:55:27.170898432', '2023-12-19T05:22:25.079010048',
            '2023-12-19T11:46:59.320861696', '2023-12-19T18:00:59.366607616',
            '2023-12-20T00:04:31.460113408', '2023-12-20T05:25:46.442291200',
            '2023-12-20T17:58:50.054504448', '2023-12-21T02:51:42.570495488',
            '2023-12-21T15:22:21.060913152', '2023-12-21T21:39:21.646881024',
            '2023-12-22T03:52:34.033874432', '2023-12-22T10:04:44.299987712',
            '2023-12-22T16:16:25.952239872', '2023-12-22T22:27:48.119781376',
            '2023-12-23T04:46:58.757446400', '2023-12-23T07:08:31.193969664',
            '2023-12-24T03:04:07.491638272', '2023-12-24T09:35:36.832855296',
            '2023-12-25T10:37:39.356353792', '2023-12-25T20:07:53.574768128',
            '2023-12-25T22:23:36.827362048', '2023-12-25T23:00:18.536163328',
            '2023-12-26T05:25:21.649627648', '2023-12-26T11:38:09.922668544',
            '2023-12-26T17:54:10.763397120', '2023-12-26T23:34:19.060363776',
            '2023-12-27T04:34:13.221618688', '2023-12-27T07:20:33.012329216',
            '2023-12-27T12:23:00.358551040', '2023-12-27T17:51:44.648132352',
            '2023-12-28T02:54:50.654479872', '2023-12-28T17:54:59.708953856',
            '2023-12-29T11:28:58.282257152', '2023-12-29T15:02:44.502319360',
            '2023-12-30T03:36:26.834045440', '2023-12-30T10:01:44.224670464',
            '2023-12-31T05:15:50.867279104', '2023-12-31T11:21:48.710021888',
            '2023-12-31T17:31:53.248931840', '2024-01-01T02:16:23.587066624',
            '2024-01-01T06:46:10.641509888', '2024-01-01T17:34:51.489410304',
            '2024-01-01T18:39:56.847869952', '2024-01-01T21:15:03.070465024',
            '2024-01-02T14:17:53.706115840', '2024-01-03T09:05:37.624023552',
            '2024-01-03T11:23:03.475463936', '2024-01-03T17:39:47.878967296',
            '2024-01-03T21:33:22.660400384', '2024-01-04T03:54:03.639099136',
            '2024-01-04T10:23:12.936340224', '2024-01-04T20:34:10.411285504',
            '2024-01-04T22:53:16.901428224', '2024-01-05T18:35:40.940185600',
            '2024-01-06T00:41:11.627502336', '2024-01-06T13:17:52.286926336',
            '2024-01-06T15:37:28.929992704', '2024-01-06T19:49:55.177337600',
            '2024-01-07T02:02:30.748687872', '2024-01-07T14:50:11.168273920',
            '2024-01-08T01:03:57.020965632', '2024-01-08T03:25:42.267852800',
            '2024-01-09T05:43:05.313598720', '2024-01-09T15:54:27.665832448',
            '2024-01-09T18:13:21.662689280', '2024-01-09T22:21:49.457855232',
            '2024-01-09T22:25:08.929351680', '2024-01-10T11:13:46.233062656',
            '2024-01-11T07:57:14.438995456', '2024-01-11T09:10:06.749450752',
            '2024-01-11T11:15:21.081634560', '2024-01-11T11:54:08.242309632',
            '2024-01-11T18:11:18.520507904', '2024-01-11T20:26:52.298431488',
            '2024-01-12T00:37:07.503692544', '2024-01-12T09:53:31.151947008',
            '2024-01-12T15:47:25.311431936', '2024-01-12T16:05:05.044250368',
            '2024-01-12T19:16:56.936248832', '2024-01-12T23:29:43.481414912'
        ], dtype='datetime64[ns]')
        num_orig = len(tssci.time)
        tssci = tssci.drop_sel(time=times_todrop)
        num_dropped = num_orig - len(tssci.time)
        if num_dropped > 0:
            logging.info("Dropped %s point from science", num_dropped)

        # Double check profiles, write to netcdf, and rerun gridding
        utils.check_profiles(tssci)
        utils.to_netcdf_esd(tssci, outname_dict["outname_tssci"])
        del tssci        
        logging.info("Generating gridded data")
        outname_dict = glider.binary_to_nc(
            deployment_info=deployment_info,
            paths=paths,
            write_raw=False,
            write_timeseries=False,
            write_gridded=True,
            file_info=file_info,
        )  

    # Acoustics
    tssci = xr.load_dataset(outname_dict["outname_tssci"])
    a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    acoustics.echoview_metadata(tssci, a_paths)

    # Imagery
    i_paths = imagery.get_path_imagery(deployment_info, imagery_path)
    imagery.imagery_timeseries(tssci, i_paths)

    # Plots
    plots.esd_all_plots(outname_dict, crs=None, base_path=paths["plotdir"])
    g5sci = xr.load_dataset(outname_dict["outname_gr5m"])
    plots.sci_surface_map_loop(
        g5sci,
        crs="Mercator",
        base_path=paths["plotdir"],
        figsize_x=11,
        figsize_y=8.5,
    )

    # # Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
