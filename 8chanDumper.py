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
SUBJECT = ""
EMAIL = ""
NAME = ""
HIDE_FLAG = "on"
POST_WAIT = 8
ALLOWED_FILE_TYPES = tuple(board_settings.allowed_extensions)

current_file = 0


def file_upload_monitor(monitor):
	sys.stdout.write("\r     {0} out of {1} Bytes Uploaded... ".format(monitor.bytes_read, monitor.len))
	sys.stdout.flush

# Get a sorted list of filenames
filenames = [f for f in listdir(DIRECTORY) if isfile(join(DIRECTORY, f)) and f.endswith(ALLOWED_FILE_TYPES)]
filenames.sort()

print("\nDirectory: \"{0}\", Board: /{1}/, Thread: {2}".format(DIRECTORY, BOARD, THREAD))
print("Allowed extensions: {0} (files that are not allowed have been automatically ignored)".format(', '.join(board_settings.allowed_extensions)))
print("Max files per post: {0}, Files to upload: {1}, Posts to make: {2}\n".format(board_settings.max_files, len(filenames), math.ceil(len(filenames) / board_settings.max_files)))
print("\nBeginning dump from directory \"{0}\" to https://8ch.net/{1}/res/{2}.html\n".format(DIRECTORY, BOARD, THREAD))

while current_file < len(filenames):
	# Collect filenames to post
	filenames_to_post = filenames[current_file:current_file+board_settings.max_files]
	current_file += board_settings.max_files

	# Build post:
	data = [("board", BOARD),
	        ("thread", THREAD),
	        ("post", "New Reply"),
	        ("body", ""),
	        ("subject", SUBJECT),
	        ("name", NAME),
	        ("no_country", HIDE_FLAG),
	        ("json_response", "1"), #debugging
	        ("email", EMAIL)]
	for index, filename in enumerate(filenames_to_post):
		filenumber = str(index + 1) if index != 0 else ""
		data.append(("file{0}".format(filenumber), (filename, open(join(DIRECTORY, filename), "rb"))))

	m = MultipartEncoderMonitor(MultipartEncoder(data), file_upload_monitor)

	# Send post:
	print("Sending post, please wait! ... ")
	r = requests.post("https://8ch.net/post.php",
		data=m,
		headers = {"referer": "https://8ch.net", "Content-Type": m.content_type})

	# Check if post was sent
	#print(r.request.headers)
	#print(r.json())

	# Wait however long we need to not hit flood detection (usually 10 seconds)
	print("Sent! Please wait for flood detection ... ", end="", flush=True)
	for x in range(0, POST_WAIT):
		time.sleep(1)
		print(str(x + 1) + "... ", end="", flush=True)
	files_left = len(filenames) - current_file
	print("Current Iteration: {0}, Files left: {1} Posts left: {2}".format(current_file, files_left, math.ceil(files_left / board_settings.max_files)))
