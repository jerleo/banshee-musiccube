ASSEMBLY = Banshee.MusicCube
LINK =  $(BANSHEE_LIBS)
#LINK += $(BANSHEE_PLAYQUEUE_LIBS)
LINK += -r:/usr/local/lib/banshee/Extensions/Banshee.PlayQueue.dll

SOURCES =  \
	Banshee.MusicCube/Coordinates.cs \
	Banshee.MusicCube/MusicCubeActions.cs \
	Banshee.MusicCube/MusicCubeService.cs \
	Banshee.MusicCube/RandomByProximity.cs

RESOURCES =  \
	Banshee.MusicCube.addin.xml \
	Resources/GlobalUI.xml

include $(top_srcdir)/build/build.mk
