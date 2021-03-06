#!/usr/bin/python
# -*- coding: utf-8 -*-
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from multiprocessing import Lock, Queue
from pprint import pprint
from threading import Thread

import requests
from lxml import html

# Threads waiting to process
processing_queue = Queue(5000)
processing_finished = False
print_lock = Lock()


def get_url(response):
    """
    Grab a URL from a moss call
    Regex Source:
    http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    """
    urls = re.findall(r"""http[s]?://(?:[a-zA-Z]|
            [0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]
            [0-9a-fA-F]))+""",
                      response)
    urls_len = len(urls)
    if urls_len > 0:
        # Only one URL should be returned
        return urls[0]
    else:
        # No results in URL - bad request
        raise ValueError("No URL")

def get_percentages(url):
    """Get all percentages from a moss URL"""
    # Get page content
    page = requests.get(url)
    content = page.content
    # Find percent in content
    percentages = re.findall('[0-9]+%', content)
    return percentages



def get_high_percentages(url, cutoff):
    """Scrape a moss URL to find the highest percentage match"""
    # No high values by default
    high_score = False
    percentages = get_percentages(url)
    # Search through resulting percentages for values past cutoff
    percentages_len = len(percentages)
    if percentages_len > 0:
        for score in percentages:
            score = int(score.strip('%'))
            if score > cutoff:
                # High value result
                high_score = True
    return high_score



def process_queue():
    """Process queue"""
    global processing_finished
    global processing_queue


    try:
        while (True):
            row = processing_queue.get()
            if (row.has_key("finished_processing")):
                print "Finished processing."
                break
            else:
                compare_files(row["new_file"], row["old_file"], row["output_filename"])
    except KeyboardInterrupt:
        print ("here")
        print traceback.format_exc()
        raise

def compare_files(_old, _new, output_filename):
    """See if two files should be compared. Compare them if they are"""
    global print_lock
    global processing_queue

    cutoff = 50

    try:
        old_matches = []
        new_matches = []

        for root, dirnames, filenames in os.walk(_old):
            for filename in filenames:
                if filename.endswith(('.php', '.js', '.css', '.html', '.py', '.txt')):
                    old_matches.append(os.path.join(root, filename))
        for root, dirnames, filenames in os.walk(_new):
            for filename in filenames:
                if filename.endswith(('.php', '.js', '.css', '.html', '.py', '.txt')):
                    new_matches.append(os.path.join(root, filename))
        old_matches_len = len(old_matches)
        new_matches_len = len(new_matches)
        if (old_matches_len < 1 or new_matches_len < 1):
            return

        # Make temporary directory for files.
        # Must put all files in the same directory because wildcard directory syntax
        # has not been working in this situation.
        old_temp = tempfile.mkdtemp()
        new_temp = tempfile.mkdtemp()


        # Move matches to temporary folder
        for match in old_matches:
            shutil.copy(match, old_temp)
        for match in new_matches:
            shutil.copy(match, new_temp)

        old_files = str(old_temp) + "/*"
        new_files = str(new_temp) + "/*"


        # Call MOSS from command line
        response = subprocess.check_output("moss/moss -d " + str(old_files)
                                           + " " +str(new_files), shell=True)
        # Get response from command

        # TODO: Add error handling
        url = get_url(response)

        high_score = get_high_percentages(url, cutoff)
        if high_score:
            percentages = get_percentages(url)
            print '****************'
            print '***** ALERT ****'
            print '****************'
            print _new
            print _old
            for _score in percentages:
                print _score
            print url
            with open(output_filename, 'a') as file:
                file.write('******' + '\n')
                file.write(_new + '\n')
                file.write(_old + '\n')
                file.write(url + '\n')
                for _score in percentages:
                    file.write(str(_score) + '\n')
        else:
            print_lock.acquire()
            print "Okay: " + url
            print "Approximately " + str(processing_queue.qsize()) + " left to process \n"
            print_lock.release()
    except Exception:
        print traceback.format_exc()
    return


def moss_compare(new_dirs, old_dirs):
    """Send moss request"""
    global processing_queue
    global processing_finished

    try:
        # Write output to file
        output_filename = sys.argv[1] + '_comp_' + sys.argv[2] + '.txt'
        # print 'Writing output to ' + output_filename

        # For loop: m * n filepaths
        for _new in new_dirs:
            for _old in old_dirs:
                if _new != _old:
                    processing_queue.put({"new_file": _new,
                                          "old_file": _old,
                                          "output_filename": output_filename})

        print "Queue populated. Approximately " + str(processing_queue.qsize()) + " in queue"

        processing_queue.put({
            "finished_processing": True
        })

        while True:
            row = processing_queue.get()

            if row.has_key("finished_processing"):
                print "Finished processing."
                break
            else:
                compare_files(row["new_file"], row["old_file"], row["output_filename"])

    except KeyboardInterrupt:
        print "cancelled"
        processing_finished = True
        sys.exit(0)



def get_extension(file_path):
    """Grab file extension"""
    extension = os.path.splitext(file_path)[1]
    return extension


def walk(substring):
    """Return files with matched name"""
    matched_files = []
    _dir = os.getcwd() + '/repositories'

    for subdirectory in os.listdir(_dir):
        path = os.path.join(_dir, subdirectory)
        if substring in path:
            matched_files.append(path)

    return matched_files



def print_usage():
    """Usage"""
    print 'USAGE:'
    print 'python file-walker.py [new modules] [old modules]'
    print "  Grab files whose full path contains the given substring, such as 'spring2015-module1'"


## MAIN
if __name__ == '__main__':
    if len(sys.argv) > 2:
        OLD_FILES = walk(sys.argv[1])
        print 'Grabbed ' + str(len(OLD_FILES)) + ' old directories'

        NEW_FILES = walk(sys.argv[2])
        print 'Grabbed ' + str(len(NEW_FILES)) + ' new directories'
        moss_compare(NEW_FILES, OLD_FILES)
    else:
        print_usage()
