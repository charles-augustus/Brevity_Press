import yfinance as yf

def fetch_stock_data():
    stocks = ['TCS.NS', 'RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'BRITANNIA.NS', 'COALINDIA.NS', 'BHARTIARTL.NS']

    stock_data = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        data = ticker.history(period="2d")  # Fetch last two days of data

        if not data.empty and len(data['Close']) > 1:
            price = data['Close'][-1]
            previous_close = data['Close'][-2]
            change = price - previous_close
        elif not data.empty: 
            price = data['Close'][-1]
            previous_close = price  
            change = 0
        else:
            price = "N/A"
            change = 0
        
        stock_data.append({
            'ticker': stock,
            'price': f'{price:.2f}' if isinstance(price, (int, float)) else price,
            'change': change
        })
    
    return stock_data
