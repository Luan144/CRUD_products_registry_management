# ADICIONAR: ao registrar uma compra checar se o produto está cadastrado e emitir uma msg

#
# uvicorn app:app --port 8091 --reload

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from datetime import date

from functions.functions import minimize, check_duplicate_product

app = FastAPI()

# Product information structure
class ProductBody(BaseModel):
    name: str
    label: str
    quantity: float
    full_name: Optional[str] = ""

# Purchase information structure
class ProductPurchase(BaseModel):
    full_name: str
    price: float
    bought: int
    date: date

# Custom exceptions
class DuplicateProduct(Exception):
    '''Raised when trying to register an already registered product in products list.'''

class EmptyRegistry(Exception):
    '''Raised when trying to get an empty registry.'''

class ProductNotFound(Exception):
    '''Raised when trying to get a non-existing product.'''


products: List[ProductBody] = []
history: List[ProductPurchase] = []

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

@app.get("/get-products-list")
    '''Get the entire product registry.'''
def get_products():
    try:
        check_empty_registry(products)
    except EmptyRegister:
        raise HTTPException(status_code=400, detail="SYSTEM ERROR: Products list is empty.")
    else:
        return {"products" : products}

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
    '''Use the product.full_name (primary key) to remove a product from the product registry.'''

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