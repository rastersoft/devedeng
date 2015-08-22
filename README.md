# DEVEDE NG #

## WHAT IS IT? ##

Devede NG is a rewrite of the Devede DVD disc authoring program. This new
code has been writen from scratch, and uses Python3 and Gtk3. It is also
cleaner, which will allow to add new features in the future.


## INSTALLING DEVEDE NG ##

Just type:

	sudo ./setup.py install


## USING DEVEDE NG ##

The second alpha version of Devede NG is very similar to the old devede, with the
exception that, when creating a DVD disc, there are no more "titles" and
"files". Instead, you just add files to the disc. It also lacks support for Mencoder,
and can use only FFMpeg or AVConv for video conversion.

The current visible changes are quite small in number:

* Now allows to add several files at once
* Now makes better use of multicore systems by parallelizing the conversion of several movie files
* The menu edition is interactive
* Has a new "cut" resizing method, to allow to store as widescreen movies with black bars
* Allows to create Matroska files with H.264 video and MP3 audio
* Allows to use VLC, MPV or MPlayer for preview
* Allows to choose between Brasero or K3B for burning the discs
* Allows to set properties for several files in one step
* Allows to choose the subtitle colors
* Allows to choose between MP2 and AC3 audio for menus


## THINGS TO DO ##

Some of the future ideas to add to Devede NG are, without an specific order:

* add more backends
* add more output formats
* allow to replace the movie's audio track with one or several MP3 or OGG audio files
* widescreen menus for DVDs
* preview of a converted menu


## CONTACTING THE AUTHOR ##

Sergio Costas Rodriguez
(Raster Software Vigo)

raster@rastersoft.com

http://www.rastersoft.com

GIT: git://github.com/rastersoft/devedeng.git
