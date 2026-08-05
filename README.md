# AI Shopping Assistant

AI Shopping Assistant is a shopping chatbot built using LangChain, Groq, Streamlit, and SQLite. It allows users to search products, compare ratings, and place orders using natural language instead of manually browsing a product catalog.

This project was built to understand how AI agents can interact with external tools and databases to solve real-world shopping tasks.

---

## Features

- Search products using natural language
- Filter products based on price and category
- View customer ratings and review statistics
- Get AI-powered product recommendations
- Place orders through the chatbot
- Store and retrieve product information using SQLite
- Interactive web interface built with Streamlit

---

## Tech Stack

- Python
- LangChain
- Groq LLM
- Streamlit
- SQLite
- Python-dotenv

---

## Project Structure

```
ai-shopping-assistant/
│
├── app.py
├── shopping_agent.py
├── reviews_api.py
├── store.db
├── pyproject.toml
├── README.md
├── .gitignore
├── requirements.txt
└── images/
```

---

## How the Project Works

1. The user enters a shopping-related query.
2. The LangChain agent understands the user's request.
3. The agent automatically selects the appropriate tool.
4. Product information is retrieved from the SQLite database.
5. Product ratings are fetched from the reviews table.
6. The AI recommends suitable products based on the user's requirements.
7. If requested, the assistant places the order and returns a confirmation.

---

## Sample Queries

- Show organic honey under $20
- Recommend products with rating above 4.5
- Show healthy nuts below $15
- Buy Organic Almonds
- Order product id 13

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-shopping-assistant.git
```

Move into the project directory:

```bash
cd ai-shopping-assistant
```

Install the required dependencies:

```bash
pip install -e .
```

Run the application:

```bash
streamlit run app.py
```

---

## Screenshots

### Home Page

(Add screenshot here)

### Product Search

(Add screenshot here)

### Checkout

(Add screenshot here)

---

## Future Improvements

- Product image search
- User authentication
- Order history
- Personalized recommendations
- Voice-based shopping assistant
- Expanded product catalog with more categories

---

## About

This project demonstrates how a Large Language Model can interact with external tools and databases to solve real-world shopping tasks. It combines LangChain tool calling, Groq LLM, SQLite, and Streamlit to provide an AI-powered shopping experience.

---

## Author

**Prakarsh Rathore**

B.Tech Computer Science Engineering

Interested in Artificial Intelligence, Data Analytics and Generative AI.