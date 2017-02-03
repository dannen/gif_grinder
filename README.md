# gif_grinder
A python script to serially create gifs from a movie file using a reference list.

gif_grinder is an over-script which parses a single flat text file that resides in the same directory as a movie file (avi, mkv, mpeg, etc.), to create a series of animated gifs based on the beginning and ending time values in said file.

The script utilizes https://github.com/Zulko/moviepy and https://github.com/FFmpeg/FFmpeg to carve out animated gifs from any movie file that FFmpeg can parse.

I typically grab the timestamps from vlc (http://www.videolan.org/vlc/index.html) using the Jump to time plugin "https://addons.videolan.org/content/show.php/Jump+to+time+(Previous+frame)+v2.1?content=156396".

The time length of the animated gifs is set by altering the "total_t" value in the script to you desired maximum length of time.  Times under 20 seconds are recommended as longer length gifs tend to create 100Mb+ files.

"gifspeed" can be changed to a float value ranging from 0.01 to 10+.  The smaller the number, the slower the gif.  Every above 1, multiplies the speed by that number.  2 is twice as fast. 5 is five times faster.

The text file format is as follows:

start - finish # cropstart_x, cropstart_y, crop_width, crop_height, speed
> 00:00:00.00 - 00:00:00.00<br>
>    00:00.00 - 00:00.00<br>
>       00.00 - 00.00<br>
>
> 00:00.00 - 00:00.00 # 0000,0000,0000,0000,0.00<br>
> 00,00.00 - 00,00.00 # 0000,0000,0000,0000,0.00<br>

Leaving out the crop values is completely valid.

Expected time values are as follows:

> minutes:seconds.microseconds<br>
> minutes,seconds.microseconds

The gifs will be created using the name of the movie file with an incremental value appended.

> mymovie.mpg

creates:

> mymovie1.gif<br>
> mymovie2.gif

from a text file containing:

> 00:01.00 - 00:04.00<br>
> 00:06.01 - 00:10.15

If the calculated time value in your text file exceeds the maximum time (total_t), a warning message will be printed and creation of the gif will be skipped.

Currently the script looks for a file named "Untitled" as for the list of times and cropping.  It can be "Untitled Document", "Untitled file", or any other file where the name contains the exact word "Untitled".


*files with "gif" in the name (not just the suffix) will be skipped.
*files containing "ficache" or "fispool" will be deleted as the script assumes they were leftover from a previous failed run of the gif_grinder script.
