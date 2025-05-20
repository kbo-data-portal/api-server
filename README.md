# KBO Data Portal

This repository provides a web-based interface for exploring KBO data, built with Flask. It serves as the frontend for visualizing collected and processed data from the KBO Data Pipeline.

## Usage
The web service and API are built on Flask and can be run locally or containerized.
1. **Clone the repository**
    ```bash
    git clone https://github.com/leewr9/kbo-data-portal.git
    cd kbo-data-portal

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Start the Local Server**
    ```bash
    flask run
    ```

The server will be available at [http://localhost:5000/](http://localhost:5000/).

## Structure
- `fetcher/`
    - Responsible for database queries and data processing. Keeps data logic separate from routing.
- `routes/`
    - Defines API endpoints and web routes, divided into
        - `/web` for the web interface (charts, tables, visualizations)
        - `/chatbot` for Kakao chatbot APIs (game schedule, predictions)
- `static/`
    - Contains CSS, JavaScript, images, and other static assets for the web frontend.
- `templates/`
    - Holds HTML templates for rendering the web pages.

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

