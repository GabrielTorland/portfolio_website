# My Portfolio Website

Welcome to the GitHub repository for my personal portfolio website. You can view the live version at [https://www.gabrieltorland.com/](https://www.gabrieltorland.com/).

This repository contains all the necessary code to set up and host your own version of the website. Here's how you can get started:

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose
- Git (for cloning the repo)

## Getting Started

### 1. Clone the Repository

To get started with your own instance of the website, you can either fork this repository or clone it directly using Git:

```bash
git clone git@github.com:GabrielTorland/portfolio_website.git
```

### 2. Set Environment Variables

Next, you'll need to set up the required environment variables. Create a .env file in the root directory of the project and fill in the following variables:
```css
SMTP_SERVER= [SMTP server address]
SMTP_PORT= [SMTP port]
SMTP_USER= [SMTP username]
SMTP_PASSWORD= [SMTP password]
SMTP_RECEIVER= [Email address to receive notifications]
REDIS_URL= [URL of your Redis server]
DATABASE_URI= [Your database URI]
POSTGRES_USER= [Postgres username]
POSTGRES_PASSWORD= [Postgres password]
DB_NAME= [Database name]
```

### 3. Build the Docker Image

Now, build the Docker image for the portfolio website. You can tag it as portfolio-website for simplicity:
```bash
docker build -t portfolio-website .
```
If you prefer a different name, remember to update the Docker Compose file accordingly.

### 5. Launch the Website

Finally, start the website using Docker Compose:
```bash
docker-compose up -d
```
Your website should now be accessible at http://your_ip:2378.
