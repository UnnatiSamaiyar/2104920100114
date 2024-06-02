from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Define the API endpoint for fetching top products
@app.route('/categories/<category>/products')
def get_top_products(category):
    # Get query parameters
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'rating')  # Default sorting by rating
    sort_order = request.args.get('sort_order', 'desc')  # Default descending order

    # Fetch products from e-commerce APIs
    products = fetch_products(category, n, page, sort_by, sort_order)

    return jsonify(products)

# Define the API endpoint for fetching details of a specific product
@app.route('/products/<product_id>')
def get_product_details(product_id):
    # Fetch product details from e-commerce APIs
    product_details = fetch_product_details(product_id)

    return jsonify(product_details)

# Function to fetch products from e-commerce APIs
def fetch_products(category, n, page, sort_by, sort_order):
    # Assuming the URL structure for fetching products from each company's API is known
    company_apis = {
        "AMZ": "https://amz-api.com/products",
        "FLP": "https://flp-api.com/products",
        "SNP": "https://snp-api.com/products",
        "MYN": "https://myn-api.com/products",
        "AZO": "https://azo-api.com/products"
    }

    all_products = []

    for company, api_url in company_apis.items():
        # Fetch products from each company's API
        response = requests.get(api_url, params={"category": category, "n": n, "page": page, "sort_by": sort_by, "sort_order": sort_order})

        if response.status_code == 200:
            products = response.json()
            all_products.extend(products)

    # Sort all products based on the specified criteria
    all_products.sort(key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))

    # Perform pagination
    start_index = (page - 1) * n
    end_index = start_index + n
    paginated_products = all_products[start_index:end_index]

    return paginated_products

# Function to fetch details of a specific product
def fetch_product_details(product_id):
    # Assuming the URL structure for fetching product details from each company's API is known
    # You need to implement this based on the actual API structure provided by each e-commerce company
    pass

if __name__ == '__main__':
    app.run(debug=True)
