# KBO Data Portal - API Server

This repository provides a web-based interface and public API for exploring KBO data.
Built with Flask, it supports both interactive visualizations and programmatic access to collected and processed data from the KBO Data Pipeline.

## Feature

- Flask-based web service and REST API for KBO data
- Interactive web visualizations (charts, tables)
- Public API endpoints for programmatic access
- Supports both local and Docker-based deployment
- Environment variable configuration via `.env` file

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/kbo-data-portal/api-server.git
   cd api-server
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Local Server

```bash
flask run
```

Then, visit http://localhost:5000/ in your browser.

### Run with Docker

```bash
docker-compose up --build
```

Then, visit http://localhost/ in your browser.

### Environment Variables

Create a `.env` file in the project root to configure environment variables such as database credentials:

```bash
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=<your_db_port>
DB_NAME=<your_db_name>
```

This file is automatically used by Docker Compose if configured properly.

## Structure

- `fetcher/` — Handles database queries and data processing.
- `routes/` — Defines API endpoints and web routes.
  - `/web` — Web interface (charts, tables, visualizations)
  - `/chatbot` — Kakao chatbot APIs (game schedule, predictions)
- `static/` — Static assets (CSS, JS, images)
- `templates/` — HTML templates for rendering web pages.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
