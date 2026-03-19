from datetime import date
import requests
from db import SessionLocal
from models import Product, ProductPrice

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

CATEGORY_IDS = [
    112, 115, 116, 117, 156, 163, 158, 159, 161, 162, 135, 133, 132, 118, 121, 120, 89, 95, 92, 97, 90, 216, 219, 
    218, 217, 164, 166, 181, 174, 168, 170, 173, 171, 169, 86, 81, 83, 84, 88, 46, 38, 47, 37, 42, 43, 44, 40, 45,
    78, 80, 79, 48, 52, 49, 51, 50, 58, 54, 56, 53, 147, 148, 154, 155, 150, 149, 151, 884, 152, 145, 122, 123, 127,
    130, 129, 126, 201, 199, 203, 202, 192, 189, 185, 191, 188, 187, 186, 190, 194, 196, 198, 213, 214, 27, 28, 29,
    77, 72, 75, 226, 237, 241, 234, 235, 233, 231, 230, 232, 229, 243, 238, 239, 244, 206, 207, 208, 210, 212, 32,
    34, 31, 36, 222, 221, 225, 65, 66, 69, 59, 60, 62, 64, 68, 71, 897, 138, 140, 142, 105, 110, 111, 106, 103, 109,
    108, 104, 107, 99, 100, 143, 98
]

def fetch_category(category_id: str, wh:str = "mad2", lang:str = "es") -> dict:
    url = f"https://tienda.mercadona.es/api/categories/{category_id}/?lang={lang}&wh={wh}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_products_from_category(data:dict) -> list[dict]:
    products = []

    for subcategory in data.get("categories", []):
        for product in subcategory.get("products", []):
            products.append(product)
    
    return products

def save_category_products(category_id : str):
    data = fetch_category(category_id)
    products = extract_products_from_category(data)

    db = SessionLocal()

    try: 
        today = date.today()
        
        for item in products:

            price_info = item.get("price_instructions", {})

            product = db.query(Product).filter(Product.id==item["id"]).first()

            if not product:
                product = Product(
                    id=item["id"],
                    display_name=item["display_name"],
                    brand=item.get("brand"),
                    packaging=item.get("packaging"),
                    unit_size=price_info.get("unit_size"),
                    size_format=price_info.get("size_format"),
                    share_url=item.get("share_url"),
                    thumbnail=item.get("thumbnail"),
                    slug=item.get("slug")
                )
                db.add(product)
            else:
                product.display_name = item.get("display_name")
                product.packaging = item.get("packaging")
                product.unit_size = price_info.get("unit_size")
                product.size_format = price_info.get("size_format")
                product.share_url = item.get("share_url")
                product.thumbnail = item.get("thumbnail")
                product.slug = item.get("slug")

            existing_price = (
                db.query(ProductPrice)
                .filter(
                    ProductPrice.product_id == item["id"],
                    ProductPrice.price_date == today
                )
                .first()
            )

            if not existing_price:
                price_row = ProductPrice(
                    product_id=item["id"],
                    price_date=today,
                    unit_price=float(price_info["unit_price"]),
                    reference_price=float(price_info["reference_price"]) if price_info.get("reference_price") else None,
                    reference_format=price_info.get("reference_format"),
                    bulk_price=float(price_info["bulk_price"]) if price_info.get("bulk_price") else None,
                )
                db.add(price_row)

        db.commit()
        print(f"Guardados {len(products)} productos de la categoría {category_id}")

    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise

    finally:
        db.close()

import time

def save_selected_categories():
    for cat_id in CATEGORY_IDS:
        print(f"Procesando categoría {cat_id}")
        try:
            save_category_products(cat_id)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error en categoría {cat_id}: {e}")