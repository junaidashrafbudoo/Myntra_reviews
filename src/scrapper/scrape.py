from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.exception import CustomException
from bs4 import BeautifulSoup as bs
import pandas as pd
import os,sys
import time
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
import sys
from src.exception import CustomException  # Assuming this is a custom exception class

class ScrapeReviews:
    def __init__(self, product_name: str, no_of_products: int):
        """
        Initialize the ScrapeReviews class with product name and number of products to scrape.
        Sets up a Chrome WebDriver session with options.
        """
        options = Options()
        # Uncomment these lines if you need to run Chrome in headless mode
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")

        # Start a new Chrome browser session
        self.driver = webdriver.Chrome(options=options)
        self.product_name = product_name
        self.no_of_products = no_of_products

    def scrape_product_urls(self, product_name: str):
        """
        Scrapes product URLs from Myntra based on the product name.

        Args:
        - product_name (str): The name of the product to search.

        Returns:
        - product_urls (list): A list of product URLs.
        """
        try:
            # Replace spaces in the product name with dashes for the search query
            search_string = product_name.replace(" ", "-")
            # Encode the search string for use in a URL
            encoded_query = quote(search_string)

            # Navigate to the Myntra search URL
            self.driver.get(
                f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}"
            )

            # Get the page source and parse it with BeautifulSoup
            myntra_text = self.driver.page_source
            myntra_html = bs(myntra_text, "html.parser")

            # Find the container with the product results
            pclass = myntra_html.find_all("ul", {"class": "results-base"})

            product_urls = []

            # Extract product URLs from the search results
            for i in pclass:
                href = i.find_all("a", href=True)
                for product_no in range(len(href)):
                    t = href[product_no]["href"]
                    product_urls.append(t)

            return product_urls

        except Exception as e:
            # Handle exceptions and raise a custom exception with error details
            raise CustomException(e, sys)

   



    def extract_reviews(self, product_link: str):
        """
        Extract reviews, ratings, and product details from the given product link.

        Args:
        - product_link (str): Partial URL for the product page.

        Returns:
        - product_reviews (BeautifulSoup object): Parsed HTML content for the reviews section, if available.
        """
        try:
            # Construct the full product URL
            productLink = "https://www.myntra.com/" + product_link
            self.driver.get(productLink)  # Open the product page
            prodRes = self.driver.page_source  # Get the HTML source
            prodRes_html = bs(prodRes, "html.parser")

            # Extract product title
            title_h = prodRes_html.find_all("title")
            self.product_title = title_h[0].text

            # Extract overall product rating
            overallRating = prodRes_html.find_all("div", {"class": "index-overallRating"})
            for i in overallRating:
                self.product_rating_value = i.find("div").text

            # Extract product price
            price = prodRes_html.find_all("span", {"class": "pdp-price"})
            for i in price:
                self.product_price = i.text

            # Find the reviews section
            product_reviews = prodRes_html.find("a", {"class": "detailed-reviews-allReviews"})
            if not product_reviews:
                return None  # Return None if no reviews are available

            return product_reviews

        except Exception as e:
            raise CustomException(e, sys)

    def scroll_to_load_reviews(self):
        """
        Scrolls the webpage to load more reviews dynamically by incrementally scrolling.
        """
        try:
            # Set the browser window size
            self.driver.set_window_size(1920, 1080)

            # Get the initial page height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            # Continue scrolling until no new content is loaded
            while True:
                # Scroll down by 1000 pixels
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(3)  # Pause to allow new content to load

                # Get the new page height
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                # Break the loop if no new content is loaded
                if new_height == last_height:
                    break

                last_height = new_height  # Update last height for the next iteration

        except Exception as e:
            raise CustomException(e, sys)

    def extract_products(self, product_reviews: list):
        """
        Extract detailed reviews, user ratings, and comments from the reviews section.

        Args:
        - product_reviews (list): List of review sections from the product page.

        Returns:
        - review_data (pd.DataFrame): A DataFrame containing extracted review details.
        """
        try:
            # Construct the review page link
            t2 = product_reviews["href"]
            review_link = "https://www.myntra.com" + t2
            self.driver.get(review_link)  # Open the review page

            # Scroll to load all reviews
            self.scroll_to_load_reviews()

            # Parse the review page HTML
            review_page = self.driver.page_source
            review_html = bs(review_page, "html.parser")

            # Extract user reviews
            reviews_section = review_html.find_all("div", {"class": "user-review-main user-review-showRating"})
            user_comments = review_html.find_all("div", {"class": "user-review-reviewTextWrapper"})
            user_names = review_html.find_all("div", {"class": "user-review-left"})

            reviews = []  # List to store extracted review details

            # Loop through reviews and extract details
            for i in range(len(reviews_section)):
                try:
                    rating = reviews_section[i].find("span", class_="user-review-starRating").get_text().strip()
                except:
                    rating = "No rating given"

                try:
                    comment = user_comments[i].text.strip()
                except:
                    comment = "No comment given"

                try:
                    name = user_names[i].find("span").text.strip()
                except:
                    name = "No name given"

                try:
                    date = user_names[i].find_all("span")[1].text.strip()
                except:
                    date = "No date given"

                # Create a dictionary for the review
                review_dict = {
                    "Product Name": self.product_title,
                    "Overall Rating": self.product_rating_value,
                    "Price": self.product_price,
                    "Date": date,
                    "Rating": rating,
                    "Name": name,
                    "Comment": comment,
                }

                reviews.append(review_dict)  # Add to reviews list

            # Create a DataFrame from the reviews list
            review_data = pd.DataFrame(
                reviews,
                columns=["Product Name", "Overall Rating", "Price", "Date", "Rating", "Name", "Comment"]
            )

            return review_data

        except Exception as e:
            raise CustomException(e, sys)
        

    def skip_products(self , search_string, no_of_products, skip_index):
        product_urls: list = self.scrape_product_urls(search_string, no_of_products)
        product_urls.pop(skip_index)

    def get_review_data(self) -> pd.DataFrame:
        try:
            # Scrape product URLs
            product_urls = self.scrape_product_urls(product_name=self.product_name)

            if not product_urls:
                raise CustomException("No product URLs found. Please refine your search.", sys)

            product_details = []
            review_len = 0

            # Ensure review_len doesn't exceed the number of available products
            while review_len < self.no_of_products and review_len < len(product_urls):
                product_url = product_urls[review_len]
                review = self.extract_reviews(product_url)

                if review:
                    product_detail = self.extract_products(review)
                    product_details.append(product_detail)
                    review_len += 1
                else:
                    # Remove the product URL if reviews are unavailable
                    product_urls.pop(review_len)

            if not product_details:
                raise CustomException("No review data could be extracted.", sys)

            # Quit the driver
            self.driver.quit()

            # Combine all product details into a single DataFrame
            data = pd.concat(product_details, axis=0)

            # Save data to CSV
            data.to_csv("data.csv", index=False)

            return data

        except Exception as e:
            # Ensure the driver quits in case of an error
            self.driver.quit()
            raise CustomException(e, sys)
