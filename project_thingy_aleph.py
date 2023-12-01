#!/usr/bin/env python3

import depthai as dai
import threading
import contextlib
import cv2
import time
from queue import Queue

run = True
def getPipeline(stereo):
    # Start defining a pipeline
    pipeline = dai.Pipeline()

    # Define a source and attributes - Mono camera
    cam = pipeline.create(dai.node.MonoCamera)
    cam.setNumFramesPool(24)

    # VideoEncoder
    jpeg = pipeline.create(dai.node.VideoEncoder)
    jpeg.setDefaultProfilePreset(cam.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)

    # MJPEG script node
    script = pipeline.create(dai.node.Script)
    script.setProcessor(dai.ProcessorType.LEON_CSS)
    script.setScript("""
        import time
        import socket
        import fcntl
        import struct
        from socketserver import ThreadingMixIn
        from http.server import BaseHTTPRequestHandler, HTTPServer

        PORT = 8080

        def get_ip_address(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                -1071617759,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15].encode())
            )[20:24])

        class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
            pass

        class HTTPHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'<h1>Toast was Here!!!</h1><p>Click <a href="img">here</a> for an image</p>')
                elif self.path == '/img':
                    try:
                        self.send_response(200)
                        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
                        self.end_headers()
                        fpsCounter = 0
                        timeCounter = time.time()
                        while True:
                            jpegImage = node.io['jpeg'].get()
                            self.wfile.write("--jpgboundary".encode())   
                            self.wfile.write(bytes([13, 10]))
                            self.send_header('Content-type', 'image/jpeg')
                            self.send_header('Content-length', str(len(jpegImage.getData())))
                            self.end_headers()
                            self.wfile.write(jpegImage.getData())
                            self.end_headers()

                            fpsCounter = fpsCounter + 1
                            if time.time() - timeCounter > 1:
                                node.warn(f'FPS: {fpsCounter}')
                                fpsCounter = 0
                                timeCounter = time.time()
                    except Exception as ex:
                        node.warn(str(ex))

        with ThreadingSimpleServer(("", PORT), HTTPHandler) as httpd:
            node.warn(f"Serving at {get_ip_address('re0')}:{PORT}")
            httpd.serve_forever()
    """)

    # Connections
    cam.out.link(jpeg.input)
    jpeg.bitstream.link(script.inputs['jpeg'])

    # Connect to device with pipeline
    with dai.Device(pipeline) as device:
        while not device.isClosed():
            device.setIrFloodLightBrightness(200)
            time.sleep(1)
    return pipeline

def worker(dev_info, stack, queue):
    global run
    openvino_version = dai.OpenVINO.Version.VERSION_2021_4
    device: dai.Device = stack.enter_context(dai.Device(openvino_version, dev_info, False))

    # Note: currently on POE, DeviceInfo.getMxId() and Device.getMxId() are different!
    print("=== Connected to " + dev_info.getMxId())
    mxid = device.getMxId()
    cameras = device.getConnectedCameras()
    usb_speed = device.getUsbSpeed()
    print("   >>> MXID:", mxid)
    print("   >>> Cameras:", *[c.name for c in cameras])
    print("   >>> USB speed:", usb_speed.name)

    device.startPipeline(getPipeline(len(cameras)==3))
    q = device.getOutputQueue(name="mjpeg", maxSize=1, blocking=False)

    while run:
        imgFrame = q.get()
        # decode
        frame = cv2.imdecode(imgFrame.getData(), cv2.IMREAD_COLOR)
        queue.put(frame)
    print('Closing thread')


device_infos = dai.Device.getAllAvailableDevices()
print(f'Found {len(device_infos)} devices')

with contextlib.ExitStack() as stack:
    queues = {}
    threads = []
    for dev in device_infos:
        time.sleep(1) # Currently required due to XLink race issues
        q = Queue(1)
        thread = threading.Thread(target=worker, args=(dev, stack, q))
        queues[dev.getMxId()] = q
        thread.start()
        threads.append(thread)

    while True:
        for name, q in queues.items():
            try:
                frame = q.get(block=False)
                frame = cv2.pyrDown(frame)
                cv2.imshow(name, frame)
            except:
                continue

        if cv2.waitKey(1) == ord('q'):
            run=False
            break

    for t in threads:
        t.join() # Wait for all threads to finish

print('Devices closed')