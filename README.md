# Capstone Camera things!
Click [here](https://shop.luxonis.com/products/oak-d-pro-w) for the Oak-D Pro W specs.

Click [here](https://github.com/luxonis/depthai-python) for cool scripts you can use on the camera.

## Hardware Provided/Needed
2x Oak-D Pro Wide Cameras

1x PoE Switch

2x Ethernet Cables

2x Ethernet to M8 Cables

1x LAN network port (Cybernet, etc)

1x Luxonis Programming Board (optional)

## DepthAI scripting, basic structure/terminology
[Pipeline](https://docs.luxonis.com/projects/api/en/latest/components/pipeline/): collection of nodes and links between them. 

[Nodes](https://docs.luxonis.com/projects/api/en/latest/components/nodes/): Provides functionality of camera. Below are nodes that we potentially need: 
```
               ┌─────────────────┐ 
               │                 │         out 
inputControl   │                 ├───────────► 
──────────────►│    MonoCamera   |         raw 
               │                 ├───────────► 
               │                 │ 
               └─────────────────┘ 


          ┌──────────────┐ 
          │              │ 
 input    │              │bitstream 
─────────►│ VideoEncoder ├────────► 
          │              │ 
          │              │ 
          └──────────────┘


            ┌───────────────────┐ 
            │                   │       out 
            │                   ├───────────► 
            │     Yolo          │ 
            │     Detection     │ 
input       │     Network       │ passthrough 
───────────►│-------------------├───────────► 
            │                   │ 
            └───────────────────┘ 
```
 

[Messages](https://docs.luxonis.com/projects/api/en/latest/components/messages/): How nodes can communicate with each other. For our purposes, we have created a script node to have communication between nodes. This currently contains the MJPEG streaming code and includes IR nighttime flooding.

[Bootloader](https://docs.luxonis.com/projects/api/en/latest/components/bootloader/?highlight=boot): Small program in the booting process of the camera. The cameras came with a factory bootloader; thus, nothing is running on it until you flash a program to it.
Below is a sample code of what needs to go into our script to flash our cameras: 

```
import depthai as dai 
 
pipeline = dai.Pipeline() 
 
# Define standalone pipeline; add nodes and link them 
# cam = pipeline.create(dai.node.ColorCamera) 
# script = pipeline.create(dai.node.Script) 
# ... 
 
# Flash the pipeline
(f, bl) = dai.DeviceBootloader.getFirstAvailableDevice() 
bootloader = dai.DeviceBootloader(bl)
progress = lambda p : print(f'Flashing progress: {p*100:.1f}%') 
bootloader.flash(progress, pipeline)
 ```

## What we may want to do
*Real Time Vessel detection from DVR.

*Switch between Day (light) and Night (dark) mode, perhaps get ORDA on this for Neural Networking? 

*Research Robothub for easier development of camera.
## Other Notes

We have statically set the IPs of both Oak-D cameras: one is `10.233.105.14`, and the other is `10.233.105.173`. If we want to change them or use them on a different network, we have to consult Mr. Chad Davis in the Power lab. If the camera setup is screwed up (e.g. soft bricking the camera after changing the IP) we have to use the Luxonis Programming board to manually factory flash the camera. More information can be found at [this link](https://github.com/luxonis/depthai-python).
