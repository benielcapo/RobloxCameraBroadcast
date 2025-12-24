import cv2
import PIL.Image
import numpy
import json
import http.server

RESOLUTION = (50, 50)
DEFAULT_CAMERA_PATH = "camera_error.png"
SAVE_JSON_FRAME_DEBUG = False
HOST_PORT = ("0.0.0.0", 8080)
CACHED_DEFAULT_CAMERA = None

def default_camera():
    global CACHED_DEFAULT_CAMERA
    if CACHED_DEFAULT_CAMERA is not None:
        return CACHED_DEFAULT_CAMERA
    img = PIL.Image.open(DEFAULT_CAMERA_PATH)
    img = img.resize(RESOLUTION)
    arr = numpy.array(img)
    CACHED_DEFAULT_CAMERA = arr
    return arr

def frame2json(np_frame):
    j = json.dumps(np_frame.tolist())
    if SAVE_JSON_FRAME_DEBUG:
        with open("debug.json", "w+") as f:
            f.write(j)
    return j

def get_frame(src = 0):
    cap = cv2.VideoCapture(src)
    ret, cam = cap.read()
    if not ret:
        cam = default_camera()
    else:
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        cam = cam.astype(numpy.uint8)
        cam = cv2.resize(cam, RESOLUTION)
    return cam

def get_cam(src = 0):
    cam = get_frame(src)
    j = frame2json(cam)
    return j

class CamHttp(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Serving requests from ip " + str(self.client_address[0]) + " and port " + str(self.client_address[1]))
        data = get_cam().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    server = http.server.HTTPServer(HOST_PORT, CamHttp)
    server.serve_forever()
