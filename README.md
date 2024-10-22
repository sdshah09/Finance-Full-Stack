# Stock Prediction and Reporting System

## Overview

This project is a Django-based web application for predicting stock prices using historical data fetched from Yahoo Finance via the `yfinance` library. It stores actual and predicted stock prices in a PostgreSQL database and generates detailed PDF reports, including visualizations and performance metrics such as total return and max drawdown.

The system is deployed on **AWS EC2** using **Docker** and connects to **AWS RDS** for database management. Continuous Integration and Deployment (CI/CD) are managed using **GitHub Actions**.

## Features

- Fetch historical stock prices from Yahoo Finance.
- Train a machine learning model using `scikit-learn` (Linear Regression) to predict future stock prices.
- Store actual and predicted stock prices in a PostgreSQL database.
- Generate a PDF report with performance metrics and a comparison plot of actual vs. predicted prices.
- Use **Docker** for containerization and deployment on **AWS EC2**.
- CI/CD pipeline with **GitHub Actions** for automated deployment.

## Tech Stack

- **Backend**: Django, Python, PostgreSQL (AWS RDS)
- **Machine Learning**: scikit-learn (Linear Regression)
- **Data Source**: yfinance (Yahoo Finance)
- **Containerization**: Docker
- **Deployment**: AWS EC2, AWS RDS
- **CI/CD**: GitHub Actions
- **PDF Generation**: WeasyPrint
- **Plotting**: matplotlib

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sdshah09/Finance-Full-Stack.git
cd Finance-Full-Stack
```

### 2. Environment Variables

Create a `.env` file in the root directory to store environment variables required for Django, database connections, and API keys.

Example `.env`:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-ec2-public-ip,localhost,127.0.0.1
DATABASE_NAME=your-database-name
DATABASE_USER=your-db-username
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-rds-endpoint
DATABASE_PORT=5432
```

### 3. Build and Run with Docker

This project uses Docker to simplify the setup process.

- **Build the Docker image**:

```bash
docker-compose build
```

- **Run the containers**:

```bash
docker-compose up -d
```

The Django application will now be running on your EC2 instance.

### 4. Database Migrations

Run the following commands to apply the migrations and create the necessary tables in your PostgreSQL database:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 5. Accessing the Application

Once the application is running, you can access it by visiting:

```
http://<EC2_PUBLIC_IP>:8000
```

Replace `<EC2_PUBLIC_IP>` with your AWS EC2 instance's public IP address.

## Usage

### Fetching and Storing Stock Data

To fetch stock data and store it in the database, you can run the following Django management command:

```bash
docker-compose exec web python manage.py fetch_stock_data --symbol=AAPL
```

This will fetch historical stock data for the symbol `AAPL` and store it in the database.

### Training the Machine Learning Model

To train a machine learning model and predict future stock prices, run:

```bash
docker-compose exec web python manage.py train_model --symbol=AAPL
```

### Generating PDF Reports

You can generate a stock prediction report by visiting the following URL in your browser:

```
http://<EC2_PUBLIC_IP>:8000/report/?symbol=AAPL
```

This will generate a PDF report with actual and predicted stock prices for the symbol `AAPL`.

## Deployment with CI/CD (GitHub Actions)

### CI/CD Pipeline

This project uses **GitHub Actions** for continuous integration and deployment. The pipeline is defined in `.github/workflows/deploy.yml` and includes the following steps:

- **Build Docker Image**: Builds the Docker image using Docker Compose.
- **Push to Docker Hub**: The image is pushed to Docker Hub (if configured).
- **Deploy to AWS EC2**: The application is deployed on the EC2 instance using SSH.

### AWS EC2 and RDS Setup

1. **AWS EC2**: Set up an EC2 instance with Docker and Docker Compose installed.
2. **AWS RDS**: Set up an AWS RDS instance with PostgreSQL and update your `.env` file with the RDS connection details.

#### GitHub Secrets

Ensure that the following secrets are set in your GitHub repository for the CI/CD pipeline to work:

- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password.
- `EC2_HOST`: The public IP address of your EC2 instance.
- `EC2_USER`: The username for your EC2 instance (e.g., `ubuntu` for default AMIs).
- `EC2_PRIVATE_KEY`: The private SSH key for accessing your EC2 instance.
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`: Your RDS database credentials.

### Deploying Changes

To deploy changes, simply push your changes to the `main` branch, and the GitHub Actions workflow will automatically build and deploy the updated version to your AWS EC2 instance.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


### Additional Notes:

1. **AWS Setup**:
   - **EC2**: Make sure that your EC2 instance has the necessary security group settings to allow traffic on port `8000` and SSH access for deployment.
   - **RDS**: Ensure that your RDS instance is accessible from the EC2 instance (by whitelisting the EC2 security group in RDS settings).

2. **GitHub Actions**:
   - The GitHub Actions CI/CD pipeline should already be configured, but ensure that all the necessary secrets are set in your GitHub repository.

---

