from data.products import products

def search_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None