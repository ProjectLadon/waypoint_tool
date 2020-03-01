#--------------------------------------------------------
# The CMakeLists.txt for:                       uWaypointMaker
# Author(s):
#--------------------------------------------------------

SET(SRC
    waypoint_helper.cpp
)

#=============================================================================
# FINDING MOOSGeodesy' HEADERS AND LIBRARIES...
#=============================================================================
find_package(MOOSGeodesy)
include_directories(${MOOSGeodesy_INCLUDE_DIRS})
link_directories(${MOOSGeodesy_LIBRARY_PATH})

message("+++++++++++++++++++++++++++++++++++++++++")
message("MOOSGeodesy_INCLUDE_DIRS:" ${MOOSGeodesy_INCLUDE_DIRS})
message("MOOSGeodesy_LIB_PATH:"     ${MOOSGeodesy_LIBRARY_PATH})
message("+++++++++++++++++++++++++++++++++++++++++")


INCLUDE_DIRECTORIES(${MOOS_INCLUDE_DIRS} ${MOOSGeodesy_INCLUDE_DIRS})

ADD_EXECUTABLE(waypoint_helper ${SRC})

TARGET_LINK_LIBRARIES(waypoint_helper
    ${MOOS_LIBRARIES}
    m
    pthread
    proj
    MOOSGeodesy
)
