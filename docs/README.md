# Computer Vision Workshop
This repository contains [software](../SDK/) components developed for the [@NTU-Mecatron](https://github.com/NTU-Mecatron) **Computer Vision Workshop** — a hands-on educational platform designed to teach robotics, embedded systems and computer vision.

## Detailed Documentation
- [Arduino code](./docs/mcu.md)
- [OpenCV code](./docs/opencv.md)

## Repository Structure
- **[SDK](../SDK/):** Software Development Kit  
  Contains the firmware and host-side code needed to operate the EduBoat system. Detailed software documentation is available [here](./SDK/).

---

### Hardware Overview
The hardware components include 1. Electrical connections; 2. Mechanical design of the gimbal camera itself.

> **Note:** Hardware assets — such as the 3D models for the robotic arm are not yet publicly released.

### Software Overview
The gimbal camera is powered by an Arduino UNO, which is connected to a host PC. The software component consists of 1. Firmware to be run on the MCU (to control the physical position of the camera); 2. Software to be run on the host PC (performing computer vision recognition).

Based on the relative position of the target recognised object in the camera, the gimbal is commanded to be towards the detected object, to keep it in the center of the screen

---

## Acknowledgements
This project was developed by the [@NTU-Mecatron](https://github.com/NTU-Mecatron) team. Special thanks to student contributors and teaching assistants who made the **Computer Vision Workshop** possible.

### Hardware Design: 
[Scott*](https://github.com/scott-cjx),
Rushdon

### Software Development: 
[Scott*](https://github.com/scott-cjx),
[Luc*](https://github.com/lucvt001)
[Wei Ming](https://github.com/Alvin0523)
[Brian](https://github.com/Thinkminator)

> \* Head of development for respective category

### Previous Works:
Thanks to student contributors, teaching assistants, and NTU’s support for making the Computer Vision Workshop possible.

---


## License
This project includes both software and hardware components:

- **Software** is licensed under the [GNU General Public License v3.0](./SOFTWARE-LICENSE).
- **Hardware** is licensed under the [CERN Open Hardware Licence Version 2 – Strongly Reciprocal (CERN-OHL-S v2)](./HARDWARE-LICENSE).


## Disclaimer
If you intend to use this project for your own **research**, **educational delivery**, or **derivative workshops**, we ask that you:

- Contact us at [@NTU-Mecatron](https://github.com/NTU-Mecatron) to discuss collaboration or reuse
- Credit the original developers appropriately in your materials or publications

We value open-source contribution, but also recognize the efforts and resources invested in this platform. Help us ensure responsible reuse and attribution.

## Citation
If you use this repository in your research or educational material, please cite it using the [`CITATION.cff`](../citation.cff) file provided. GitHub automatically extracts citation metadata, which can also be accessed using the “**Cite this repository**” button on the GitHub page.
