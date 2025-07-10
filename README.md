# Artificial Business Intelligence (ABI)

This project is a modular, intelligent data pipeline that allows users to upload CSV files containing business data. The pipeline performs data cleaning, stores the cleaned data in a SQL database, and allows users to query the data using natural language.

## Features

- CSV file upload through a FastAPI backend
- Data cleaning with the help of LangChain and predefined business rules
- Asynchronous data processing for scalability and responsiveness
- Cleaned data is validated and stored in Microsoft SQL Server
- Answering agent powered by LangChain to handle natural language questions and return data-driven answers
- Easily extensible for future dashboard visualizations and LLM-based summaries

## Tech Stack

- Python
- FastAPI
- LangChain
- Pandas
- Pydantic
- SQLAlchemy
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server
- asyncio

## How it Works

- Users upload CSV files via a FastAPI endpoint.
- The file is parsed and optionally stored.
- Data is cleaned using Pandas and LangChain-assisted logic.
- Cleaned data is validated and inserted into the SQL Server database.
- A LangChain-powered answering agent takes natural language questions and converts them into SQL queries to fetch answers.

## Future Enhancements

- Dashboard generation using Streamlit or React + Plotly
- Automated trend summaries using LLMs
- Support for Excel and JSON uploads
