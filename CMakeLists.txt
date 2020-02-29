#--------------------------------------------------------
# The CMakeLists.txt for:                       uWaypointMaker
# Author(s):                              
#--------------------------------------------------------

FILE(GLOB SRC *.cpp)

ADD_EXECUTABLE(uWaypointMaker ${SRC})

TARGET_LINK_LIBRARIES(uWaypointMaker
   ${MOOS_LIBRARIES}
   mbutil
   m
   pthread)

