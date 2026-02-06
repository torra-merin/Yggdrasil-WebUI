# Yggdrasil WebUI

A cross-platform web interface for managing your Yggdrasil node. The user must have [Yggdrasil](https://yggdrasil-network.github.io/) installed on their system to use this WebUI.

**Tested only with:** Windows 11 and Yggdrasil 0.5.12

**Note:** This is an unofficial web interface for Yggdrasil Network and is not affiliated with or endorsed by the Yggdrasil developers. This project was made for fun with the help of ChatGPT. 
Icon by OpenClipart-Vectors, licensed via [Pixabay](https://pixabay.com/es/vectors/hoja-planta-verde-ecolog%c3%ada-147490/).

## Screenshot

![Yggdrasil WebUI](screenshot.jpg)

## Features

- Add/remove peers
- View node information
- Refresh node and peer info
- Start/Stop service (Linux/macOS)
- Manual `yggdrasilctl` path configuration

## Installation

1. Download the code and extract it.
2. Open a command line in the project folder.
3. Install the dependencies:
```bash

pip install fastapi uvicorn jinja2

```
4. Run main.py.
