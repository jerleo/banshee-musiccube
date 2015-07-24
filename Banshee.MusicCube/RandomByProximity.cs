//
// RandomByProximity.cs
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
using Hyena;
using Hyena.Data.Sqlite;
using Banshee.Collection;
using Banshee.Collection.Database;
using Banshee.Gui;
using Banshee.PlayQueue;
using Banshee.ServiceStack;
using Mono.Unix;

namespace Banshee.MusicCube
{
    public class RandomByProximity : RandomBy
    {
        private static PlayQueueSource queue;
        private static Coordinates seed;

        public RandomByProximity () : base ("proximity")
        {
            Label = Catalog.GetString ("Shuffle by Proximity");
            Adverb = Catalog.GetString ("by proximity");
            Description = Catalog.GetString ("Play all songs close to selected song");
        }

        public static TrackInfo SeedTrack ()
        {
            queue = MusicCubeService.PlayQueue;

            var actions = ServiceManager.Get<InterfaceActionService> ().TrackActions;
            foreach (TrackInfo track in actions.SelectedTracks) {
                seed = Coordinates.Of (track as DatabaseTrackInfo);
                return track;                                    
            }
            return null;
        }

        protected override void OnModelAndCacheUpdated ()
        {
            // Calculate distance within cube
            string distance = @", ABS(MusicCube.Axis1 - {0}) 
                                + ABS(MusicCube.Axis2 - {1}) 
                                + ABS(MusicCube.Axis3 - {2}) AS Distance";

            // Don't repeat albums
            string album = @"SELECT DISTINCT AlbumID
                               FROM CorePlayListEntries
                               JOIN CoreTracks
                                 ON CoreTracks.TrackID = CorePlayListEntries.TrackID
                              WHERE CorePlayListEntries.PlayListID = {0}";

            // Don't repeat artists
            string artist = @"SELECT DISTINCT ArtistID
                                FROM CorePlayListEntries
                                JOIN CoreTracks
                                  ON CoreTracks.TrackID = CorePlayListEntries.TrackID
                               WHERE CorePlayListEntries.PlayListID = {0}";

            // Set query fragments
            Select = String.Format (distance, seed.X, seed.Y, seed.Z);
            From = ", MusicCube";
            Condition = "MusicCube.TrackID = CoreTracks.TrackID";
            Condition += String.Format (" AND CoreTracks.ArtistID NOT IN (" + artist + ")", queue.DbId);
            Condition += String.Format (" AND CoreTracks.AlbumID NOT IN (" + album + ")", queue.DbId);
            OrderBy = "Distance";
        }

        /*
           Signature changed to protected virtual in
           Core/Banshee.Services/Banshee.Collection.Database/RandomBy.cs
        */
        protected override DatabaseTrackInfo GetTrack (HyenaSqliteCommand cmd, params object[] args)
        {    
            DatabaseTrackInfo track = base.GetTrack (cmd, args);

            // Write coordinates to debug log
            Coordinates.Of (track);
            return track;
        }
    }
}
