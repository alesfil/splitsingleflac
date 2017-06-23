#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
import os.path

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Split single flac")

        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.bigVbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.hbox1 = Gtk.Box(spacing=6)

        label = Gtk.Label("Single Flac filename")
        label.set_alignment(xalign=0, yalign=0.5)
        self.vbox1.pack_start(label, True, True, 0)

        label = Gtk.Label("Cue filename")
        label.set_alignment(xalign=0, yalign=0.5)
        self.vbox1.pack_start(label, True, True, 0)

        self.flacfilenameEntry = Gtk.Entry()
        self.vbox2.pack_start(self.flacfilenameEntry, True, True, 0)

        self.cuefilenameEntry = Gtk.Entry()
        self.vbox2.pack_start(self.cuefilenameEntry, True, True, 0)

        self.flacBrowseButton = Gtk.Button(label="Browse...")
        self.vbox3.pack_start(self.flacBrowseButton, True, True, 0)

        self.cueBrowseButton = Gtk.Button(label="Browse...")
        self.vbox3.pack_start(self.cueBrowseButton, True, True, 0)

        self.hbox1.pack_start(self.vbox1, False, False, 5)
        self.hbox1.pack_start(self.vbox2, True, True, 5)
        self.hbox1.pack_start(self.vbox3, False, False, 5)

        self.splitButton = Gtk.Button(label="Split")

        self.bigVbox.pack_start(self.hbox1, True, True, 0)
        self.bigVbox.pack_start(self.splitButton, True, True, 5)

        self.splitButton.connect("clicked", self.on_splitButton_clicked)
        self.flacBrowseButton.connect("clicked", self.on_flacButton_clicked)
        self.cueBrowseButton.connect("clicked", self.on_cueButton_clicked)

        self.add(self.bigVbox)

    def on_splitButton_clicked(self, widget):
        flacfile = str(self.flacfilenameEntry.get_text())
        cuefile = str(self.cuefilenameEntry.get_text())
        workdir = os.path.dirname(flacfile)
        if flacfile != "":
            subprocess.call(['shntool','split','-f',cuefile,'-o','flac','-t','"%n - %t"',flacfile],cwd = workdir)
            subprocess.call(['mv',flacfile,flacfile+'.bkp'])
            shellCuefile = cuefile.replace(" ","\ ")
            subprocess.call('cuetag %s *.flac' % (shellCuefile), shell=True, cwd = workdir)

    def on_flacButton_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a flac file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_flac = Gtk.FileFilter()
        filter_flac.set_name("Flac files")
        filter_flac.add_pattern("*.flac")
        dialog.add_filter(filter_flac)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            flacfile = dialog.get_filename()
            self.flacfilenameEntry.set_text(flacfile)
            cuefile = flacfile.replace("flac","cue")
            if os.path.isfile(cuefile):
                self.cuefilenameEntry.set_text(cuefile) 

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def on_cueButton_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a cue file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_cue = Gtk.FileFilter()
        filter_cue.set_name("Cue files")
        filter_cue.add_pattern("*.cue")
        dialog.add_filter(filter_cue)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.cuefilenameEntry.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
