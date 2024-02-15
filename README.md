# Capstone Camera things!!!

## Basic structure/terminology
Pipeline: collection of nodes and links between them. 

Nodes: Provides functionality of camera. Below are nodes that we potentially need: 
```
               ┌─────────────────┐ 
               │                 │         out 
inputControl   │                 ├───────────► 
──────────────►│    MonoCamera   |         raw 
               │                 ├───────────► 
               │                 │ 
               └─────────────────┘ 

            ┌───────────────────┐ 
            │                   │       out 
            │                   ├───────────► 
            │     Yolo          │ 
            │     Detection     │ 
input       │     Network       │ passthrough 
───────────►│-------------------├───────────► 
            │                   │ 
            └───────────────────┘ 

          ┌──────────────┐ 
          │              │ 
 input    │              │bitstream 
─────────►│ VideoEncoder ├────────► 
          │              │ 
          │              │ 
          └──────────────┘ 
```
 

Messages: How nodes can communicate with each other. For our purposes, we need to create a script. This currently contains the MJPEG streaming code and includes IR nighttime flooding.

Bootloader: Small program in the booting process of the camera. The cameras came with a factory bootloader; thus, nothing is running on it until you flash a program to it.
Below is a skeleton of what needs to go into our script to flash our cameras: 

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
*Real Time Vessel detection from DVR

*Switch between Day (light) and Night (dark) mode, perhaps get ORDA on this for Neural Networking? 
