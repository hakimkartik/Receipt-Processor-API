# Receipt Processor API

This is a Flask-based web service that processes receipts and calculates points based on a set of rules. The application is Dockerized for easy deployment and testing.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Running the Application](#running-the-application)
   - [Option 1: Using the Shell Script](#option-1-using-the-shell-script)
   - [Option 2: Manual Docker Commands](#option-2-manual-docker-commands)
4. [API Endpoints](#api-endpoints)
5. [Testing the API](#testing-the-api)
6. [Stopping the Application](#stopping-the-application)
7. [Cleaning Up](#cleaning-up)

---

## Overview

The Receipt Processor API provides two main endpoints:

1. **Process Receipts**: Submits a receipt for processing and returns a unique ID.
2. **Get Points**: Retrieves the points awarded for a receipt based on its ID.

The application is built using Flask and is Dockerized for easy setup and deployment.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (optional): [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Running the Application

You can run the application in two ways: using a provided shell script or manually with Docker commands.

---

### Option 1: Using the Shell Script

A shell script (`run.sh`) is provided to simplify the process of building and running the Docker container.

#### Steps:

1. Make the script executable:

   ```bash
   chmod +x run.sh
   ```
2. Run the script:

```bash
./run.sh
```
#### What the Script Does:
Builds the Docker image with the tag `receipt-processor`.

Runs the container, mapping port 3000 on your local machine to port 3000 in the container.

---

### Option 2: Manual Docker Commands
If you prefer not to use the shell script, you can manually build and run the Docker container.

#### Steps:
#### Build the Docker image manually:

```bash
docker build -t receipt-processor .
```

Run the Docker container:

```bash
docker run -p 3000:3000 receipt-processor
```
---
## API Endpoints

1. Process Receipts

    Path: /receipts/process

    Method: POST

    Payload: Receipt JSON

    Response: JSON containing an ID for the receipt.

    Example Request:
    ```bash
    curl -X POST http://localhost:3000/receipts/process \
    -H "Content-Type: application/json" \
    -d '{
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        },
        {
          "shortDescription": "Emils Cheese Pizza",
          "price": "12.25"
        }
      ],
      "total": "18.74"
    }'
   ```
   
    Example Response:

    ```json
    { "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }
   ```
   
2. Get Points
Path: /receipts/{id}/points

    Method: GET

    Response: JSON containing the number of points awarded.

    Example Request:

    ```bash
    curl -X GET http://localhost:3000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points
    ```
   
    Example Response:

    ```json
    { "points": 32 }
    ```

---

## Testing the API
You can test the API using tools like curl, Postman, or any other HTTP client. Examples are provided in the API Endpoints section.

---

## Stopping the Application
To stop the running container:

Find the container ID:

```bash
docker ps
```
Stop the container:

```bash
docker stop <container_id>
```

---

## Cleaning Up

To remove the Docker image and free up space:

Remove the container (if it still exists):

```bash
docker rm <container_id>
```

Remove the Docker image:
```bash
docker rmi receipt-processor
```

---

## Notes

The application stores data in memory, so it will not persist after the container is stopped.

The API is designed to be simple and lightweight, making it easy to test and integrate.