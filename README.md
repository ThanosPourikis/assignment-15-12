## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python 3.12
### Urls
1. [App](http://localhost:8000)
2. [Prometheus](http://localhost:9090)
### Quick Run
1. Clone the repo
   ```sh
   git clone git@github.com:ThanosPourikis/assignment-15-12.git
   ```
2. Access directory
    ```sh 
   cd assignment-15-12
    ```
3. Within the directory
    ```sh
    docker compose up
    ```
### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone git@github.com:ThanosPourikis/assignment-15-12.git
   ```
2. Create venv
   ```sh
   python3.12 -m venv venv
   ```
3. Activate Venv
    ```sh
    source venv/bin/activate
    ```
4. Install project
    ```sh
   cd assignment-15-12
   pip install .
   ```
5. Declare the only environment variable needed
   ```sh
   export DATA_FOLDER=<path_to_folder>
   ```
6. Run the Startup script
   ```sh
   startup -f $DATA_FOLDER
   ```
7. Start server
    ```sh
   cd src
   uvicorn app.main:app --log-config=../conf/log_conf.yaml --workers=4
    ```
