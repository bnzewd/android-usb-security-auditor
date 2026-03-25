
--- 
### `android-usb-security-auditor/README.md`

```md
# Android USB Security Auditor

A GUI desktop tool for reviewing Android device security information over USB using ADB.

## Overview
Android USB Security Auditor is a Python desktop application that connects to an Android device through ADB and displays important system and security-related information in a user-friendly interface.

## Features
- GUI interface built with Tkinter
- Detects connected Android device through ADB
- Displays device model and brand
- Shows Android version
- Shows security patch level if available
- Reads encryption state
- Reads debuggable state
- Shows USB configuration
- Saves the audit result as a text report

## Technologies Used
- Python
- Tkinter
- subprocess
- ADB

## Requirements
- Python installed
- ADB installed and available in PATH
- Android device connected through USB
- USB debugging enabled on the device

## Run
```bash
python android_usb_security_auditor.py
