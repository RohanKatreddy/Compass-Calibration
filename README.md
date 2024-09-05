# Compass-Calibration

## Hardware:
* HMC5883L
* Arduino
* Laptop

## Brief explanation of architecture and inner workings
* The arduino program is used to gather raw data from the magnetometer (will now be refered to as a compass)
* The data from the arduino is picked up from a python data collection script
* The user is to rotate the compass in a circle, ensuring most of the points on the ellipse are covered
* The python program then runs a calibration algorithm to correct hard and soft iron errors
* The pythohn program then spits out the rotation matrix and related data required to correct data on the fly
* Utilizing these values alongside an arduino and a compass will product compass readings that are free of hard and soft iron distortions.

### Note: This program only does 2D calibration. 3D is in works.
