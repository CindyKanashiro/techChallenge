worker: python scraping/books.py
web: uvicorn api.main:app --host=0.0.0.0 --port=$PORT
web: streamlit run run_dashboard.py --port=$PORT_STREAMLIT