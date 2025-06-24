from djitellopy import Tello
import config
import time

class DroneController:
    def __init__(self):
        """Initialize the Tello drone connection."""
        self.drone = Tello()
        self.connected = False

    def connect(self):
        """Connect to the drone and enter SDK mode."""
        try:
            self.drone.connect()
            self.drone.send_rc_control(0, 0, 0, 0)  # Reset control to zero
            response = self.drone.send_command_with_return("command")
            if response.lower() == "ok":
                self.connected = True
                print("Drone connected and in SDK mode")
            else:
                print("Failed to enter SDK mode:", response)
        except Exception as e:
            print("Connection error:", str(e))
            self.connected = False

    def takeoff(self):
        """Command the drone to take off."""
        if not self.connected:
            print("Error: Drone not connected")
            return False
        try:
            response = self.drone.send_command_with_return("takeoff")
            if response.lower() == "ok":
                print("Drone taking off")
                return True
            else:
                print("Takeoff failed:", response)
                return False
        except Exception as e:
            print("Takeoff error:", str(e))
            return False

    def land(self):
        """Command the drone to land."""
        if not self.connected:
            print("Error: Drone not connected")
            return False
        try:
            response = self.drone.send_command_with_return("land")
            if response.lower() == "ok":
                print("Drone landing")
                return True
            else:
                print("Landing failed:", response)
                return False
        except Exception as e:
            print("Landing error:", str(e))
            return False

    def emergency_stop(self):
        """Stop all motors immediately."""
        if not self.connected:
            print("Error: Drone not connected")
            return False
        try:
            response = self.drone.send_command_with_return("emergency")
            if response.lower() == "ok":
                print("Emergency stop activated")
                return True
            else:
                print("Emergency stop failed:", response)
                return False
        except Exception as e:
            print("Emergency stop error:", str(e))
            return False

    def get_battery(self):
        """Get the drone's battery level."""
        if not self.connected:
            print("Error: Drone not connected")
            return None
        try:
            battery = self.drone.get_battery()
            print("Battery level:", battery, "%")
            return battery
        except Exception as e:
            print("Battery query error:", str(e))
            return None


    def disconnect(self):
        """End the drone connection."""
        if self.connected:
            self.drone.end()
            self.connected = False
            print("Drone disconnected")