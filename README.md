# KBO Data Portal - API Server

This repository provides a web-based interface and public API for exploring KBO data. Built with Flask, it supports both interactive visualizations and programmatic access to collected and processed data from the KBO Data Pipeline.

## Usage

The web service and API are built on Flask and can be run locally or containerized.

1. **Clone the repository**
    ```bash
    git clone https://github.com/kbo-data-portal/api-server.git
    cd api-server
    ```

2. **Install dependencies (Local environment only)**
    ```bash
    pip install -r requirements.txt
    ```

3. **Start the Local Server**
    ```bash
    flask run
    ```

The server will be available at [http://localhost:5000/](http://localhost:5000/).

### Run with Docker

You can run the service easily using Docker and Docker Compose.

1. **Build and start containers**
    ```bash
    docker-compose up --build
    ```

2. **Access the service**
    - Open your browser and go to [http://localhost/](http://localhost/).

3. **Stop containers**
    ```bash
    docker-compose down
    ```

#### Environment Variables

- Create a `.env` file in the project root (if not provided) to set environment variables like database credentials.
- This file is automatically used by Docker Compose if configured.

```bash
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
DB_NAME=<your_db_name>
```

## Structure
- `fetcher/`
    - Responsible for database queries and data processing. Keeps data logic separate from routing.
- `routes/`
    - Defines API endpoints and web routes.
        - `/web` for the web interface (charts, tables, visualizations)
        - `/chatbot` for Kakao chatbot APIs (game schedule, predictions)
- `static/`
    - Contains CSS, JavaScript, images, and other static assets for the web frontend.
- `templates/`
    - Holds HTML templates for rendering the web pages.

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

