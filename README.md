# EcoPlant

## To-Do
- [x] Dokerize project
- [ ] Migrate to Postgres DB (acctually SQLite)
- [ ] Implement AI
  
## Deployment

compose.yaml

```yaml
version: "3"
services:
  db:
    image: postgres:14.1
    environment:
      POSTGRES_DB: ecoplant
      POSTGRES_USER: ecoplant
      POSTGRES_PASSWORD: ecoplant
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - 7432:5432
  backend:
    build:
      context: https://github.com/Yirade/EcoPlant.git
      dockerfile: src/Dockerfile
    ports:
      - 8070:8000
    env_file:
      - .env
    depends_on:
      - db
volumes:
  pgdata: null
networks: {}
```

## API Endpoints

### Login

- **URL**: `/login/`
- **Method**: `POST`
- **Auth required**: NO
- **Data Params**: 
    - `username`: string
    - `password`: string
- **Description**: Authenticates the user and returns a refresh and an access token.
- **Example Body**:
    ```json
    {
        "username": "example",
        "password": "examplepassword"
    }
    ```

### Registration

- **URL**: `/register/`
- **Method**: `POST`
- **Auth required**: NO
- **Data Params**: 
    - `username`: string
    - `password`: string
    - `email`: string
- **Description**: Registers a new user and returns a message along with a refresh and an access token.
- **Example Body**:
    ```json
    {
        "username": "example",
        "password": "examplepassword",
        "email": "example@example.com"
    }
    ```

### Token Refresh

- **URL**: `/token/refresh/`
- **Method**: `POST`
- **Auth required**: YES
- **Description**: Refreshes the JWT token.

### Token Check

- **URL**: `/token/check/`
- **Method**: `GET`
- **Auth required**: YES
- **Description**: Verifies if the provided JWT token is valid.

### Device Data

- **URL**: `/device-data/`
- **Method**: `POST`
- **Auth required**: YES
- **Data Params**: 
    - `device_id`: string
    - `air_temperature`: float
    - `air_humidity`: float
    - `soil_moisture`: float
    - `water_level`: float
    - `light`: bool
- **Description**: Adds sensor data for a specific device.
- **Example Body**:
    ```json
    {
        "device_id": "exampledeviceid",
        "air_temperature": 23.5,
        "air_humidity": 45.0,
        "soil_moisture": 30.0,
        "water_level": 75.0,
        "light": true
    }
    ```

### User Device Data

- **URL**: `/user-device-data/`
- **Method**: `GET`
- **Auth required**: YES
- **Description**: Returns all sensor data for all devices of the authenticated user.

### Device Registration

- **URL**: `/register-device/`
- **Method**: `POST`
- **Auth required**: YES
- **Data Params**: 
    - `device_id`: string
    - `name`: string
- **Description**: Registers a new device for the authenticated user.
- **Example Body**:
    ```json
    {
        "device_id": "exampledeviceid",
        "name": "Example Device"
    }
    ```

### User Devices

- **URL**: `/user-devices/`
- **Method**: `GET`
- **Auth required**: YES
- **Description**: Returns all devices of the authenticated user.

### Device Sensor Data

- **URL**: `/device-sensor-data/`
- **Method**: `POST`
- **Auth required**: YES
- **Data Params**: 
    - `device_id`: string
- **Description**: Returns all sensor data for the specified device.
- **Example Body**:
    ```json
    {
        "device_id": "exampledeviceid"
    }
    ```

### User Detail

- **URL**: `/user-detail/`
- **Method**: `GET`
- **Auth required**: YES
- **Description**: Returns the details of the authenticated user.

### Device Command

- **URL**: `/device-command/`
- **Method**: `POST`
- **Auth required**: YES
- **Data Params**: 
    - `device_id`: string
    - `command`: string
- **Description**: Sends a command to a specific device.
- **Example Body**:
    ```json
    {
        "device_id": "exampledeviceid",
        "command": "examplecommand"
    }
    ```
