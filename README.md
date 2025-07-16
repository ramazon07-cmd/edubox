# EduBox - Modern Learning Platform

[![Django CI/CD Pipeline](https://github.com/yourusername/edubox/actions/workflows/django-ci.yml/badge.svg)](https://github.com/yourusername/edubox/actions/workflows/django-ci.yml)
[![codecov](https://codecov.io/gh/yourusername/edubox/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/edubox)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EduBox is a comprehensive learning platform built with Django and Django REST Framework that enables educators to create courses and students to enroll in them.

## Features

- Course creation and management
- Student enrollment system
- REST API with Swagger documentation
- Authentication and permissions
- Asynchronous task processing with Celery
- Automated testing and CI/CD pipeline

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for Celery)
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/edubox.git
   cd edubox
   ```

2. Set up environment variables (see .env.template)

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Using Docker

You can also run the application using Docker:

```bash
docker-compose up
```

## API Documentation

API documentation is automatically generated using drf-yasg and is available at:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Testing

Run tests with:

```bash
python manage.py test
```

For test coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.