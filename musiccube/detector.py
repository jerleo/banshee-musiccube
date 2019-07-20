#!/usr/bin/env python

'''
    Simple program that uses the 'bpmdetect' GStreamer plugin to detect
    the BPM of a song, and outputs that to console.

    Requires GStreamer 1.x, PyGObject 1.x, and gst-plugins-bad

    Copyright (C) 2015 Dustin Spicuzza

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2 as
    published by the Free Software Foundation.
'''

import os
import shelve
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gio

from banshee import Banshee

class Detector:

    def __message__(self, bus, msg):

        if msg.type == Gst.MessageType.TAG:
            tags = msg.parse_tag()

            # Discard tags already set on the file
            if tags.n_tags() > 1:
                return

            val = tags.get_value_index('beats-per-minute', 0)
            try:
                bpm = int(val)
            except:
                return

            if bpm > 0:
                self.bpm = bpm

        elif msg.type == Gst.MessageType.ERROR:

            self.playbin.set_state(Gst.State.NULL)
            gerror, debug_info = msg.parse_error()
            if gerror:
                print gerror.message.rstrip(".")
            else:
                print debug_info

        elif msg.type == Gst.MessageType.EOS:
            self.playbin.set_state(Gst.State.NULL)
            self.loop.quit()

    def __init__(self, song):

        Gst.init(None)

        audio_sink = Gst.Bin.new('audio_sink')

        # bpmdetect doesn't work properly with more than one channel,
        # see https://bugzilla.gnome.org/show_bug.cgi?id=751457
        cf = Gst.ElementFactory.make('capsfilter')
        cf.props.caps = Gst.Caps.from_string('audio/x-raw,channels=1')

        fakesink = Gst.ElementFactory.make('fakesink')
        fakesink.props.sync = False
        fakesink.props.signal_handoffs = False

        bpmdetect = Gst.ElementFactory.make('bpmdetect')

        audio_sink.add(cf)
        audio_sink.add(bpmdetect)
        audio_sink.add(fakesink)
        
        cf.link(bpmdetect)
        bpmdetect.link(fakesink)

        audio_sink.add_pad(Gst.GhostPad.new('sink', cf.get_static_pad('sink')))

        self.playbin = Gst.ElementFactory.make('playbin')
        self.playbin.props.audio_sink = audio_sink

        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.__message__)

        uri = Gio.File.new_for_commandline_arg(song).get_uri()
        self.playbin.props.uri = uri

        self.loop = GObject.MainLoop()

    def get_bpm(self):

        self.playbin.set_state(Gst.State.PLAYING)
        self.loop.run()
        return self.bpm


if __name__ == '__main__':

    if len(sys.argv) == 2:
        song = sys.argv[1]
        bpm_detector = Detector(song)
        print bpm_detector.get_bpm()
        sys.exit(0)

    banshee = Banshee()

    db_path = banshee.library_source()
    db_path = os.path.join(db_path, '.bpm.dbm')
    bpm_list = shelve.open(db_path, writeback=True)

    song_list = banshee.get_tracks()

    for song in song_list:
        if song not in bpm_list:
            bpm_detector = Detector(song)
            bpm_list[song] = bpm_detector.get_bpm()

        uri = Gio.File.new_for_commandline_arg(song).get_uri()
        bpm = bpm_list[song]
        print 'UPDATE CoreTracks SET BPM = %d WHERE Uri = "%s";' % (bpm, uri)
