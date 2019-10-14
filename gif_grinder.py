#!/usr/bin/python

import os
from os import listdir
from os.path import isfile, join
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import *


mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# assumes second file is "Untitled Document"
# valid file formats

# 00.00 - 00.00
# 00,00 - 00,00

# 00:00.00 - 00:00.00
# 00,00.00 - 00,00.00

# 00:00:00.00 - 00:00:00.00
# 00,00,00.00 - 00,00,00.00

# 00.00 - 00.00 # 0000,0000,0000,0000,0.00
# 00,00 - 00,00 # 0000,0000,0000,0000,0.00

# 00:00.00 - 00:00.00 # 0000,0000,0000,0000,0.00
# 00,00.00 - 00,00.00 # 0000,0000,0000,0000,0.00

# 00:00:00,00.00 - 00:00:00,00.00 # 0000,0000,0000,0000,0.00
# 00,00,00,00.00 - 00,00,00,00.00 # 0000,0000,0000,0000,0.00

file1 = onlyfiles[0]
file2 = onlyfiles[1]
# print '',file1, file2

# max video length in seconds
total_t = 80

contents = ''
cropped = 0
currentgifnumber = 0
scale = ''
videoname = ''

# speed up gif >1, slow down gif <1
# gifspeed = '0.5'
gifspeed = '1'


# convert time to seconds
def get_sec(s):
    vidlen = s.split(':')
    # print "seconds:", s
    # print "micro:" , (float(l[2]) * .001)
    # print "s:", len(l)
    if len(vidlen) == 5:
        # 00:00:00:00.000
        print("1")
        return (int(vidlen[1]) * 604800) + (int(vidlen[1]) * 86400) + (int(vidlen[2]) * 3600) + (float(vidlen[3]) * 60) + (float(vidlen[4]))
    elif len(vidlen) == 4:
        # 00:00:00.000
        print("2")
        return (int(vidlen[0]) * 86400) + (int(vidlen[1]) * 3600) + (float(vidlen[2]) * 60) + (float(vidlen[3]))
    elif len(vidlen) == 3:
        # 00:00.000
        print("3")
        return (float(vidlen[0]) * 3660) + (float(vidlen[1]) * 60) + (float(vidlen[2]))
    else:
        # 00.000
        print("4")
        return (float(vidlen[0]) * 60) + (float(vidlen[1]))


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
        # if scale:
            # disabled, too slow
            # clip = resize(VideoFileClip(videoname), newsize=scale)
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
        print("clip too long.")

# process directory listing
# blank lines are purged
# gif files are skipped
# temp files for moviepy are deleted


for i in onlyfiles:
    # print("file:", i)
    processfile = i
    if "Untitled" in processfile:
        # print processfile
        contents = [contents.rstrip('\n') for contents in open(processfile)]
        # print("Contents1:", contents)
        # replace with generator?
        contents = filter(lambda name: name.strip(), contents)
        # print("Contents2:", contents)
        # contents = filter(None, contents)
        # print("Contents3:", contents)
        # print contents
        # with open(processfile) as f:
        #     contents = f.readlines()
        totalgifs = len(contents)
        # print("total gifs:", totalgifs)
    elif ".gif" in processfile:
        print("")
    elif "ficache" in processfile:
        os.unlink(processfile)
    elif "fispool" in processfile:
        os.unlink(processfile)
    else:
        videoname = i
        shortvideoname = i.split('.')[0]


# parse start end timestamps
for element in contents:
    currentgifnumber += 1
    if currentgifnumber <= totalgifs:
        if element.startswith("#"):
            print("skipping line: ", currentgifnumber)
            print('')

        else:
            # print "element:", element

            if "#" in element:
                cropdata = element.split('#')
                crops = cropdata[-1].split(',')
                x_1 = int(crops[0])
                y_1 = int(crops[1])
                wdt = int(crops[2])
                hgt = int(crops[3])
                if len(crops) >= 5:
                    gifspeed = float(crops[4])
                else:
                    gifspeed = 1
                if len(crops) >= 6:
                    scale = float(crops[5])
                print("x_1:", x_1, "y_1:", y_1, "wdt:", wdt, "hgt:", hgt, "speed:", gifspeed, scale)

                partsdata = cropdata[0].split('-')
                parts = partsdata
                cropped = 1

            else:
                parts = element.split("-")
                cropped = 0

            # print("element:", element)
            # print("parts:", parts)
            starttime0 = str(parts[0]).replace(",", ".").strip()
            endtime0 = str(parts[-1]).replace(",", ".").strip()
            print("0starttime:", starttime0, "endtime:", endtime0)

            starttime = get_sec(starttime0)
            endtime = get_sec(endtime0)
            print("1starttime:", starttime, "endtime:", endtime)

            print("currentgifnumber:", currentgifnumber)
            # print "st:", starttime
            # print "et:", endtime
            # print "video:", videoname
            # print "shortvideoname:", shortvideoname
            # print "parts:", parts
            processGif()

# post process colorize
# convert 1.gif -fill green -tint 100 1b.gif

# use exifdata to get size of image
# do math to sort out image combination spacing and sizing
# convert green.gif -gamma 0.65 -black-threshold 10% green1.gif

# moviepy.video.fx.all.headblur(clip, fx, fy, r_zone, r_blur=None)
# Returns a filter that will blurr a moving part (a head ?) of the frames. The
# position of the blur at time t is defined by (fx(t), fy(t)), the radius of
# the blurring by r_zone and the intensity of the blurring by r_blur. Requires
# OpenCV for the circling and the blurring. Automatically deals with the case
# where part of the image goes offscreen.

# exiftool -ImageSize video.avi
