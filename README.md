# led-strip-control
## Introduction

Run a REST API to control APA102 LED strips. By default you can:

- Pulse LED strip in a direction
- Set a solid colour
- Run a circular rainbow
- Clear strip

However, this is intended to be customised based on usage requirements.

## Pre-requisites

```bash
pip install -r requirements.txt
```

## Usage

Customise your LED layout in `config.json` and run the application.

```bash
python main.py
```

View the `openapi.json` for the specification.
