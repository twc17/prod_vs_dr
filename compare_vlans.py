#!/usr/bin/python

# Description: Check that vlans match on PROD and DR
# Author: Lucci
# Author: Troy <twc17@pitt.edu>
# Date Updated: 09/16/2017
# Version: 1.3.2
#
# TODO: Check how I'm comparing VLAN IDs. Updated data strcut to a dict. 

import os, re, sys, glob

# Compare two lists for differences
def compare_lists(list1, list2):
    # List comprehension. Returns two lists, with only the differences between the original lists
    return [[item for item in list1.keys() if not item in list2.keys()], [item for item in list2.keys() if not item in list1.keys()]]

#
# Get latest configs
#
def get_latest_config(switch):
    for config_file in glob.iglob("/tftpboot/ciscoconfg/" + switch + ".gw*"):

        mtime = os.stat(config_file).st_mtime

        if mtime > highest_mtime:
            latest_config = config_file

            highest_mtime = mtime

    return latest_config

#
# Loop through configs looking for vlans
#
def get_vlans(latest_config):
    vlans = {}

    try:
        print ("Latest config: " + latest_config)
        config_file_handle = open(latest_config, "r")

    except IOError as err:
        sys.stderr.write("Failed to open latest config file " + latest_config + "\n")

    all_lines = config_file_handle.readlines()

    for x in range(0, len(all_lines)):
        line = all_lines[x].rstrip()

        # Did we hit a new vlan?
        match = re.match("vlan ", line)

        if match is not None:
            if ',' not in line:
                vlan_id = line.split()[-1]
                vlan_name = all_lines[x+1].rstrip().split()[-1]
                vlans[vlan_id] = vlan_name
                continue

    return vlans

def main():
    switches = [
    "rd-core-1",
    "fqdr-core-1",
    ]

    # prod_config = get_latest_config(switches[0])
    # dr_config = get_latest_config(switches[1])
    prod_config = "rd-core-1.gw-confg.201709141130"
    dr_config = "fqdr-core-1.gw-confg.201709141130"

    prod_vlans = get_vlans(prod_config)
    dr_vlans = get_vlans(dr_config)

    prod_diff, dr_diff = compare_lists(prod_vlans, dr_vlans)

    print("prod_diff:" + str(len(prod_diff)))
    print("dr_diff:" + str(len(dr_diff)))
    print
    print("On prod, but not dr")
    for pdiff in prod_diff:
        print(pdiff + ' ' + prod_vlans[pdiff])
    print
    print("On dr, but not prod")
    for ddiff in dr_diff:
        print(ddiff + ' ' + dr_vlans[ddiff])

if __name__ == "__main__":
    main()
