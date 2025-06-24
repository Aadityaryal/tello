from djitellopy import Tello
import time

# Create Tello object
tello = Tello()

# Connect to drone
tello.connect()

# Take off
tello.takeoff()
time.sleep(2)

# # Rotate in place
# tello.rotate_clockwise(90)
# time.sleep(2)

# Land
tello.land()
