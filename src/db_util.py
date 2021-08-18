import streamlit as st
from gsheetsdb import connect


class GoogleSheet:
    def __init__(self):    
        # Create a connection object.
        self.conn = connect()
    
    # Perform SQL query on the Google Sheet.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    @st.cache(ttl=600)
    def run_query(self, query):
        rows = self.conn.execute(query, headers=1)
        return rows
