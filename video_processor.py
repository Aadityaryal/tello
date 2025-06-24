import cv2
import config
from drone_controller import DroneController

class VideoProcessor:
    def __init__(self, drone_controller):
        """Initialize video processor with drone controller."""
        self.drone_controller = drone_controller
        self.video_capture = None
        self.streaming = False

    def start_stream(self):
        """Start the drone's video stream and initialize capture."""
        if not self.drone_controller.connected:
            print("Error: Drone not connected")
            return False
        try:
            # Send streamon command
            response = self.drone_controller.drone.send_command_with_return("streamon")
            if response.lower() != "ok":
                print("Failed to start video stream:", response)
                return False
            
            # Initialize OpenCV video capture
            video_url = f"udp://{config.DRONE_IP}:{config.VIDEO_PORT}"
            self.video_capture = cv2.VideoCapture(video_url)
            if not self.video_capture.isOpened():
                print("Error: Could not open video stream")
                return False
            
            self.streaming = True
            print("Video stream started")
            return True
        except Exception as e:
            print("Video stream start error:", str(e))
            return False

    def stop_stream(self):
        """Stop the video stream and release resources."""
        if self.streaming:
            try:
                self.drone_controller.drone.send_command_with_return("streamoff")
                self.streaming = False
            except Exception as e:
                print("Video stream stop error:", str(e))
            
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None
        cv2.destroyAllWindows()

    def display_frame(self):
        """Read and display a single frame from the video stream."""
        if not self.streaming or self.video_capture is None:
            print("Error: Video stream not active")
            return False
        
        try:
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: Could not read frame")
                return False
            
            # Display frame in a window
            if config.DEBUG:
                cv2.imshow("Tello Video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                    return False
            return True
        except Exception as e:
            print("Frame display error:", str(e))
            return False