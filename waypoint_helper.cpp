/************************************************************/
/*    NAME:                                               */
/*    ORGN: MIT                                             */
/*    FILE: WaypointMakerMain.cpp                                    */
/*    DATE:                                                 */
/************************************************************/

#include <string>
#include <iostream>
#include "MOOS/libMOOSGeodesy/MOOSGeodesy.h"

using namespace std;

void bad_args ()
{
    cerr << "Usage: waypoint_helper <origin_lat> <origin_lon> <target_lat> <target_lon>" << endl;
}

int main(int argc, char *argv[])
{
  if (argc != 5) {
      bad_args();
      return -1;
  }

  double origin_lat = atof(argv[1]);
  double origin_lon = atof(argv[2]);
  double target_lat = atof(argv[3]);
  double target_lon = atof(argv[4]);
  double northing = 0;
  double easting = 0;

  CMOOSGeodesy geo;
  if (!geo.Initialise(origin_lat, origin_lon)) {bad_args(); return -1;}
  geo.LatLong2LocalGrid(target_lat, target_lon, northing, easting);
  cout << to_string(easting) << "," << to_string(northing) << endl;

  return(0);
}
