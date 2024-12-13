# DALI-DMX Bridge for Lighting Applications  

## Overview  
This project implements a **DALI-DMX bridge** on a Raspberry Pi, allowing control of both DALI and DMX lighting fixtures through a single interface. The system integrates these two protocols and features a **Tkinter-based GUI**, providing a versatile solution for lighting control in various applications.  

## Features  
- Control DALI and DMX lighting systems from a unified, Tkinter-based graphical interface.  
- Translate commands between DALI and DMX protocols.  
- Manage lighting configurations, including brightness, scenes, and group settings.  

## Components  
1. **DALI Implementation**: Handles interaction with DALI lights, including brightness, scenes, and group membership.  
2. **DMX Implementation**: Interacts with DMX devices using the ArtNet protocol and the Open Lighting Architecture (OLA).  
3. **Bridge Functionality**: Core module for translating DALI commands to DMX and vice versa, integrated into the Tkinter GUI.  

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/KGupte/DALI_DMX_Team_Project/tree/master
   cd DALI_DMX_Team_Project
