import pandas as pd  #pandas for data manipulation
import streamlit as st  # Importing Streamlit for web application interface
from src.cloud_io import MongoIO

from src.constants import SESSION_PRODUCT_KEY  # Importing session key constant
from src.scrapper.scrape import ScrapeReviews  # Importing the scraper for extracting reviews

# Set the page configuration for the Streamlit app
st.set_page_config(
    "myntra-review-scrapper"  # Page title for the app
)

# Display the main title of the app
st.title("Myntra Review Scrapper")

# Initialize session state to store whether data is available
st.session_state["data"] = False

# Define the input form function
def form_input():
    """
    Collects user input for the product name and number of products to scrape.
    Initiates the scraping process and stores the scrapped data in MongoDB.

    Returns:
        None
    """
    # Text input for the product to search reviews for
    product = st.text_input("Search Products")

    # Store the product name in session state
    st.session_state[SESSION_PRODUCT_KEY] = product

    # Input for the number of products to scrape, with validation for minimum value
    no_of_products = st.number_input("Enter Number of Products to Search", step=1, min_value=1)

    # Button to trigger the scraping process
    if st.button("Scrape Reviews"):
        # Initialize the scraper with product name and number of products
        scrapper = ScrapeReviews(
            product_name=product,
            no_of_products=int(no_of_products)
        )

        # Get the scraped review data
        scrapped_data = scrapper.get_review_data()

        if scrapped_data is not None:
            # Update session state to indicate data is available
            st.session_state["data"] = True

            # Initialize MongoDB interaction object
            mongoio = MongoIO()

            # Store the scraped reviews into MongoDB
            mongoio.store_reviews(product_name=product, reviews=scrapped_data)
            print("Stored Data into MongoDB")  # Log success in console

        # Display the scraped data as a DataFrame in the app
        st.dataframe(scrapped_data)

# Check if the script is the main module
if __name__ == "__main__":
    # Call the form input function to display input fields and process data
    data = form_input()