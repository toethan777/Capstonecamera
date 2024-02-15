# Capstone Camera things!
Click [here](https://shop.luxonis.com/products/oak-d-pro-w) for the Oak-D Pro W specs
## Basic structure/terminology
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
 

[Messages](https://docs.luxonis.com/projects/api/en/latest/components/messages/): How nodes can communicate with each other. For our purposes, we have created a script node to have communication between nodes. This currently contains the MJPEG streaming code and includes IR nighttime flooding.

[Bootloader](https://docs.luxonis.com/projects/api/en/latest/components/bootloader/?highlight=boot): Small program in the booting process of the camera. The cameras came with a factory bootloader; thus, nothing is running on it until you flash a program to it.
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
*Real Time Vessel detection from DVR.

*Switch between Day (light) and Night (dark) mode, perhaps get ORDA on this for Neural Networking? 
