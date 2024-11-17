# CCTV System - Camera Feature Branch

This repository contains the source code for a CCTV system under development, focusing on camera integration, streaming, and management features available in the `camera_feature` branch.

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

- **Python 3.x**
- **Git**
- (Optional) A virtual environment manager such as `venv` or `virtualenv`.

### Step 1: Clone the Repository

```bash
git clone -b camera_feature https://github.com/agrin10/cctv.git
cd cctv
```

### Step 2: Build the Environment

Run the `build.bat` script to install all necessary dependencies and set up the environment.

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command:

```bash
build.bat

```

This script will:

- Install required Python packages specified in `requirements.txt`.
- Set up any additional environment variables or dependencies.

### Step 3: Run the Application

After setting up the environment, use the `run.bat` script to start the application:

```bash
run.bat
```

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
  
Monitor Feeds

- View live video streams from connected cameras.
- Manage recordings directly from the dashboard.

---

## Development Workflow

1. Make Changes: Add new features, fix bugs, or improve existing functionality.
2. Test Locally: Run the application locally using run.bat to ensure your changes work as expected.
3. Commit and Push Changes:

```bash 
git add .
git commit -m "Describe your changes here"
git push origin camera_feature
```

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

## Troubleshooting

- Environment Setup Issues:
  - Ensure all dependencies in `requirements.txt` are installed correctly.
  - Verify that the Python environment is properly configured.
  - If problems persist, delete the environment and rebuild it using `build.bat`.
- Application Fails to Start:
  - Check for any logs or error messages in the console.
- Cannot Connect to Cameras:
  - Ensure the camera's IP address, username, and password are correct.
  - Verify that the camera supports RTSP or the configured protocol.
  
---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---
