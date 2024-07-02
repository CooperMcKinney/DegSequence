# DegSequence Analysis

This project analyzes sequencing data using a Streamlit application.

## Prerequisites

- Docker
- Visual Studio Code
- Visual Studio Code Remote - Containers extension

## Setup Instructions

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/DegSequence.git
    cd DegSequence
    ```

2. **Open the project in Visual Studio Code:**

    ```sh
    code .
    ```

3. **Open the project in a development container:**

    - Open the Command Palette (Ctrl+Shift+P), and select **Remote-Containers: Open Folder in Container**.

4. **Run the Streamlit application:**

    Once the development container is running, the app should automatically start. If it doesn't, you can manually start it by running the following command in the terminal:

    ```sh
    streamlit run Illumina_Analysis.py
    ```

5. **Access the application:**

    Open your web browser and navigate to `http://localhost:8501`.

## File Upload Limit

To handle large file uploads (up to 3GB), the `config.toml` file has been configured accordingly.
