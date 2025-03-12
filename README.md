# Dynamsoft Server

Follow these steps to get the Dynamsoft Server up and running:

### 1. Clone the Repository
Run the following command to clone the repository:

```bash
git clone git@github.com:smujtaba1/dynamsoft-server.git
```

### 2. Navigate to the Project Directory
Change into the `dynamsoft-server` directory:

```bash
cd dynamsoft-server
```

### 3. Set Up and Start the Server
Run the following commands to set up the environment and start the server:

1. Set the `DYNAMSOFT_LICENSE` environment variable with your license string:

   ```bash
   export DYNAMSOFT_LICENSE=[license string]
   ```

2. Start the server:

   ```bash
   sh start.sh
   ```

### 4. Verify the Server is Running
The uWSGI server should start listening for requests on port `5000`. To confirm everything is working correctly:

1. Open your browser and visit `http://localhost:5000`.
2. You should see the API documentation load upon a GET request.

#### Note:
This recurring warning is not critical and doesn’t affect the main function:

```
uwsgi_check_logrotate()/lseek(): Illegal seek [core/logging.c line 494]
```

