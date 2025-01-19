import cv2
import time

def test_camera(camera_index):
    print(f"\nTesting camera index {camera_index}...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Camera index {camera_index} could not be opened")
        return False
    
    print(f"Camera {camera_index} opened successfully!")
    ret, frame = cap.read()
    
    if ret:
        print(f"Frame captured from camera {camera_index}")
        cv2.imshow(f'Camera Test {camera_index}', frame)
        cv2.waitKey(1000)  # Show for 1 second
    
    cap.release()
    cv2.destroyAllWindows()
    return ret

# Test multiple camera indices
print("Searching for available cameras...")
for i in range(4):  # Test indices 0-3
    if test_camera(i):
        print(f"\nCamera {i} is available!")
        user_input = input(f"Is this the correct camera? (y/n): ")
        if user_input.lower() == 'y':
            print(f"\nUse camera index {i} in your main program!")
            break
    else:
        print(f"Camera {i} is not available")

print("\nTest completed.")