# OpenRoverRosSerial
source /opt/ros/melodic/setup.bash
rosdep init
rosdep update

removed old build and devel dirs
then run catkin_make  should rebuild everything

apt-get install libbluetooth-dev libcwiid-dev

copy github.com/ros-drivers/joystick_drivers
move wiitmote dir to /opt/ros/version/share
share/wiimote
mkdir build
cd build
cmake ../
make
make install

source devel/setup.bash
echo $ROS_PACKAGE_PATH

/opt/repos/OpenRoverRosSerial/src:/opt/ros/melodic/share

Four windows: roscore, wiimote, wiiconverter, openroverserial

roscore
rosrun open_rover_serial openroverserial.py
rosrun wiimote wiimote_node.py
rosrun open_rover_serial openroverserial.py







