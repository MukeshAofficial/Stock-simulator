from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import plotly.graph_objects as go

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

# List of 10 stocks to display
stocks_list = [
    'AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT', 
    'NFLX', 'META', 'NVDA', 'SPY', 'BA',
    'IBM', 'INTC', 'WMT', 'DIS', 'NVDA', 
    'V', 'PYPL', 'PFE', 'BABA', 'AMD', 'NVDA'  # Added NVDA here
]
# Route for the home page
@app.route('/visual')
def home():
    return render_template('index.html', stocks=stocks_list)

# Route to display the live stock chart
@app.route('/stock', methods=['POST'])
def stock_search():
    ticker = request.form['ticker']
    return redirect(url_for('stock', ticker=ticker.upper()))

@app.route('/stock/<ticker>')
def stock(ticker):
    try:
        # Fetch live stock data
        stock_data = yf.Ticker(ticker)
        df = stock_data.history(period="1d", interval="1m")  # 1-day data with 1-minute intervals

        # Create a live stock chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        ))

        # Chart customization
        fig.update_layout(
            title=f"Live Stock Chart for {ticker.upper()}",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )

        # Render the chart as HTML
        chart_html = fig.to_html(full_html=False)

        return render_template('stock.html', ticker=ticker.upper(), chart_html=chart_html)

    except Exception as e:
        return f"Error fetching data for {ticker}: {e}"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
