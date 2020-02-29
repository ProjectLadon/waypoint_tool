/************************************************************/
/*    NAME:                                               */
/*    ORGN: MIT                                             */
/*    FILE: WaypointMakerMain.cpp                                    */
/*    DATE:                                                 */
/************************************************************/

#include <string>
#include "WaypointMaker.h"

using namespace std;

int main(int argc, char *argv[])
{
  // default parameters file
  string sMissionFile = "WaypointMaker.moos";
        
  //under what name shoud the application register with the MOOSDB?
  string sMOOSName = "uWaypointMaker";
  
  switch(argc)
    {
    case 3:
      //command line says don't register with default name              
      sMOOSName = argv[2];
    case 2:
      //command line says don't use default config file
      sMissionFile = argv[1];
    }
  
  //make an application
  WaypointMaker WaypointMakerApp;

  //run it
  WaypointMakerApp.Run(sMOOSName.c_str(), sMissionFile.c_str());
  
  return(0);
}

