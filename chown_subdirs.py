#!/usr/bin/python

import argparse
import os
import pwd
import grp

# Use argparse to make the user supply a directory
parser = argparse.ArgumentParser(description='Chown sub directories to the same as the parent directory.')
parser.add_argument('--directory', help='the directory to start from', required=True)
parser.add_argument('--verbose', help='verbose output', action='store_true')

# Parse arguments
args = parser.parse_args()

# Check if the directory exits
if (os.path.exists(args.directory) == False):
	exit("\033[31mThe directory do not exist")

# Method for verbose output
def verbose_output(directory, uid, gid):
	if (args.verbose):
		user = pwd.getpwuid(uid).pw_name
		group = grp.getgrgid(gid).gr_name
		print "\033[33mChowning " + directory + " to " + user + ":" + group


# Method for chowning every directory and file
def chown_sub_directory(directory, uid, gid):
	for root, dirs, files in os.walk(directory):
		for _dir in dirs:
			os.chown(os.path.join(root, _dir), uid, gid)
			verbose_output(os.path.join(root, _dir), uid, gid)
		for _file in files:
			os.chown(os.path.join(root, _file), uid, gid)
			verbose_output(os.path.join(root, _file), uid, gid)

# Get every directory in the parent directory
# We'll read the uid and gid, and then chown them independently
for _dir in os.listdir(args.directory):
	if not _dir.startswith('.'):

		# Get full path
		_dir = os.path.join(args.directory, _dir)
		
		# Get the user and group of the directory
		uid = os.stat(_dir).st_uid
		gid = os.stat(_dir).st_gid

		# Do the chowning
		chown_sub_directory(_dir, uid, gid)

# We're done
print "\033[32mWe're done"
