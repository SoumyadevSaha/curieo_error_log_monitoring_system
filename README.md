# Error Log Monitoring System

## Problem Statement

In an error log monitoring platform, each log entry comprises three properties:

1. **Timestamp**: A 64-bit integer representing the time when the error occurred.
2. **Log Type**: A string with a maximum length of 100 characters describing the type or category of the error.
3. **Log Severity**: A floating-point value indicating the severity level of the error.

The log entry format is as follows: `TIMESTAMP; LOG_TYPE; SEVERITY`. For example: `1715744138011; INTERNAL_SERVER_ERROR; 23.72`.

### Operations

1. **1 timestamp; log_type; severity**: Submit a new log entry to the platform.
2. **2 log_type**: Compute the min, max, and mean severity of the log entry associated with the specified log type.
3. **3 BEFORE timestamp**: Compute the min, max, and mean severity of all log entries occurring before the specified timestamp.
4. **3 AFTER timestamp**: Compute the min, max, and mean severity of all log entries occurring after the specified timestamp.
5. **4 BEFORE log_type timestamp**: Compute the min, max, and mean severity of all log entries occurring before the specified timestamp and associated with the specified log type.
6. **4 AFTER log_type timestamp**: Compute the min, max, and mean severity of all log entries occurring after the specified timestamp and associated with the specified log type.

## Approach

### Data Structures

- **SegmentTree**: A class to manage a segment tree that stores log entries.
  - **update()**: Updates the segment tree with a new value.
  - **query()**: Queries the segment tree for statistics (min, max, sum, count) over a range.
- **LogMonitor**: A class to manage and process log entries using the segment tree.
  - **add_log()**: Adds a new log entry.
  - **get_details_type2()**: Gets min, max, and mean severity for a specific log type.
  - **get_details_type3()**: Gets min, max, and mean severity before or after a specific timestamp.
  - **get_details_type4()**: Gets min, max, and mean severity for a log type before or after a specific timestamp.

## Running the Application

### Prerequisites

- Docker installed on your system.

### Instructions

1. **Clone the repository**

    ```sh
    git clone https://github.com/SoumyadevSaha/curieo_error_log_monitoring_system.git
    cd curieo_error_log_monitoring_system
    ```

2. **Create a Dockerfile**

    Create a `Dockerfile` in the root directory of the project and add the following content:

    ```Dockerfile
    # Use the official Python image from the Docker Hub
    FROM python:3.9-slim

    # Set the working directory
    WORKDIR /app

    # Copy the requirements file into the container
    COPY requirements.txt requirements.txt

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of the working directory contents into the container at /app
    COPY . .

    # Command to run the Python script
    CMD ["python", "log_monitor.py"]
    ```

3. **Create a requirements.txt**

    Create a `requirements.txt` file in the root directory of the project. If your script has any dependencies, list them here. If not, leave it empty.

    ```txt
    # Example dependencies
    # numpy==1.21.0
    ```

4. **Build the Docker Image**

    In the terminal, navigate to the project directory and build the Docker image:

    ```sh
    docker build -t error-log-monitor .
    ```

5. **Run the Docker Container**

    Run the Docker container, mounting the current directory to `/app` in the container:

    ```sh
    docker run -v $(pwd):/app error-log-monitor
    ```

6. **Provide Input**

    Ensure your `input.txt` file is in the same directory before running the container. The container reads from `input.txt` and writes the results to `output.txt`.

### Example Commands

#### Input File: `input.txt`

```txt
1 1715744138011; INTERNAL_SERVER_ERROR; 23.72
2 INTERNAL_SERVER_ERROR
3 BEFORE 1715744138011
4 AFTER INTERNAL_SERVER_ERROR 1715744138011
```

## Explanation of Functions and Classes

### 'SegmentTree' Class

- `__init__(self, size)`: Initializes the segment tree with the given size.
- `updateST(self, node, start, end, idx, value)`: Recursively updates the segment tree nodes.
- `update(self, idx, value)`: Public method to update the segment tree at a specific index with a given value.
- `queryST(self, node, start, end, left, right)`: Recursively queries the segment tree for a range.
- `query(self, left, right)`: Public method to query the segment tree for a range.

### 'LogMonitor' Class

- `__init__(self, nodes, log_types, timestamp_to_idx)`: Initializes the log monitor with given nodes, log types, and timestamp index mapping.
- `set_precision(self, value)`: Formats the value to a specific precision.
- `add_log(self, log)`: Adds a new log entry and updates the segment trees.
- `get_details_type2(self, log_type)`: Retrieves min, max, and mean severity for a specific log type.
- `get_details_type3(self, command, timestamp)`: Retrieves min, max, and mean severity before or after a specific timestamp.
- `get_details_type4(self, command, log_type, timestamp)`: Retrieves min, max, and mean severity for a specific log type before or after a specific timestamp.

### Helper Functions

- `write_to_file(result, file_name='output.txt')`: Writes the result to an output file.
- `preprocess_input(commands)`: Preprocesses the input to extract unique timestamps and log types.
- `main(input_file='input.txt', output_file='output.txt')`: Main function to read input, process commands, and write output.

## Conclusion

This project demonstrates the use of segment trees to efficiently manage and query log entries based on timestamp and log type. The solution is dockerized to ensure portability and ease of deployment across different environments.
