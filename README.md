# OU-Library

OU-Library is a web-based library management system built with Flask. It supports user authentication, book management, borrowing/return tracking, and statistics visualization. The project aims to streamline library operations and provide an intuitive experience for both library staff and users.

## Features

- User authentication (including Google OAuth login)
- User registration and email verification
- Book catalog browsing and management
- Borrow/return tracking for users
- Overdue and current borrow monitoring
- Borrowing statistics visualized with charts
- Responsive UI with modern CSS and JS frameworks

## Technology Stack

- Python 3.11
- Flask & Flask extensions (Flask-Login, Flask-Dance, Flask-SQLAlchemy)
- Cloudinary (for image hosting)
- SendGrid (for email verification)
- Bootstrap 5, Slick Carousel (for frontend)
- Docker support

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- A .env file with the following keys:
  - `DB_URL`, `DB_PASSWORD`, `SECRET_KEY`, `CLIENT_ID`, `CLIENT_SECRET`

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tanle9t2/OU-Library.git
   cd OU-Library
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your credentials.

4. **Run the application:**
   ```bash
   flask run
   ```

   Or with Docker:
   ```bash
   docker build -t ou-library .
   docker run -p 5000:5000 ou-library
   ```

### Running with Jenkins & SonarQube

A Jenkins pipeline (`Jenkinsfile`) is provided for CI/CD, including SonarQube static analysis.

## Usage

- Visit the home page to browse the library catalog.
- Register a new account or log in (Google OAuth supported).
- Monitor your borrows and manage book returns.
- Library staff can view borrowing statistics and user activity.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

- Tân Lê

---
Feel free to contribute or open issues on the [GitHub repository](https://github.com/tanle9t2/OU-Library).