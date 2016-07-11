dnl Warning: This is an automatically generated file, do not edit!
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ([2.54])
AC_INIT([Banshee.MusicCube], [0.1])
AM_INIT_AUTOMAKE([foreign])
AM_MAINTAINER_MODE

dnl pkg-config
AC_PATH_PROG(PKG_CONFIG, pkg-config, no)
if test "x$PKG_CONFIG" = "xno"; then
        AC_MSG_ERROR([You need to install pkg-config])
fi

SHAMROCK_EXPAND_LIBDIR
SHAMROCK_EXPAND_BINDIR
SHAMROCK_EXPAND_DATADIR

AC_PROG_INSTALL

AC_PATH_PROG(DMCS, dmcs, no)
if test "x$DMCS" = "xno"; then
        AC_MSG_ERROR([dmcs Not found])
fi


AC_ARG_ENABLE(release,
	AC_HELP_STRING([--enable-release],
		[Use 'RELEASE' Configuration [default=YES]]),
		enable_release=yes, enable_release=no)
AM_CONDITIONAL(ENABLE_RELEASE, test x$enable_release = xyes)
if test "x$enable_release" = "xyes" ; then
	CONFIG_REQUESTED="yes"
fi
if test -z "$CONFIG_REQUESTED" ; then
	AM_CONDITIONAL(ENABLE_RELEASE, true)
	enable_release=yes
fi


dnl package checks, common for all configs
PKG_CHECK_MODULES([BANSHEE_CORE], [banshee-core])
PKG_CHECK_MODULES([BANSHEE_COLLECTION_INDEXER], [banshee-collection-indexer])
PKG_CHECK_MODULES([BANSHEE_PLAYQUEUE], [banshee-playqueue])
PKG_CHECK_MODULES([BANSHEE_SERVICES], [banshee-services])
PKG_CHECK_MODULES([BANSHEE_THICKCLIENT], [banshee-thickclient])
PKG_CHECK_MODULES([BANSHEE_HYENA], [banshee-hyena])
PKG_CHECK_MODULES([BANSHEE_HYENA_DATA_SQLITE], [banshee-hyena-data-sqlite])
PKG_CHECK_MODULES([BANSHEE_HYENA_GUI], [banshee-hyena-gui])
PKG_CHECK_MODULES([GTK_SHARP_20], [gtk-sharp-2.0])

dnl package checks, per config


AC_CONFIG_FILES([
Makefile

])

AC_OUTPUT
