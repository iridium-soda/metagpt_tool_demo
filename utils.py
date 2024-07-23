import math
import csv
from metagpt.tools.tool_registry import register_tool

@register_tool()
def query_fields():
    """
    Reads the headers from a CSV file named 'example.csv'.

    This function opens the 'example.csv' file, reads the first row to extract
    the headers, and returns them as a list.

    Returns:
        list: A list of headers (field names) from the CSV file.
    """
    with open('example.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the first row as headers
    return headers


@register_tool()
def query_data(query_date, query_product):
    """
    Queries a single record with the specified date and product from a CSV file.

    Args:
        query_date (str): The date to query.
        query_product (str): The product to query.

    Returns:
        dict: The queried record as a dictionary, or None if not found.
    """
    filename = "company_operational_data_by_product.csv"
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['date'] == query_date and row['Product'] == query_product:
                return row
    return None
