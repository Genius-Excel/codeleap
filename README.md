# CodeLeap Careers API

A Django REST Framework (DRF) project for managing job posts, built as part of the CodeLeap assessment.

## Features

- Create, retrieve, update, and delete job posts
- Health check endpoint for service monitoring
- Supports SQLite, PostgreSQL, and MySQL (via `.env` configuration)
- API documentation available [here](https://documenter.getpostman.com/view/43539597/2sBXcKDeRq)

## Endpoints

- `GET /careers/` — List all posts
- `POST /careers/` — Create a new post
- `PATCH /careers/<post_id>/` — Update a post
- `DELETE /careers/<post_id>/` — Delete a post
- `GET /careers/health/` — Health check

## Setup

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your environment variables.
3. Install dependencies:
   ```sh
   pip install -r requirements.txt