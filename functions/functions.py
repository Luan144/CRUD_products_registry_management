def minimize(product_string: str):
    return product_string.lower()

def check_duplicate_product(product_full_name:str):
    '''Check if product.full_name (primary key) is already in products list.'''

    product = list(filter(lambda x: x.full_name == product_full_name, products))

    if len(product) != 0:
        raise DuplicateProduct

def check_empty_registry(registry_name: list):
    '''Check if product.full_name (primary key) is already in products list.'''

    if len(registry_name) == 0:
        raise EmptyRegistry

def delete_product(product_full_name: str, product_registry: list):
    '''Delete a product from the product registry using product.full_name (primary key).'''
    for idx, prod in enumerate(product_registry):
        if prod.full_name == product_full_name:
            del product_registry[idx]
            break
        else:
            raise ProductNotFound