# banshee-musiccube
Playback Extension for Banshee Media Player

MusicCube is an extension for the Banshee Media Player allowing you to play statistically similar songs from the play queue. Your music collection needs to be analyzed first using:

	python musiccube.py

This creates a table called MusicCube in your Banshee database which stores the coordinates of each song in the MusicCube. The extension adds to the context menu the command "Play by MusicCube". Select it to clear the play queue and fill it with statistically similar songs.

As I did not know how to programmatically switch the playback mode of the play queue other than modifying the play queue extension code, you will need the full source code of Banshee to make the extension work. Required steps are documented in setup.sh.
