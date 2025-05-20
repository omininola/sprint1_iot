import cv2 as cv
from pupil_apriltags import Detector
import numpy as np

img = cv.imread("tags/tags.jpg")

detector = Detector(
    families="tag16h5",
    nthreads=1,
    quad_decimate=1,
    quad_sigma=0,
    refine_edges=1,
    decode_sharpening=0.25,
)

img = cv.resize(img, (640, 480))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
results = detector.detect(gray)

for r in results:
    if r.decision_margin < 20:
        continue

    corners = r.corners
    pts = np.array(corners, dtype=np.int32).reshape((-1, 1, 2))
    cv.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
    cX, cY = pts[0][0]
    cv.putText(
        img,
        "TAG_ID: " + str(r.tag_id),
        (cX + 10, cY - 10),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

cv.imshow("AprilTag Detection", img)
cv.waitKey(0)
