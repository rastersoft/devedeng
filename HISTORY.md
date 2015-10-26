## History of versions ##

* version 4.3 (2015-10-26)
  * Now doesn't fail when creating a DVD without menu
  * Added help in html format

* version 4.2 (2015-09-08)
  * Now can work with old and new versions of AVConv
  * Added extra debug code to be able to track problems with MKV files

* version 4.1 (2015-06-30)
  * Fixed dependencies in package
  * Trying to fix a bug with MKV files (incorrect stream assign)

* version 4.0 (2015-04-26)
  * First stable version of DevedeNG

* version 0.1.0 beta 12 (2015-02-01)
  * Now uses the version number available in the CONFIGURATION_DATA file for the setup process
  * Fixed the icon name in the .desktop file

* version 0.1 beta 11 (2015-01-29)
  * Now allows to automatically generate a debian package
  * Renamed the module from 'devede' to 'devedeng'
  * Renamed some files to avoid clashing with the 'classic devede' debian package.

* version 0.1 beta 10 (2015-01-22)
  * Now jumps to the desired next video when the current movie ends and the creator set it to jump to another menu entry

* version 0.1 beta 9 (2015-01-16)
  * Now doesn't fail with AVPROBE or FFPROBE if a file doesn't have streams

* version 0.1 beta 8 (2014-12-28)
  * Added an extra fix for AVPROBE and FFPROBE, using the human readable strings to get the duration
  * Cleaner code for AVPROBE and FFPROBE
  * Removed devedesans.ttf file
  * Updated the setup.py file

* version 0.1 beta 7 (2014-12-28)
  * Moved the priority of MPLAYER over AVPROBE and FFPROBE until I discover what is happening with some data fields

* version 0.1 beta 6 (2014-12-27)
  * Fixed AVPROBE and FFPROBE command line

* version 0.1 beta 5 (2014-12-27)
  * Added support for MPV as movie player
  * Added support for ffprobe and avprobe as movie info detector

* version 0.1 beta 4 (2014-12-25)
  * Now ensures that the maximum bitrate is honored
  * Added the maximum bitrates for each available format

* version 0.1 beta 3 (2014-12-21)
  * Fixed the subtitle colors
  * Now puts the video and audio streams in the right order

* version 0.1 beta 2 (2014-12-07)
  * Fixed a bug when jumping to a video not visible in the main menu
  * Fixed a bug when the main menu has two or more pages
  * Default size for main window bigger
  * Allows to change the title by double-clicking on it
  * Shows the duration of each title

* version 0.1 beta 1 (2014-09-22)
  * Fixed several strings in the menu
  * Fixed the bug that prevented to choose the final folder
  * Removed single quotes that triggered an exception when creating a DVD without menu

* version 0.1 alpha 2 (2014-08-13)
  * Updated spanish translation and added POTFILES.in file
  * Allows to choose between MP2 and AC3 audio for menus
  * Now only deletes the bare minimum files and folders to be able to create a disk in the specified final folder
  * Better message text to specify which folder will be deleted when the final folder already exists
  * It failed when the selected backend was not installed in the system. Fixed.
  * Now shows a default value for preview duration
  * Fixed progress bar for subtitle creation
  * Allows to choose the subtitle colors
  * Allows to set properties for several files in one step
  * Fixed bug when setting PAL or NTSC toggle in file properties
  * Added two-pass conversion
  * Now detects separately MKISOFS and GENISOIMAGE, allowing to have only one of them installed in the system
  * Now checks that the number of files is smaller than the limit for DVD projects
  * Now uses GLib for DBus instead of python-dbus
  * Fixed the DESKTOP file to ensure that an icon is shown in the applications menu

* version 0.1 alpha 1 (2014-08-06)
  * First public version
