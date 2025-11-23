import cv2
import numpy as np

# Load your fisheye image
img = cv2.imread('fisheye.png')

# Define your camera matrix and distortion coefficients
# Calibration for precise values, but can guess small values too
K = np.array([[500, 0, img.shape[1]//2],
              [0, 500, img.shape[0]//2],
              [0, 0, 1]], dtype=np.float64)

D = np.array([-0.025, 0.005, 0, 0], dtype=np.float64)



# New camera matrix for dewarped image
dim = img.shape[:2][::-1]
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim, np.eye(3), balance=0.5)

# Dewarp
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, dim, cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)

# Save output
cv2.imwrite('undistorted.png', undistorted_img)
cv2.imshow('undistorted', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

