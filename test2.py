import cv2

# Define the video paths
video1_path = "video.mp4"
video2_path = "video.mp4"

# Create VideoCapture objects
cap1 = cv2.VideoCapture(video1_path)
cap2 = cv2.VideoCapture(video2_path)

# Create windows and set mouse callback functions
cv2.namedWindow("Video 1")
cv2.setMouseCallback("Video 1", lambda event, x, y, flags, param: onMouse1(event, x, y, flags, param))
cv2.namedWindow("Video 2")
cv2.setMouseCallback("Video 2", lambda event, x, y, flags, param: onMouse2(event, x, y, flags, param))

# Define global variables
drawing1 = False  # True if mouse is pressed on video 1
drawing2 = False  # True if mouse is pressed on video 2
ix1, iy1 = -1, -1  # Starting point of the rectangle on video 1
ix2, iy2 = -1, -1  # Starting point of the rectangle on video 2
fx1, fy1 = -1, -1  # End point of the rectangle on video 1
fx2, fy2 = -1, -1  # End point of the rectangle on video 2
duration = 0     # Duration of the object inside the AOI

# Mouse callback function for video 1
def onMouse1(event, x, y, flags, param):
    global ix1, iy1, fx1, fy1, drawing1

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing1 = True
        ix1, iy1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing1:
            cv2.rectangle(frame1, (ix1, iy1), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing1 = False
        fx1, fy1 = x, y
        cv2.rectangle(frame1, (ix1, iy1), (fx1, fy1), (0, 255, 0), 2)

# Mouse callback function for video 2
def onMouse2(event, x, y, flags, param):
    global ix2, iy2, fx2, fy2, drawing2

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing2 = True
        ix2, iy2 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing2:
            cv2.rectangle(frame2, (ix2, iy2), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing2 = False
        fx2, fy2 = x, y
        cv2.rectangle(frame2, (ix2, iy2), (fx2, fy2), (0, 255, 0), 2)

# Loop through the frames
while True:
    # Read frames from the videos
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    # Display the frames
    cv2.imshow("Video 1", frame1)
    cv2.imshow("Video 2", frame2)

    # Check if the AOI is selected in both videos
    if fx1 != -1 and fy1 != -1 and fx2 != -1 and fy2 != -1:
        # Get the ROI in both videos
        roi1 = frame1[min(iy1, fy1):max(iy1, fy1), min(ix1, fx1):max(ix1, fx1)]
        roi2 = frame2[min(iy2, fy2):max(iy2, fy2), min(ix2, fx2):max(ix2, fx2)]

        # Convert the ROI to grayscale
        gray1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to the grayscale ROI
        _, thresh1 = cv2.threshold(gray1, 100, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded ROI
        contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the duration of the object inside the AOI in both videos
        duration1 = 0
        for contour in contours1:
            x, y, w, h = cv2.boundingRect(contour)
            duration1 += w

        duration2 = 0
        for contour in contours2:
            x, y, w, h = cv2.boundingRect(contour)
            duration2 += w

        duration = (duration1 + duration2) / 2

    # Draw the duration on the frame
    cv2.putText(frame1, f"Duration: {duration:.2f} frames", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame2, f"Duration: {duration:.2f} frames", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frames with the duration
    cv2.imshow("Video 1", frame1)
    cv2.imshow("Video 2", frame2)

    # Check for quit key
    if cv2.waitKey(1) == ord("q"):
        break

# Release the video captures and destroy the windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()
