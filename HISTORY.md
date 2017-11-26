## History of versions ##
* version 4.8.10 (2017-11-26)
  * Removed minrate during second pass when using two-pass encoding because it fails with ffmpeg

* version 4.8.9 (2017-07-10)
  * Fixed bug when there are no CD burner installed

* version 4.8.8 (2017-02-07)
  * Fixed genisoimage bug with some locales

* version 4.8.7 (2017-01-29)
  * Allows to translate the "Play all" text in the DVD menu
  * Fixed mkisofs bug with some locales

* version 4.8.6 (2016-12-14)
  * Now ensures that the average bitrate is never smaller than the minimum bitrate
  * Now the matroska and divx files have the right extension

* version 4.8.5 (2016-11-24)
  * Fixed a bug when loading a project file (thanks to RecursiveProgrammer)
  * Updated the german translation

* version 4.8.4 (2016-11-03)
  * Allows to set if a movie is shown or not in the DVD menu from the main window

* version 4.8.3 (2016-10-16)
  * Fixed the problem fixed bitrate problem with FFMpeg and AVConv (thanks to Juniorsnet)

* version 4.8.2 (2016-09-24)
  * Fixed a problem when adding several subtitles to the same movie (thanks to Rocco Barisci)

* version 4.8.1 (2016-09-05)
  * Fixed a float value used for volume where it expected an integer

* version 4.8.0 (2016-08-12)
  * Fixed a division by zero when a clip has a duration of less than one second

* version 4.7.1 (2016-07-17)
  * Updated translations

* version 4.7.0 (2016-04-24)
  * Fixed a bug when creating the subtitles'XML: now ensures that an integer value is passed

* version 4.6.1 (2016-03-14)
  * Fixed translations

* version 4.6.0 (2016-03-13)
  * Fixed a bug when using the Play all option on menus with several pages
  * Updated italian translation

* version 4.5.0 (2016-01-02)
  * Reduced the height of the MENU window
  * Now the menu works fine when enabling the "Play all" option

* version 4.4.0 (2015-11-07)
  * Removed MPlayer as an option for getting movie information

* version 4.3.2 (2015-11-07)
  * Added extra debug info in the log

* version 4.3.1 (2015-11-07)
  * Added manpage (thanks to Alession Treglia)

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
