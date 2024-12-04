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


## Endpoints

### 1. Trigger Rainbow Circle

- **Endpoint:** `GET /api/circle`
- **Summary:** Activates the rainbow circle effect on the LED strip.
- **Response:**
  - **200:** Successful Response

### 2. Pulse LED Strip

- **Endpoint:** `GET /api/pulse-direction`
- **Summary:** Pulses the LED strip in a specified direction.
- **Description:** 
  - **Args:**
    - `direction` (int): The direction to pulse.
      - `0`: Bottom
      - `1`: Left
      - `2`: Top
      - `3`: Right
- **Parameters:**
  - `direction` (required, integer): Direction of the pulse.
- **Responses:**
  - **200:** Successful Response
  - **422:** Validation Error

### 3. Clear LED Strip

- **Endpoint:** `GET /api/clear`
- **Summary:** Clears any effects on the LED strip.
- **Response:**
  - **200:** Successful Response

### 4. Set Solid Color

- **Endpoint:** `POST /api/solid`
- **Summary:** Sets the LED strip to a solid color.
- **Description:** Expects a JSON body with a `color` key and a valid hex code.
- **Response:**
  - **200:** Successful Response

## Error Schemas

### HTTPValidationError

- **Properties:**
  - `detail` (array): List of validation error details.

### ValidationError

- **Properties:**
  - `loc` (array): Location of the error.
  - `msg` (string): Error message.
  - `type` (string): Type of the error.
