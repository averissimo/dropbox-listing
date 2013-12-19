#!/bin/python

# must download from dropbox at start and upload when it finishes

import json, datetime
from os import listdir, remove
from os.path import isdir, join, isfile
import sys, getopt, datetime

dir_files = ["series","movies","music","anime"]
base_path = "/home/averissimo/work/dropbox_list"
json_file = join(base_path,"listing.json")
change_to = "change for action"


def delete_file(path,deleted):
	deleted["deleted"] += [{"path": path, "date": datetime.datetime.now().strftime("%c")}]
	#print "remove( " + path + "  )"
	remove( path )

def describe_folder(path,json_base,only_files,data):

	if "files" not in json_base:
		json_base["files"] = {}
	#	
	for file_name in listdir(path):
		file_name_path = join(path,file_name)
		if only_files and isdir(file_name_path):
			continue
		#
		if file_name not in json_base["files"]:
			json_base["files"][file_name] = {"path": file_name_path , "delete?": change_to, "upload": change_to }
		#
#		if json_base["files"][file_name]["upload"] != change_to:
			# upload file to dropbox
		#
		if json_base["files"][file_name]["delete?"] != change_to:
			delete_file( json_base["files"][file_name]["path"] , data )
		else:
			json_base["files"][file_name]["exists"] = True
	#
	for leave in json_base["files"].keys():
		aux = json_base["files"][leave]
		# delete node if "exists" flag does exists
		if "exists" in aux:
			del(aux["exists"])
		else:
			del(json_base["files"][leave])

def load_json():

	# load json if available
	try:
		json_data = open(json_file)
		data = json.load(json_data)
	except (IOError, ValueError):
		data = {}

	if "deleted" not in data:
		data["deleted"] = []

	for name in dir_files:
		dir_path = join(base_path,name)
		# check if key exists
	
		if not isdir(dir_path):
			continue

		if name not in data:
			data[name] = dict()
		# lists folder

		describe_folder(dir_path, data[name],True,data)

		for f in listdir(dir_path):
			sub_path = join(dir_path,f)
			#
			if not isdir(sub_path):
				continue	
			if f not in data[name]:
				data[name][f] = {}
			# path for dir
			data[name][f]["path"] = sub_path
			# files
	
			describe_folder(sub_path, data[name][f],False,data)
	#
	return data

def write(data):
	no_write = False
	dump = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
	if not no_write:
		json_data = open(json_file,"wb")
		json_data.write(dump)
		json_data.close()
	else:
		print dump



def main(argv):
	data = load_json()
	write(data)


if __name__ == "__main__":
	main(sys.argv[1:])
