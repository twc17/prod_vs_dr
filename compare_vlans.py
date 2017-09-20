#!/usr/bin/python

# Title: compare_vlans.py
#
# Author: Lucci <lucci@pitt.edu>
# Author: Troy <twc17@pitt.edu>
# Date Updated: 09/20/2017
# Version: 1.3.4
#
# Purpose:
#   Compare VLANs from RIDC Production and the DR site
#
# Dependencies:
#   python 2.6.6+
#
# Usage:
#   python compare_vlans.py [-h]
#
# TODO:
#   Clean up output and add arg parser

import os, re, sys, glob

def compare_lists(list1, list2):
    """Compare two different lists.

    Arguments:
    list1 -- the first list to be compared
    list2 -- the second list to be compared

    Returns:
    Two lists, the differences between the original lists
    """
    # List comprehension. Google it
    return [[item for item in list1.keys() if not item in list2.keys()], [item for item in list2.keys() if not item in list1.keys()]]

def get_latest_config(switch):
    """Grab the latest config file for a specific switch

    Arguments:
    switch -- name of the switch to grab the config file for

    Returns:
    Name of the config file
    """
    highest_mtime = int()

    # Loop through all of the config files for the given switch to determine
    # which one is the most recent
    # Note we keep all of the config files in the same location
    for config_file in glob.iglob("/tftpboot/ciscoconfg/" + switch + ".gw*"):

        mtime = os.stat(config_file).st_mtime

        if mtime > highest_mtime:
            latest_config = config_file

            highest_mtime = mtime

    # Latest config file based on date and time
    return latest_config

def get_vlans(latest_config):
    """Get all of the VLAN IDs and names from a given cisco config file

    Arguments:
    latest_config -- the latest config file to search through

    Returns:
    Dictionary of VLAN IDs and names in the following format
    vlans[ID] = NAME
    """
    vlans = {}

    try:
        # Try to open the latest config file for reading only
        config_file_handle = open(latest_config, "r")

    except IOError as err:
        # Something went wrong opening the file
        print("Failed to open latest config file " + latest_config + "\n")

    # Read all lines of the config file into one string
    # We do this because it's easier to grab the next line
    # after the current one while going through the 'for' loop
    all_lines = config_file_handle.readlines()

    # Loop through each line in the config
    for x in range(0, len(all_lines)):
        # This makes the string easier to work with
        line = all_lines[x].rstrip()

        # Check to see if we found the word 'vlan' in the given line
        match = re.match("vlan ", line)

        if match is not None:
            # We only want the lines in the cisco config that read
            # 'vlan, NUM' so we search for the ',' character in the line
            if ',' not in line:
                vlan_id = line.split()[-1]
                vlan_name = all_lines[x+1].rstrip().split()[-1]
                # Assign ID = NAME
                vlans[vlan_id] = vlan_name
                continue

    # vlans[ID] = NAME
    return vlans

def main():
    """Main program logic

    1 -- Grab the latest config files
    2 -- Search config files for VLAN IDs and names
    3 -- Compare PROD and DR VLAN IDs
    4 -- Output diffs
    """
    # Switches that we are going to compare to
    # Note that if these names ever change PROD needs to go first,
    # DR second
    switches = [
    "rd-core-1",
    "fqdr-core-1",
    ]

    # 1
    prod_config = get_latest_config(switches[0])
    dr_config = get_latest_config(switches[1])

    # 2
    prod_vlans = get_vlans(prod_config)
    dr_vlans = get_vlans(dr_config)

    # 3
    prod_diff, dr_diff = compare_lists(prod_vlans, dr_vlans)

    # 4
    print("Latest PROD Config: " + prod_config)
    print("Latest DR Config: " + dr_config)
    print
    print("prod_diff:" + str(len(prod_diff)))
    print("dr_diff:" + str(len(dr_diff)))
    print
    print("On PROD, but NOT on DR")
    for pdiff in prod_diff:
        print(pdiff + ' ' + prod_vlans[pdiff])
    print
    print("On DR, but NOT on Prod")
    for ddiff in dr_diff:
        print(ddiff + ' ' + dr_vlans[ddiff])

# RUN!
if __name__ == "__main__":
    main()
