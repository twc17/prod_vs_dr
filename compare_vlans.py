#!/usr/bin/env python
# Description: Check that vlans match on PROD and DR
# Author: Lucci
# Author: Troy <twc17@pitt.edu>
# Date Updated: 09/15/2017
# Version: 1.1.1

import os, re, sys, glob
from optparse import OptionParser


switches = {
  "rd-core-1" : {},
  "fqdr-core-1" : {}
}


parser = OptionParser("%prog [options] $nodes\nCheck that vlans on switches match")

parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Verbose mode")

(options, args) = parser.parse_args()



# Compare two lists for differences
def compare_lists(list1, list2):
    # List comprehension. Returns two lists, with only the differences between the original lists
    return [[item for item in list1 if not item in list2], [item for item in list2 if not item in list1]]

#
# Get latest configs
#
def get_latest_config(switch):
    if options.verbose is True: sys.stdout.write("Finding the latest config files ...\n")

    latest_config = ""

    for config_file in glob.iglob("/tftpboot/ciscoconfg/" + switch + ".gw*"):
        if options.verbose: sys.stdout.write("Checking file " + config_file + " ...\n")

        mtime = os.stat(config_file).st_mtime

        if mtime > highest_mtime:
            latest_config = config_file

            highest_mtime = mtime

    return latest_config


#
# Loop through configs looking for vlans
#
def get_vlans(latest_config):
    if options.verbose is True: sys.stdout.write("Reading the latest config files ...\n")


    vlans = []

    try:
        print ("Latest config: " + latest_config)
        config_file_handle = open(latest_config, "r")

    except IOError as err:
        sys.stderr.write("Failed to open latest config file " + latest_config + "\n")

    for line in config_file_handle:
        line = line.rstrip()

        # Did we hit a new vlan?
        match = re.match("vlan ", line)

        if match is not None:
            if ',' not in line:
                vlan.append(line.split()[-1])
                if options.verbose is True: sys.stdout.write("Found a vlan " + vlan[-1] + "\n")
                continue

        # I don't think this code is actually doing anyting...?
        # find next vlan
        # match = re.match(" name", line)

        # if match is not None:
         #   if options.verbose is True: sys.stdout.write("Found a new vlan " + vlan + " : " + line + "\n")

         #   current_vlan_list = vlans_dict[vlan]

         #   current_vlan_list.append(line)

    # config_file_handle.close()

def main():
    for switch in switches:
        switches[switch]


# main():
# for each switch in switch_list
#   get the latest configs
#   search configs for VLANs
# compare lists and output diffs
