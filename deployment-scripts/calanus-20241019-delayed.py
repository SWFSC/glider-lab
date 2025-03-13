# Processing script for calanus-20241019
# This script expected to be run in the glider-utils Instance in GCP

import os
import logging

import esdglider.pathutils as putils
import esdglider.gcp as gcp
import esdglider.config as config
import esdglider.process as process


deployment = 'calanus-20241019'
project = "ECOSWIM"
mode = 'delayed'
bucket_name = 'amlr-gliders-deployments-dev'

base_path = "/home/sam_woodman_noaa_gov"
deployments_path = f'{base_path}/{bucket_name}'
config_path = f"{base_path}/glider-lab/deployment-configs"

if __name__ == "__main__":
    logging.basicConfig(
        format='%(module)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')


    gcp.gcs_mount_bucket(
        "amlr-gliders-deployments-dev", deployments_path, ro=False)
    
    # Create config file - one-time local run by Sam
    # with open("db/glider-db-prod.txt", "r") as f:
    #     conn_string = f.read()

    # config.make_deployment_config(
    #     deployment, project, mode, 
    #     "C:/Users/sam.woodman/Downloads", conn_string)

    # Generate timeseries and gridded netCDF files
    outname_tseng, outname_tssci, outname_1m, outname_5m = process.binary_to_nc(
        deployment, project, mode, deployments_path, config_path, 
        write_timeseries=True, write_gridded=True, 
        min_dt='2024-10-19 17:37:00')
    
    # Generate profile netCDF files for the DAC
    # outname_tseng, outname_tssci, outname_1m, outname_5m = process.binary_to_nc(
    #     deployment, project, mode, deployments_path, config_path, 
    #     write_timeseries=False, write_gridded=False)
    
    # paths = putils.esd_paths(
    #     project, deployment, mode, deployments_path, config_path)
    
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'], 
    #     force=True)
