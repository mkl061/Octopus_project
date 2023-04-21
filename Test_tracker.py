import cv2

# Initialize some variables
roi = None
roi_x1, roi_y1, roi_x2, roi_y2 = -1, -1, -1, -1
in_roi = False
start_time = None
total_time_in_roi = 0

# Mouse callback function to handle mouse events
def mouse_callback(event, x, y, flags, param):
    global roi, roi_x1, roi_y1, roi_x2, roi_y2

    # If the left mouse button is pressed, start drawing the ROI
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_x1, roi_y1 = x, y

    # If the left mouse button is released, finish drawing the ROI and set it
    elif event == cv2.EVENT_LBUTTONUP:
        roi_x2, roi_y2 = x, y
        roi = (roi_x1, roi_y1, roi_x2, roi_y2)

# Load the video file
cap = cv2.VideoCapture('video.mp4')

# Set up the mouse callback function
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_callback)

while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # If the ROI has been defined, draw it on the frame
    if roi is not None:
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create a mask of the white background
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # If the bounding box overlaps with the ROI, set in_roi to True and start the timer
        if roi is not None and x < roi_x2 and x + w > roi_x1 and y < roi_y2 and y + h > roi_y1:
            if not in_roi:
                start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                in_roi = True

        # If the bounding box does not overlap with the ROI, add the time spent in the ROI to the total
        # and reset the timer
        elif in_roi:
            end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            total_time_in_roi += end_time - start_time
            in_roi = False

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Show the frame
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed or the video stops
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

# Print the total time spent in the ROI
print('Total time in ROI:', total_time_in_roi)




# import cv2

# # Initialize some variables
# roi = None
# roi_x1, roi_y1, roi_x2, roi_y2 = -1, -1, -1, -1
# in_roi = False
# start_time = None
# total_time_in_roi = 0

# # Mouse callback function to handle mouse events
# def mouse_callback(event, x, y, flags, param):
#     global roi, roi_x1, roi_y1, roi_x2, roi_y2

#     # If the left mouse button is pressed, start drawing the ROI
#     if event == cv2.EVENT_LBUTTONDOWN:
#         roi_x1, roi_y1 = x, y

#     # If the left mouse button is released, finish drawing the ROI and set it
#     elif event == cv2.EVENT_LBUTTONUP:
#         roi_x2, roi_y2 = x, y
#         roi = (roi_x1, roi_y1, roi_x2, roi_y2)

# # Load the video file
# cap = cv2.VideoCapture('video.mp4')

# # Set up the mouse callback function
# cv2.namedWindow('frame')
# cv2.setMouseCallback('frame', mouse_callback)

# while True:
#     # Read a frame from the video
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # If the ROI has been defined, draw it on the frame
#     if roi is not None:
#         cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)

#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Threshold the grayscale image to create a mask of the white background
#     _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

#     # Find contours in the mask
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Loop over the contours
#     for contour in contours:
#         # Get the bounding box of the contour
#         x, y, w, h = cv2.boundingRect(contour)

#         # If the bounding box overlaps with the ROI, set in_roi to True and start the timer
#         if roi is not None and x < roi_x2 and x + w > roi_x1 and y < roi_y2 and y + h > roi_y1:
#             if not in_roi:
#                 start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
#                 in_roi = True

#         # If the bounding box does not overlap with the ROI, add the time spent in the ROI to the total
#         # and reset the timer
#         elif in_roi:
#             end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
#             total_time_in_roi += end_time - start_time
#             in_roi = False

#         # Draw the bounding box on the frame
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

#     # Show the frame
#     cv2.imshow('frame', frame)

#     # Exit the loop if the 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Print the total time spent in the ROI
# print(f'Total time in ROI {total_time_in_roi}.')
