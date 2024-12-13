# Myntra Review Scraper

## Overview

Myntra Review Scraper is a comprehensive web application that allows users to scrape, store, and analyze product reviews from Myntra. The application provides an interactive interface to search for products, extract reviews, store them in a MongoDB database, and generate insightful visualizations and reports.

## Features

- 🔍 Product Review Scraping
  - Search for products on Myntra
  - Scrape reviews for multiple products
  - Extract detailed review information including ratings, comments, and dates

- 💾 Data Storage
  - Store scraped reviews in MongoDB
  - Persistent storage for future analysis
  - Easy retrieval of previously scraped reviews

- 📊 Interactive Dashboard
  - Generate comprehensive visualizations
  - Analyze product ratings
  - Compare product prices
  - View positive and negative reviews
  - Detailed rating distribution

## Prerequisites

- Python 3.8+
- Selenium WebDriver
- Chrome Browser
- MongoDB Atlas Account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/junaidashrafbudoo/Myntra_reviews.git
cd Myntra_reviews
```

2. Create a virtual environment:
```bash
python -m env env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up ChromeDriver:
- Download ChromeDriver compatible with your Chrome browser version
- Add ChromeDriver to your system PATH

## Configuration

1. MongoDB Setup:
- Create a MongoDB Atlas account
- Create a cluster and get your connection string
- Update `src/constants.py` with your MongoDB connection details

2. Environment Variables (Optional):
- Set `MONGO_URL` for database connection
- Set other necessary environment variables

## Usage

### Running the Application

```bash
streamlit run app.py
```

### Scraping Reviews

1. Open the web application
2. Enter a product name
3. Specify the number of products to scrape
4. Click "Scrape Reviews"

### Analyzing Reviews

1. Navigate to the Analysis page
2. View scraped review data
3. Click "Generate Analysis" for detailed insights

## Project Structure

```
myntra-review-scraper/
│
├── src/
│   ├── cloud_io/         # MongoDB integration
│   ├── constants/        # Project constants
│   ├── data_report/      # Dashboard generation
│   ├── exception/        # Custom exception handling
│   ├── scrapper/         # Web scraping logic
│   └── utils/            # Utility functions
│   └── database_connect.py/ # Database connection
├── pages/                # Streamlit application pages
├── app.py                # Main Streamlit application
└── requirements.txt      # Project dependencies
```

## Technologies Used

- Python
- Selenium WebDriver
- Beautiful Soup
- Pandas
- Plotly
- Streamlit
- MongoDB

## Limitations

- Depends on Myntra's website structure
- Limited by Myntra's review loading mechanism
- Requires active maintenance for website changes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

Junaid - junaidashraf.cqai@gmail.com

Project Link: [https://github.com/junaidashrafbudoo/Myntra_reviews](https://github.com/junaidashrafbudoo/Myntra_reviews)
