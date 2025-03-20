# Processing script for calanus-20241019
# This script expects to be run in the glider-utils Instance in GCP

import os
import logging
import importlib
import xarray as xr

# import esdglider.config as config
import esdglider as eg


# Variables for user to update
deployment = 'amlr08-20220513'
project = 'SANDIEGO'
mode = 'delayed'
min_datetime='2017-01-01'
write_nc = True

# Other vars
base_path = "/home/sam_woodman_noaa_gov"
bucket_name = 'amlr-gliders-deployments-dev'
deployments_path = os.path.join(base_path, bucket_name)
config_path = os.path.join(base_path, "glider-lab/deployment-configs")

if __name__ == "__main__":
    logging.basicConfig(
        format='%(module)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

    # Mount the deployments bucket, and generate paths dictionary
    eg.gcp.gcs_mount_bucket(
        "amlr-gliders-deployments-dev", deployments_path, ro=False)
    paths = eg.slocum.get_path_esd(
        project, deployment, mode, deployments_path, config_path)
    
    # # Create config file - one-time local run
    # with open("db/glider-db-prod.txt", "r") as f:
    #     conn_string = f.read()
    # config.make_deployment_config(
    #     deployment, project, mode, 
    #     "C:/Users/sam.woodman/Downloads", conn_string)

    # Generate timeseries and gridded netCDF files
    # min_dt determined from examining sci and eng timeseries files
    # 13 Mar 2025: cdom data removed from deployment yaml
    outnames = eg.slocum.binary_to_nc(
        deployment, mode, paths, min_dt=min_datetime, 
        write_timeseries=write_nc, write_gridded=write_nc)
    
    # # Overwrite the history attribute, if writing nc files
    if write_nc:
        history_str = (
            f"{eg.utils.datetime_now_utc()}: " + 
            f"https://github.com/SWFSC/glider-lab: " + 
            f"{os.path.basename(__file__)}: " +
            "; ".join([
                f"deployment={deployment}", f"mode={mode}", 
                f"min_dt={min_datetime}", 
                f"pyglider v{importlib.metadata.version("pyglider")}", 
                f"esdglider v{importlib.metadata.version("esdglider")}"])
        )
        for filename in outnames:
            print(filename)
            ds = xr.load_dataset(filename)
            ds.attrs['history'] = history_str
            ds.to_netcdf(filename, encoding=eg.slocum.encoding_dict)
        
    # # Generate profile netCDF files for the DAC
    # outname_tssci = os.path.join(paths['tsdir'], f"{deployment}-{mode}-sci.nc")
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'], 
    #     force=True)
