# API Documentation version 1.0.0

## Overview
This API provides two endpoints for text and image classification.

## Endpoints

### 1. Text Classification
**Endpoint:** `/v1_text`
- **Method:** POST
- **Description:** Classifies text input and returns whether it's valid or not
- **Request Body:**
  ```json
  {
    "predict": "your text here"
  }
  ```
- **Response:**
  ```json
  {
    "predict": "true"  // or "false"
  }
  ```
- **Error Responses:**
  - 400 Bad Request:
    ```json
    {
      "error": "Input harus berupa string"
    }
    ```
  - 500 Internal Server Error:
    ```json
    {
      "error": "Error message details"
    }
    ```

### 2. Image Classification
**Endpoint:** `/v1_image`
- **Method:** POST
- **Description:** Classifies images from URL and returns validity status
- **Request Body:**
  ```json
  {
    "image-link": "https://example.com/image.jpg"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Image downloaded",
    "filepath": "path/to/saved/image",
    "valid": 1  // 1 for invalid, 0 for valid
  }
  ```
- **Error Responses:**
  - 400 Bad Request:
    ```json
    {
      "error": "Input harus berupa string"
    }
    ```
    ```json
    {
      "error": "Invalid URL format"
    }
    ```
  - 500 Internal Server Error:
    ```json
    {
      "error": "Error message details"
    }
    ```

## Usage Example
### Text Classification
```bash
curl -X POST http://localhost:5000/v1_text \
  -H "Content-Type: application/json" \
  -d '{"predict": "your text here"}'
```

### Image Classification
```bash
curl -X POST http://localhost:5000/v1_image \
  -H "Content-Type: application/json" \
  -d '{"image-link": "https://example.com/image.jpg"}'
```