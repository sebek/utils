#!/usr/bin/python

import argparse
import os
import sys

# Use argparse to make the user supply a directory
parser = argparse.ArgumentParser(description='Batch create users from list.')
parser.add_argument('--file', help='file with users (username:password)', required=True)
parser.add_argument('--shell', help='what shell to use')
parser.add_argument('--group', help='user group')
parser.add_argument('--permissions', help='permissions for homedir')

# Parse arguments
args = parser.parse_args()

# Method for adding user
def user_add (username, homedir, shell, group):
    cmd = "useradd -s " + shell + " -g " + group + " -d " + homedir + " " + username
    os.system(cmd)

# Method for setting password
def set_password (username, password):
    cmd = "echo " + username + ":" + password + " | chpasswd"
    os.system(cmd)

# Set permissions for directory
def set_permissions (directory, username, group, permissions):
    cmd = "chown " + username + ":" + group + " " + directory + " | chmod " + permissions + " " + directory
    os.system(cmd)


# Method for creating a directory
def create_directory (directory):
    # Create homedir
    cmd = "mkdir " + directory
    os.system(cmd)


# Check if the directory exits
if (os.path.isfile(args.file) == False):
	exit("\033[31mThe file with username passwords is missing")

# Set shell, group and permissions
shell = args.shell if args.shell else '/bin/bash'
group = args.group if args.group else 'users'
permissions = args.permissions if args.permissions else '775'

# Read the file content
file = open(args.file, 'r').read().split("\n")

# Create and set password for all users
for row in filter(len, file):
    username, password, homedir, sub_directories = row.split(':')
    sub_directories = sub_directories.split(',')


    user_add(username, homedir, shell, group)
    print "Adding " + username

    set_password(username, password)
    print "Setting password for " + username

    create_directory(homedir)
    print "Creating homedir for " + username

    set_permissions(homedir, username, group, permissions)
    print "Setting permissions for " + homedir

    for sub_directory in sub_directories:

        full_path = homedir + "/" + sub_directory

        create_directory(full_path)
        print "Creating sub_directory " + full_path

        set_permissions(full_path, username, group, permissions)
        print "Setting permissions for " + full_path


# We're done
print "\033[32mWe're done"
