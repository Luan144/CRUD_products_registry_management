# ADICIONAR: ao registrar uma compra checar se o produto está cadastrado e emitir uma msg

#
# uvicorn app:app --port 8091 --reload

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from datetime import date

from functions.functions import minimize

app = FastAPI()

# Product information structure
class ProductBody(BaseModel):
    name: str
    label: str
    quantity: float
    full_name: Optional[str] = ""

# Product history structure
class ProductPurchase(BaseModel):
    full_name: str
    price: float
    bought: int
    date: date


products: List[ProductBody] = []
history: List[ProductPurchase] = []

class DuplicateProduct(Exception):
    '''Raised when trying to register an already registered product in products list.'''

class EmptyRegister(Exception):
    '''Raised when trying to get an empty registry.'''

class ProductNotFound(Exception):
    '''Raised when trying to get a non-existing product.'''

def check_duplicate_product(product_full_name:str):
    '''Check if product.full_name (primary key) is already in products list.'''

    product = list(filter(lambda x: x.full_name == product_full_name, products))

    if len(product) != 0:
        raise DuplicateProduct

def check_empty_registry(registry_name: list):
    '''Check if product.full_name (primary key) is already in products list.'''

    if len(registry_name) == 0:
        raise EmptyRegister

def delete_product(product_full_name: str, product_registry: list):
    for idx, prod in enumerate(product_registry):
        if prod.full_name == product_full_name:
            del product_registry[idx]
            break
        else:
            raise ProductNotFound


# Create a new product using ProductBody structure
@app.post("/register-product", status_code=201)
def create_product(product: ProductBody):
    '''Register a product in the products list using the ProductBody structure'''

    product.name = minimize(product.name)
    product.label = minimize(product.label)
    # Primary key
    product.full_name = product.name + " " + product.label

    try:
        check_duplicate_product(product_full_name=product.full_name)
    except DuplicateProduct:
        raise HTTPException(status_code=400, detail="SYSTEM ERROR: Product already registered.")
    else:
        products.append(product)
        return "SYSTEM: Product created!"


@app.post("/register-purchase", status_code=201)
def create_purchase(product_purchase: ProductPurchase):
    '''Register a product purchase in the history using the ProductPurchase structure'''

    product_purchase.full_name = minimize(product_purchase.full_name)

    history.append(product_purchase)

    return "SYSTEM: Purchase registered!"

# Recieve a dict with all the existing products
@app.get("/get-products-list")
def get_products():
    try:
        check_empty_registry(products)
    except EmptyRegister:
        raise HTTPException(status_code=400, detail="SYSTEM ERROR: Products list is empty.")
    else:
        return {"products" : products}

# Retrieve specific product history using the primary key full_name
@app.get("/{product_full_name}")
def retrieve_specific_product_purchase_history(product_full_name:str):
    '''Retrieve an specific product's purchase history using its full name (primary key).'''

    product_purchase_history = list(filter(lambda x: x.full_name == product_full_name, history))

    try:
        check_empty_registry(product_purchase_history)
    except EmptyRegister:
        raise HTTPException(status_code=400, detail="SYSTEM ERROR: Product not found.")
    else:
        return {"product_purchase_history": product_purchase_history}

@app.delete("/{product_full_name}", status_code=201)
def delete_registered_product(product_full_name:str):
    '''Use a product full name (primary key to remove a product from products list'''

    try:
        check_empty_registry(products)
    except EmptyRegister:
        raise HTTPException(status_code=400, detail="SYSTEM ERROR: Product not found.")
    else:
        try:
            delete_product(product_full_name=product_full_name, product_registry=products)
        except ProductNotFound:
            raise HTTPException(status_code=400, detail="SYSTEM ERROR: Product not found.")
        else:
            return "SYSTEM: product successfully removed."