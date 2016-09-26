#!/usr/bin/python
# -*- coding: utf-8 -*-

# If you encounter any problems please make an issue on https://github.com/fixpls/8chanDumper/issues/new or make a new thread on /test/ (https://8ch.net/test)

import requests, time, os, sys, math, argparse
from os import listdir
from os.path import isfile, join
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import DumpHelper

parser = argparse.ArgumentParser(description="Directory dump to 8chan with multiple-file posts")

parser.add_argument('directory', action="store", type=str, help="Path to the directory with the files you wish to dump")
parser.add_argument('board', action="store", type=str, help="8chan board you wish to post to (e.g. for /test/ put test)")
parser.add_argument('thread', action="store", type=int, help="Thread number to post to (e.g. for https://8ch.net/test/res/34429.html put 34429)")
parser.add_argument('-s', '--subject', action='store', type=str, default="", dest='subject', help="Set the Subject to use for each post")
parser.add_argument('-e', '--email', action='store', type=str, default="", dest='email', help="Set the Email to use for each post")
parser.add_argument('-n', '--name', action='store', type=str, default="", dest='name', help="Set the Name to use for each post")
parser.add_argument('-S', '--spoiler', action='store_true', default=False, dest='spoiler', help="Set 8chanDumper to spoiler all files (by default files are not spoilered)")
parser.add_argument('-p', '--password', action='store', type=str, default="", dest='password', help="Set the Password to use for each post")
parser.add_argument('-f', '--userflag', action='store', type=str, default="", dest='userflag', help="Set the Userflag to use for each post (input the Userflag's ID, for 8chan this is a unix timestamp e.g. 1424645719083) (note, may increase chance of triggering flood detection on 8chan)")
parser.add_argument('-c', '--countryflag', action='store_true', default=False, dest='countryflag', help="Set 8chanDumper to show your countryflag for all posts (by default countryflags are hidden if possible)")
parser.add_argument('-w', '--wait', action='store', type=int, default=8, dest='wait', help="Set how long we should wait between each post (by default 8 seconds seems to be good enough to respect 8chan's flood detector, lower this if you are sure each post will take a while to upload. Beware, too low and posts many not get through)")
parser.add_argument('-u', '--useragent', action='store', type=str, default="", dest='user_agent', help="Set the User Agent to use with the website")
parser.add_argument('-W', '--website', action='store', type=str, default="https://8ch.net", dest='website', help="Set which website to use (by default uses \"https://8ch.net\")")
parser.add_argument('-m', '--maxfiles', action='store', type=int, default=9999, dest='max_files', help="Set how many files to post per post (limited by however many the board allows)")
parser.add_argument('-r', '--resume', action='store', type=int, default=0, dest='resume', help="Resume from a specific upload position, start = 0 (a value of \"0\" will start uploading from the 1st file in the sorted list, \"1\" from the 2nd and so on)")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 2016.09.26')

results = parser.parse_args()

if results.thread == None:
    print(results)
    exit()

board_settings = DumpHelper.BoardSettings(results.board)
if board_settings.captcha_enabled:
	print("/{0}/ has captcha-per-post enabled, cannot post!".format(results.board))
	exit()

DIRECTORY = results.directory # e.g. "/home/test/pictures"
BOARD = results.board # e.g. "test"
THREAD = str(results.thread) # e.g. "34429"
SUBJECT = results.subject
EMAIL = results.email
NAME = results.name
PASSWORD = results.password
USERFLAG = str(results.userflag)
SPOILER = results.spoiler
COUNTRYFLAG = results.countryflag
POST_WAIT = results.wait
USER_AGENT = results.user_agent
WEBSITE = results.website
MAX_FILES = board_settings.max_files if results.max_files > board_settings.max_files else results.max_files
ALLOWED_FILE_TYPES = tuple(board_settings.allowed_extensions)

current_file = results.resume


def file_upload_monitor(monitor):
	sys.stdout.write("\r     {0} out of {1} Bytes Uploaded... ".format(monitor.bytes_read, monitor.len))
	sys.stdout.flush

# Get a sorted list of filenames
filenames = [f for f in listdir(DIRECTORY) if isfile(join(DIRECTORY, f)) and f.endswith(ALLOWED_FILE_TYPES)]
filenames.sort()

print("\nDirectory: \"{0}\", Board: /{1}/, Thread: {2}".format(DIRECTORY, BOARD, THREAD))
print("Allowed extensions: {0} (files that are not allowed have been automatically ignored)".format(', '.join(board_settings.allowed_extensions)))
print("Max files per post: {0}, Files to upload: {1}, Posts to make: {2}\n".format(MAX_FILES, len(filenames), math.ceil(len(filenames) / MAX_FILES)))
print("\nBeginning dump from directory \"{0}\" to {1}/{2}/res/{3}.html\n".format(DIRECTORY, WEBSITE, BOARD, THREAD))

while current_file < len(filenames):
	# Collect filenames to post
	filenames_to_post = filenames[current_file:current_file+MAX_FILES]
	current_file += MAX_FILES

	# Build post:
	data = [("board", BOARD),
	        ("thread", THREAD),
	        ("post", "New Reply"),
	        ("body", ""),
	        ("subject", SUBJECT),
	        ("name", NAME),
	        ("json_response", "1"), #debugging
	        ("email", EMAIL)]
	if SPOILER:
		data.append(("spoiler", "on"))
	if PASSWORD:
		data.append(("password", PASSWORD))
	if USERFLAG:
		data.append(("user_flag", USERFLAG))
	if not COUNTRYFLAG:
		data.append(("no_country", "on"))
	for index, filename in enumerate(filenames_to_post):
		filenumber = str(index + 1) if index != 0 else ""
		data.append(("file{0}".format(filenumber), (filename, open(join(DIRECTORY, filename), "rb"))))

	m = MultipartEncoderMonitor(MultipartEncoder(data), file_upload_monitor)

	# Send post:
	print("Sending post, please wait! ... ")
	r = requests.post("{0}/post.php".format(WEBSITE),
		data=m,
		headers = {"referer": WEBSITE, "Content-Type": m.content_type, "User-Agent": USER_AGENT})

	# Check if post was sent
	#print(r.request.headers)
	#print(r.json())

	# Wait however long we need to not hit flood detection (usually 10 seconds)
	print("Sent! Please wait for flood detection ... ", end="", flush=True)
	for x in range(0, POST_WAIT):
		time.sleep(1)
		print(str(x + 1) + "... ", end="", flush=True)
	files_left = len(filenames) - current_file
	print("Files uploaded: {0}, Files left: {1} Posts left: {2}".format(current_file, files_left, math.ceil(files_left / MAX_FILES)))