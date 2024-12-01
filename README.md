# CCTV System

This repository contains the source code for a CCTV system under development, focusing on camera integration, streaming, and management features.

---

## Features

- **Camera Integration**:
  - Connect and configure multiple CCTV cameras.
  - Support for RTSP streams.

- **Live Streaming**:
  - View live video feeds from connected cameras.
  - Optimized for real-time performance.

---

## Installation and Setup

### Prerequisites

Before running the application, ensure the following are installed on your system:

- **Docker**: Install Docker from [here](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Comes bundled with Docker Desktop.

### Step 1: Clone the Repository

Clone the repository from GitHub:

```bash
git clone -b camera_feature https://github.com/agrin10/cctv.git
cd cctv
```

### Step 2: Build and Run the Docker Containers

Use Docker Compose to build and run the application. This process will handle installing dependencies and setting up the environment.

Run the following command:

```bash
docker-compose up --build
```

This command will:

- Build the Docker images specified in the `docker-compose.yml` file.
- Start the application and its dependencies.

---

## Usage

### Access the Dashboard

Once the application is running, open your web browser and navigate to:

```plaintext
http://localhost:5000
```

### Add Cameras

- Use the dashboard interface to configure camera details such as:
  - Camera name.
  - Camera IP address.
  - Username and password for authentication.

### Monitor Feeds

- View live video streams from connected cameras.
- Manage recordings directly from the dashboard.

---

## Development Workflow

1. Make Changes: Add new features, fix bugs, or improve existing functionality.
2. Test Locally: Build and run the application using Docker to ensure your changes work as expected.
3. Commit and Push Changes:

```bash
git add .
git commit -m "Describe your changes here"
git push origin camera_feature
```

---

## Troubleshooting

- **Docker Issues**:
  - Ensure Docker Desktop is running before executing `docker-compose`.
  - Verify that ports specified in `docker-compose.yml` are not in use by other services.
- **Environment Setup Issues**:
  - Ensure the `docker-compose.yml` file is correctly configured.
  - Delete and rebuild the containers using:
  
    ```bash
    docker-compose down
    docker-compose up --build
    ```

- **Application Fails to Start**:
  - Check logs for errors using:
  
    ```bash
    docker-compose logs
    ```

- **Cannot Connect to Cameras**:
  - Ensure the camera's IP address, username, and password are correct.
  - Verify that the camera supports RTSP or the configured protocol.

---

## Contributing

We welcome contributions from the community! Follow these steps to contribute:

1. Fork the Repository: Click the "Fork" button on the repository page.
2. Create a Feature Branch:

    ```bash
    git checkout -b feature_name
    ```

3. Make Changes: Add your improvements or new features.

4. Commit and Push Changes:

    ```bash
    git add .
    git commit -m "Your commit message"
    git push origin feature_name
    ```

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
