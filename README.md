# FastAPI MongoDB REST API

A simple REST API built with FastAPI that connects to a MongoDB instance.

## Prerequisites

- Python 3.8+
- pip
- Access to a MongoDB instance

## Setup

1. Clone the repository:
bash
git clone <repository-url>
cd <repository-name>

2. Create a virtual environment and activate it:

bash
```
python -m venv venv
```
On Windows
```
venv\Scripts\activate
```
On Unix or MacOS
```
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Create a .env file in the root directory with your MongoDB credentials:
```
MONGO_USER=your_username
MONGO_PASS=your_password
MONGO_ADDR=your.mongodb.server.com:27017 
```

5. Run the application:
```
uvicorn app:app --reload
```
