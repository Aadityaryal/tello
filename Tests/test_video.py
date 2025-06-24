from drone_controller import DroneController
from video_processor import VideoProcessor
import time
import config

def main():
    # Initialize drone controller
    controller = DroneController()
    
    # Connect to drone
    controller.connect()
    if not controller.connected:
        print("Exiting due to connection failure")
        return
    
    # Get initial battery level
    battery = controller.get_battery()
    if battery is None or battery < 20:
        print("Battery too low or unavailable, exiting")
        controller.disconnect()
        return
    
    # Initialize video processor
    video_processor = VideoProcessor(controller)
    
    # Start video stream
    if not video_processor.start_stream():
        print("Exiting due to video stream failure")
        controller.disconnect()
        return
    
    # Perform takeoff
    if controller.takeoff():
        print("Displaying video for 1 seconds. Press 'q' to stop.")
        start_time = time.time()
        while time.time() - start_time < 1:
            if not video_processor.display_frame():
                break
            time.sleep(1 / config.FRAME_RATE)  # Match frame rate
    
    # Land the drone
    controller.land()
    
    # Stop video stream
    video_processor.stop_stream()
    
    # Get final battery level
    controller.get_battery()
    
    # Disconnect
    controller.disconnect()

if __name__ == "__main__":
    main()