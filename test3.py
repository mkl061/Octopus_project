import cv2

# Create video capture objects for both videos
cap1 = cv2.VideoCapture("video.mp4")
cap2 = cv2.VideoCapture("video.mp4")

# Initialize variables for the AOI in both videos
ix1, iy1, fx1, fy1 = -1, -1, -1, -1
ix2, iy2, fx2, fy2 = -1, -1, -1, -1

# Define a function to handle mouse events in both videos
def select_roi(event, x, y, flags, params):
    global ix1, iy1, fx1, fy1, ix2, iy2, fx2, fy2

    if event == cv2.EVENT_LBUTTONDOWN:
        # Start selecting AOI
        if params == 1:
            ix1, iy1 = x, y
        else:
            ix2, iy2 = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        # Finish selecting AOI
        if params == 1:
            fx1, fy1 = x, y
        else:
            fx2, fy2 = x, y

# Set the mouse callback function for both videos
cv2.namedWindow("Video 1")
cv2.setMouseCallback("Video 1", select_roi, 1)
cv2.namedWindow("Video 2")
cv2.setMouseCallback("Video 2", select_roi, 2)

# Initialize variables for the duration of the object inside the AOI in both videos
duration1 = 0
duration2 = 0

while True:
    # Read frames from both videos
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # Check if both frames were read successfully
    if not ret1 or not ret2:
        break

    # Draw the selected AOI in both videos
    cv2.rectangle(frame1, (ix1, iy1), (fx1, fy1), (0, 255, 0), 2)
    cv2.rectangle(frame2, (ix2, iy2), (fx2, fy2), (0, 255, 0), 2)

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

        # Iterate over the contours in both videos
        for contour in contours1:
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the bounding box is inside the AOI
            if x >= min(ix1, fx1) and x + w <= max(ix1, fx1) and y >= min(iy1, fy1) and y + h <= max(iy1, fy1):
                # Increment the duration of the object inside the AOI
                duration1 += 1

                # Draw the bounding box around the object
                cv2.rectangle(roi1, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for contour in contours2:
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the bounding box is inside the AOI
            if x >= min(ix2, fx2) and x + w <= max(ix2, fx2) and y >= min(iy2, fy2) and y + h <= max(iy2, fy2):
                # Increment the duration of the object inside the AOI
                duration2 += 1

                # Draw the bounding box around the object
                cv2.rectangle(roi2, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Display the frames in both videos with the selected AOI and the bounding boxes around the objects
        cv2.imshow("Video 1", frame1)
        cv2.imshow("Video 2", frame2)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # Exit the loop if the 'q' key is pressed
    if key == ord("q"):
        break

# Release the video capture objects and destroy all windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()

# Print the duration of the object inside the AOI in both videos
print("Duration in video 1: {} frames".format(duration1))
print("Duration in video 2: {} frames".format(duration2))
