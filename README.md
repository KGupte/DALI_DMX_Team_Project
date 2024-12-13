# DALI-DMX Bridge for Lighting Applications  

## Overview  
This project implements a **DALI-DMX bridge** on a Raspberry Pi, allowing control of both DALI and DMX lighting fixtures through a single interface. The system integrates these two protocols, providing a versatile solution for lighting control in various applications.  

## Features  
- Control DALI and DMX lighting systems from a unified interface.  
- Translate commands between DALI and DMX protocols.  
- User-friendly GUI for managing lighting systems.  

## Components  
1. **DALI Implementation**: Handles interaction with DALI lights, including brightness, scenes, and group membership.  
2. **DMX Implementation**: Interacts with DMX devices using the ArtNet protocol and the Open Lighting Architecture (OLA).  
3. **Bridge Functionality**: Core module for translating DALI commands to DMX and vice versa, integrated into the Tkinter GUI.

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/dali-dmx-bridge.git
   cd dali-dmx-bridge

2. Install dependencies and OLA:
   ```bash
   sudo apt-get install ola  
   pip install -r requirements.txt  
