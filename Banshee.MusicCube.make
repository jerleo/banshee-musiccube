

# Warning: This is an automatically generated file, do not edit!

if ENABLE_RELEASE
ASSEMBLY_COMPILER_COMMAND = dmcs
ASSEMBLY_COMPILER_FLAGS =  -noconfig -codepage:utf8 -warn:4 -optimize+
ASSEMBLY = lib/Banshee.MusicCube.dll
ASSEMBLY_MDB = 
COMPILE_TARGET = library
PROJECT_REFERENCES = 
BUILD_DIR = lib


endif

AL=al
SATELLITE_ASSEMBLY_NAME=$(notdir $(basename $(ASSEMBLY))).resources.dll


RESGEN=resgen2
	
all: $(ASSEMBLY) 

FILES = \
	Banshee.MusicCube/MusicCubeActions.cs \
	Banshee.MusicCube/RandomByProximity.cs \
	Banshee.MusicCube/MusicCubeService.cs \
	Banshee.MusicCube/Coordinates.cs 

DATA_FILES = 

RESOURCES = \
	Resources/GlobalUI.xml \
	Banshee.MusicCube.addin.xml 

EXTRAS = \
	Resources 

REFERENCES =  \
	System \
	System.Core \
	Mono.Posix \
	$(BANSHEE_CORE_LIBS) \
	$(BANSHEE_COLLECTION_INDEXER_LIBS) \
	$(BANSHEE_PLAYQUEUE_LIBS) \
	$(BANSHEE_SERVICES_LIBS) \
	$(BANSHEE_THICKCLIENT_LIBS) \
	$(BANSHEE_HYENA_LIBS) \
	$(BANSHEE_HYENA_DATA_SQLITE_LIBS) \
	$(BANSHEE_HYENA_GUI_LIBS) \
	$(GTK_SHARP_20_LIBS)

DLL_REFERENCES = 

CLEANFILES = 

include $(top_srcdir)/Makefile.include




$(eval $(call emit_resgen_targets))
$(build_xamlg_list): %.xaml.g.cs: %.xaml
	xamlg '$<'

$(ASSEMBLY_MDB): $(ASSEMBLY)

$(ASSEMBLY): $(build_sources) $(build_resources) $(build_datafiles) $(DLL_REFERENCES) $(PROJECT_REFERENCES) $(build_xamlg_list) $(build_satellite_assembly_list)
	mkdir -p $(shell dirname $(ASSEMBLY))
	$(ASSEMBLY_COMPILER_COMMAND) $(ASSEMBLY_COMPILER_FLAGS) -out:$(ASSEMBLY) -target:$(COMPILE_TARGET) $(build_sources_embed) $(build_resources_embed) $(build_references_ref)
