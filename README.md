# Yggdrasil WebUI

A cross-platform web interface for managing your Yggdrasil node.

**Note:** This project was created with the assistance of ChatGPT.  

**Tested only with:** Windows 11 and Yggdrasil 0.5.12

## Screenshot

![Yggdrasil WebUI](screenshot.jpg)

## Features

- Add/remove peers
- View node information
- Refresh node and peer info
- Start/Stop service (Linux/macOS)
- Manual `yggdrasilctl` path configuration

## Installation

```bash
pip install fastapi uvicorn jinja2
uvicorn app:app --reload
