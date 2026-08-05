import base64
import json
import os
import sqlite3
from typing import Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from reviews_api import get_product_rating

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

vision_llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)
@tool #tells langchain,this function can be used by the Ai
def search_products(
    query: str,
    max_price: Optional[float] = None,
    is_organic: Optional[bool] = None,
) -> str:
    """
    Search the product database by keyword (matched against name, description, and category).
    Optionally filter by maximum price and/or organic status.
    Returns a JSON array of matching products.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sql = "SELECT id, name, category, price, description, is_organic FROM products WHERE 1=1"
    params: list = []

    if query:
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like, like])

    if max_price is not None:
        sql += " AND price <= ?"
        params.append(max_price)

    if is_organic is not None:
        sql += " AND is_organic = ?"
        params.append(1 if is_organic else 0)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": row[3],
            "description": row[4],
            "is_organic": bool(row[5]),
        }
        for row in rows
    ]

    return json.dumps(products)
@tool
def get_rating(product_id: int) -> str:
    """
    Get the average customer rating and total review count for a product by its ID.
    Returns a JSON object with: product_id, average_rating, review_count.
    """
    result = get_product_rating(product_id)
    return json.dumps(result)
@tool
def checkout(product_id: int) -> str:
    """
    Place an order for the given product ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, price FROM products WHERE id = ?",
        (product_id,),
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return f"Error: product with ID {product_id} not found."

    name, price = row

    cursor.execute(
        "INSERT INTO orders (product_id, product_name, price) VALUES (?, ?, ?)",
        (product_id, name, price),
    )

    order_id = cursor.lastrowid

    conn.commit() #coz INSERT,UPDATE and DELETE are not permanently saved until committed.
    conn.close()

    return (
        f"Order Successfully Placed\n\n"
        f"Order ID : {order_id}\n\n"
        f"Product  : {name}\n\n"
        f"Price    : ${price:.2f}\n\n"
        f"Status   : Confirmed\n\n"
        f"Thank you for shopping with us."
    )
@tool
def describe_product_image(image_path: str) -> str:
    """
    Analyze a product image and return its key attributes as a JSON object.
    """
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
#rb means Read Binary, Images are binary files, not text files
# The LLM cannot directly understand image bytes so we convert them into Base64
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"

    message = HumanMessage(content=[
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime};base64,{image_data}"
            },
        },
        {
            "type": "text",
            "text": (
                "Look at this product image and extract its key attributes. "
                "Return ONLY a JSON object with these fields:\n"
                "- product_type\n"
                "- search_query\n"
                "- is_organic\n"
                "- description"
            ),
        },
    ])

    response = vision_llm.invoke([message])
    return response.content
agent = create_agent(
    tools=[
        search_products,
        get_rating,
        checkout,
        describe_product_image,
    ],
    model=llm,
    system_prompt=(
        "You are a helpful shopping assistant..."
    ),
)
if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I want to buy organic honey with 4.5+ rating and less than $20 price."
                }
            ]
        }
    )

    print(result["messages"][-1].content)