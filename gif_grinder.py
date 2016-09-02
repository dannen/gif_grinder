#!/usr/bin/python

import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import *
from os import listdir
from os.path import isfile, join


mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# assumes second file is "Untitled Document"
# valid file format
# 00:00.00
# 00,00.00
# 00:00.00 - 00:00.00 # 0000,0000,0000,0000
# 00,00.00 - 00,00.00 # 0000,0000,0000,0000

file1 = onlyfiles[0]
file2 = onlyfiles[1]
# print '',file1, file2

# max video length in seconds
total_t = 20

contents = ''
cropped = 0
currentgifnumber = 0
videoname = ''

# speed up gif >1, slow down gif <1
# gifspeed = '0.5'
gifspeed = '1'

# convert time to seconds
def get_sec(s):
    l = s.split(':')
    return float(l[0]) * 60 + float(l[1])
    # alternate for longer videos
    # return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

# convert to gif
def processGif():
    # print "st:", starttime
    # print "et:", endtime
    # print "video:", videoname
    # procvideoname = '"' + videoname + '"'
    # procvideoname = mypath + "/" + videoname

    # clips should be under total_t seconds
    totaltime = endtime - starttime
    if totaltime <= (total_t):

        # print "clip = VideoFileClip(%s).subclip((%s),(%s))" % (videoname, starttime, endtime)
        # print "crop = x_1(%s),y_1(%s),wdt(%s),hgt(%s)" % (x_1, y_1, wdt, hgt)

        # look for cropping information
        if cropped == 1:
            clip = crop(VideoFileClip(videoname).subclip((starttime), (endtime)), x1=(x_1), y1=(y_1), width=(wdt), height=(hgt))
        else:
            clip = VideoFileClip(videoname).subclip((starttime), (endtime))

        # clip = VideoFileClip(procvideoname).subclip((01,59.60),(02,04.24))
        endfile = shortvideoname + "_" + str(currentgifnumber) + ".gif"
        # optendfile = shortvideoname + "_opt_" + str(currentgifnumber) + ".gif"
        # print "endfile:", endfile
        clip.subclip().speedx(float(gifspeed)).write_gif(endfile, loop=1)

        # post process compression
        # gifsicle = "gifsicle --colors 256 -O3 " + endfile + " -o " + optendfile
        # print "gifsicle:", gifsicle
        # gifsicle = ["/usr/bin/gifsicle /-/-colors 256 /-O3", endfile, "/-o", optendfile]
        # call(gifsicle)

    else:
        print "clip too long."

# process directory listing
# blank lines are purged
# gif files are skipped
# temp files for moviepy are deleted
for i in onlyfiles:
    processfile = i
    if "Untitled" in processfile:
        # print processfile
        contents = [contents.rstrip('\n') for contents in open(processfile)]
        contents = filter(lambda name: name.strip(), contents)
        contents = filter(None, contents)
        # print contents
        # with open(processfile) as f:
        #     contents = f.readlines()
    elif "gif" in processfile:
        print ""
    elif "ficache" in processfile:
        os.unlink(processfile)
    elif "fispool" in processfile:
        os.unlink(processfile)
    else:
        videoname = i
        shortvideoname = i.split('.')[0]

totalgifs = len(contents)
print "total gifs:", totalgifs

# parse start end timestamps
for element in contents:
    currentgifnumber += 1
    if currentgifnumber <= totalgifs:
        if "#" in element:
            cropdata = element.split('#')
            crops = cropdata[-1].split(',')
            x_1 = int(crops[0])
            y_1 = int(crops[1])
            wdt = int(crops[2])
            hgt = int(crops[3])
            print "x_1:", x_1, "y_1:", y_1, "wdt:", wdt, "hgt:", hgt

            partsdata = cropdata[0].split('-')
            parts = partsdata
            cropped = 1

        else:
            parts = element.split("-")
            cropped = 0
        # print "parts:", parts
        starttime0 = str(parts[0]).replace(",", ":").strip()
        endtime0 = str(parts[-1]).replace(",", ":").strip()
        print "starttime:", starttime0, "endtime:", endtime0
        starttime = get_sec(starttime0)
        endtime = get_sec(endtime0)
        print "starttime:", starttime, "endtime:", endtime


        print "currentgifnumber:", currentgifnumber
        # print "st:", starttime
        # print "et:", endtime
        # print "video:", videoname
        # print "shortvideoname:", shortvideoname
        processGif()
