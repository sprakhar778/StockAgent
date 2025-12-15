# StockAgent Backend

This backend provides a FastAPI server for real-time stock analysis using LLM agents and financial data APIs.

## Features
- **Real-time Stock Price**: Get the latest price for any ticker symbol.
- **Historical Stock Data**: Retrieve historical prices for a given date range.
- **Balance Sheet Data**: Access company balance sheets.
- **Stock News**: Fetch recent news for a ticker.
- **LLM Agent**: Uses LangChain and OpenAI/Groq models to process and respond to user queries.

## Project Structure
- `main.py`: FastAPI app with endpoints and agent logic.
- `pyproject.toml`: Python dependencies and project metadata.
- `test.ipynb`: Example notebook for experimenting with LangChain, yfinance, and plotting.

## API Usage
### POST `/api/chat`
Send a JSON body with a prompt and thread info. The agent will stream a response using the tools above.

**Request Example:**
```json
{
  "prompt": {
    "content": "Get the latest price for AAPL",
    "id": "1",
    "role": "user"
  },
  "threadId": "thread-1",
  "responseId": "resp-1"
}
```

**Response:**
- Streams tokens as text/event-stream.

## Core Dependencies
- fastapi
- uvicorn
- langchain, langchain-openai, langchain-groq
- yfinance
- pydantic
- python-dotenv

Install all dependencies with:
```bash
pip install -r requirements.txt
```
Or use the `[project.dependencies]` in `pyproject.toml`.

## Example Tools in Agent
- `get_stock_price(ticker)`
- `get_historical_stock_price(ticker, start_date, end_date)`
- `get_balance_sheet(ticker)`
- `get_stock_news(ticker)`

## Development
- Run the server:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8888
  ```
- Test endpoints with curl, Postman, or the provided notebook.

## Notebooks
- `test.ipynb` demonstrates LangChain agent, yfinance data fetching, and matplotlib plotting for stock analysis.

## Environment
- Requires Python 3.12+
- Set up your `.env` file for any required API keys.

---
For more details, see code comments in `main.py` and the notebook for usage examples.
