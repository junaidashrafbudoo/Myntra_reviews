import pandas as pd  # Import pandas for data manipulation and analysis
import streamlit as st  # Import Streamlit for creating the web application
from src.cloud_io import MongoIO  # Import custom MongoDB interaction class
from src.constants import SESSION_PRODUCT_KEY  # Import constant for session key
from src.utils import fetch_product_names_from_cloud  # Utility to fetch product names from cloud
from src.data_report.generate_data_report import DashboardGenerator  # Class to generate dashboard for data analysis

# Initialize the MongoDB connection
mongo_con = MongoIO()

def create_analysis_page(review_data: pd.DataFrame):
    """
    Creates an analysis page for the given review data.

    Args:
        review_data (pd.DataFrame): A DataFrame containing the review data to be analyzed.

    Returns:
        None
    """
    if review_data is not None and not review_data.empty:
        # Display the review data in the app as a DataFrame
        st.dataframe(review_data)
        
        # Button to trigger the generation of the analysis dashboard
        if st.button("Generate Analysis"):
            # Initialize the dashboard generator with review data
            dashboard = DashboardGenerator(review_data)
            
            # Display general information about the reviews
            dashboard.display_general_info()
            
            # Display product-specific sections (e.g., ratings, comments)
            dashboard.display_product_sections()
    else:
        st.error("No review data found. Please check your data source.")

try:
    # Check if data is available in the session state
    if st.session_state.get('data', False):
        # Check if product_name exists in session state
        product_name = st.session_state.get(SESSION_PRODUCT_KEY, None)
        
        if product_name:
            # Fetch reviews for the specified product from MongoDB
            data = mongo_con.get_reviews(product_name=product_name)
            
            if data is not None and not data.empty:
                # Create the analysis page with the fetched data
                create_analysis_page(data)
            else:
                st.error("No review data found for the selected product.")
        else:
            st.error("Product name not found in session state.")
    else:
        # If no data is available, display a message in the sidebar
        with st.sidebar:
            st.markdown("""
            No Data Available for analysis. Please go to the search page to initiate data scraping and analysis.
            """)
except AttributeError:
    # Handle AttributeError when session state or data is not properly initialized
    product_name = None
    st.markdown(""" # No Data Available for analysis.""")
