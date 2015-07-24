//
// MusicCubeActions.cs
//
// Copyright (C) 2015 Jeremiah J. Leonard
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.
using System;
using Mono.Unix;
using Gtk;
using Banshee.Collection;
using Banshee.Collection.Database;
using Banshee.PlayQueue;
using Banshee.ServiceStack;
using Banshee.Sources;
using Banshee.Gui;

namespace Banshee.MusicCube
{
    public class MusicCubeActions : Banshee.Gui.BansheeActionGroup
    {
        public MusicCubeActions (MusicCubeService musiccube) : base ("music-cube")
        {
            Add (new ActionEntry [] {
                new ActionEntry ("PlayByMusicCubeAction", Stock.Add,
                    Catalog.GetString ("Play by MusicCube"), null,
                    Catalog.GetString ("Play similar songs"),
                    OnPlayByMusicCube)
            });

            // Add action to track context menu
            AddUiFromFile ("GlobalUI.xml");
            Register ();
        }
        /*
        Required changes to switch shuffle mode programmatically:

        1) Extensions/Banshee.PlayQueue/Banshee.PlayQueue/HeaderWidget.cs

           public bool SetMode (Shuffler shuffler, String modeId) {
               foreach (var random_by in shuffler.RandomModes.OrderBy (r => r.Adverb)) {                
                   if (random_by.Id == modeId) {
                       mode_combo.ActiveValue = random_by;
                       return true;
                   }
               }
               return false;
           }

        2) Extensions/Banshee.PlayQueue/Banshee.PlayQueue/PlayQueueSource.cs

           public bool ChangeShuffleMode (String modeId)
           {
               return header_widget.SetMode (shuffler, modeId);
           }
        */
        private void OnPlayByMusicCube (object o, EventArgs args)
        {        
            // Try to get the play queue
            PlayQueueSource queue = MusicCubeService.PlayQueue;
            if (queue == null)
                return;

            // Get selected track
            TrackInfo track = RandomByProximity.SeedTrack ();

            // Set up play queue
            queue.Clear ();
            queue.EnqueueTrack (track, false);
            queue.ChangeShuffleMode ("proximity");

            // Switch to play queue and start playing
            ServiceManager.SourceManager.SetActiveSource (queue);
            if (ServiceManager.PlayerEngine.IsPlaying ())
                ServiceManager.PlayerEngine.Close ();
            ServiceManager.PlayerEngine.Play ();
        }
    }
}
