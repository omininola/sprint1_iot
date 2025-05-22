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

def draw_rounded_rect(img, top_left, bottom_right, color, radius=10, thickness=-1):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    cv.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)

for r in results:
    if r.decision_margin < 20:
        continue

    corners = r.corners
    pts = np.array(corners, dtype=np.int32).reshape((-1, 1, 2))

    cv.line(img, pts[0][0], pts[1][0], (0, 255, 0), 3)
    cv.line(img, pts[1][0], pts[2][0], (0, 0, 255), 3)
    cv.line(img, pts[2][0], pts[3][0], (255, 0, 0), 3)
    cv.line(img, pts[3][0], pts[0][0], (255, 0, 0), 3)

    center_x, center_y = int(r.center[0]), int(r.center[1])
    tag_text = f"ID: {r.tag_id}"

    # Text settings
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    text_size, _ = cv.getTextSize(tag_text, font, font_scale, thickness)
    text_w, text_h = text_size

    padding = 10
    rect_w = text_w + 2 * padding
    rect_h = text_h + 2 * padding

    # Rectangle position (centered horizontally, above the tag)
    rect_x1 = center_x - rect_w // 2
    rect_y1 = center_y - 40 - rect_h  # 40 pixels above the tag
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h

    # Text position (inside rect)
    text_x = rect_x1 + padding
    text_y = rect_y1 + padding + text_h

    # Draw filled rectangle (background)
    draw_rounded_rect(img, rect_tl, rect_br, (0, 0, 0), radius=10, thickness=-1)  # Black background
    
    # Draw text over rectangle
    text_origin = (rect_tl[0] + 5, rect_br[1] - 5)
    cv.putText(img, tag_text, text_origin, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)

cv.imshow("AprilTag Detection", img)
cv.waitKey(0)
