//
// Coordinates.cs
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
using Banshee.Collection.Database;
using Banshee.ServiceStack;

namespace Banshee.MusicCube
{
    public class Coordinates
    {
        public Coordinates (int x, int y, int z)
        {
            this.X = x;
            this.Y = y;
            this.Z = z;
        }

        public int X { get; private set; }

        public int Y { get; private set; }

        public int Z { get; private set; }

        public static Coordinates Of (DatabaseTrackInfo track)
        {
            string sql = "SELECT Axis1, Axis2, Axis3 FROM MusicCube WHERE TrackId = ?";             
            HyenaSqliteCommand cmd = new HyenaSqliteCommand (sql);

            using (var reader = ServiceManager.DbConnection.Query (cmd, track.TrackId)) {
                if (reader.Read ()) {

                    // Cube coordinates of track
                    int x = Convert.ToInt32 (reader [0]);
                    int y = Convert.ToInt32 (reader [1]);
                    int z = Convert.ToInt32 (reader [2]);

                    Log.DebugFormat ("MusicCube: ({0}, {1}, {2})\t{3}: {4}", 
                                     x, y, z, track.ArtistName, track.TrackTitle);

                    return new Coordinates (x, y, z);
                }
            }
            return null;
        }
    }
}
