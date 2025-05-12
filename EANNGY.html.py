from flask import Flask, render_template_string, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

real_free_cryptos = [
    {"pair": "LTC/USDT", "name": "Litecoin", "price": "$75.50", "direction": "BUY", "targets": ["$77.00", "$79.00"], "stop_loss": "$74.00", "leverage": 20, "entry_zone": ["$75.00", "$75.80"]},
    {"pair": "XLM/USDT", "name": "Stellar", "price": "$0.11", "direction": "BUY", "targets": ["$0.12", "$0.13"], "stop_loss": "$0.105", "leverage": 20, "entry_zone": ["$0.108", "$0.112"]},
    {"pair": "DASH/USDT", "name": "Dash", "price": "$45.20", "direction": "SELL", "targets": ["$44.00", "$43.00"], "stop_loss": "$46.50", "leverage": 20, "entry_zone": ["$45.30", "$44.90"]},
    {"pair": "ZEC/USDT", "name": "Zcash", "price": "$30.80", "direction": "BUY", "targets": ["$31.50", "$32.50"], "stop_loss": "$30.00", "leverage": 20, "entry_zone": ["$30.50", "$31.00"]},
    {"pair": "ETC/USDT", "name": "Ethereum Classic", "price": "$22.10", "direction": "BUY", "targets": ["$22.50", "$23.00"], "stop_loss": "$21.80", "leverage": 20, "entry_zone": ["$22.00", "$22.20"]},
]

real_platinum_cryptos = [
    {"pair": "LINK/USDT", "name": "Chainlink", "price": "$14.30", "direction": "BUY", "targets": ["$14.70", "$15.20"], "stop_loss": "$13.90", "leverage": 20, "entry_zone": ["$14.20", "$14.40"]},
    {"pair": "UNI/USDT", "name": "Uniswap", "price": "$7.80", "direction": "SELL", "targets": ["$7.60", "$7.40"], "stop_loss": "$8.00", "leverage": 20, "entry_zone": ["$7.85", "$7.75"]},
    {"pair": "AVAX/USDT", "name": "Avalanche", "price": "$35.60", "direction": "BUY", "targets": ["$36.50", "$37.50"], "stop_loss": "$34.80", "leverage": 20, "entry_zone": ["$35.50", "$35.70"]},
    {"pair": "DOT/USDT", "name": "Polkadot", "price": "$8.20", "direction": "BUY", "targets": ["$8.40", "$8.60"], "stop_loss": "$8.00", "leverage": 20, "entry_zone": ["$8.15", "$8.25"]},
    {"pair": "ATOM/USDT", "name": "Cosmos", "price": "$9.50", "direction": "SELL", "targets": ["$9.30", "$9.10"], "stop_loss": "$9.70", "leverage": 20, "entry_zone": ["$9.55", "$9.45"]},
]

signals = [
    {"pair": "BTC/USDT", "name": "Bitcoin", "price": "$53,245.78", "direction": "BUY", "targets": ["$54,200", "$55,500"], "stop_loss": "$52,100", "leverage": 20, "entry_zone": ["$53,100", "$53,350"]},
    {"pair": "SOL/USDT", "name": "Solana", "price": "$138.25", "direction": "BUY", "targets": ["$142.50", "$148.00"], "stop_loss": "$134.80", "leverage": 20, "entry_zone": ["$138.00", "$138.50"]},
    {"pair": "ETH/USDT", "name": "Ethereum", "price": "$2,845.92", "direction": "SELL", "targets": ["$2,780", "$2,700"], "stop_loss": "$2,900", "leverage": 20, "entry_zone": ["$2,850", "$2,840"]},
    {"pair": "BNB/USDT", "name": "Binance Coin", "price": "$572.15", "direction": "BUY", "targets": ["$580.00", "$595.00"], "stop_loss": "$560.00", "leverage": 20, "entry_zone": ["$571.50", "$572.50"]},
    {"pair": "ADA/USDT", "name": "Cardano", "price": "$0.42", "direction": "BUY", "targets": ["$0.45", "$0.48"], "stop_loss": "$0.40", "leverage": 20, "entry_zone": ["$0.418", "$0.422"]},
    {"pair": "XRP/USDT", "name": "Ripple", "price": "$0.58", "direction": "SELL", "targets": ["$0.55", "$0.52"], "stop_loss": "$0.60", "leverage": 20, "entry_zone": ["$0.582", "$0.578"]},
    {"pair": "DOGE/USDT", "name": "Dogecoin", "price": "$0.18", "direction": "BUY", "targets": ["$0.20", "$0.22"], "stop_loss": "$0.16", "leverage": 20, "entry_zone": ["$0.179", "$0.181"]},
    {"pair": "DOT/USDT", "name": "Polkadot", "price": "$8.20", "direction": "BUY", "targets": ["$8.40", "$8.60"], "stop_loss": "$8.00", "leverage": 20, "entry_zone": ["$8.18", "$8.22"]},
    {"pair": "AVAX/USDT", "name": "Avalanche", "price": "$35.60", "direction": "SELL", "targets": ["$34.80", "$34.00"], "stop_loss": "$36.20", "leverage": 20, "entry_zone": ["$35.65", "$35.55"]},
    {"pair": "MATIC/USDT", "name": "Polygon", "price": "$0.92", "direction": "BUY", "targets": ["$0.95", "$1.00"], "stop_loss": "$0.88", "leverage": 20, "entry_zone": ["$0.918", "$0.922"]},
]

futures_users = []
features = []

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EANNGY - Real-Time Cryptocurrency Trading Signals</title>
    <style>
        :root {
            --primary-color: #5741d9;
            --secondary-color: #1de9b6;
            --bg-color: #0d1117;
            --text-color: #e6edf3;
            --card-bg: #161b22;
        }
        body { background-color: var(--bg-color); color: var(--text-color); font-family: sans-serif; margin: 0; padding: 0; }
        header { background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); color: white; padding: 1rem; text-align: center; }
        .container { max-width: 800px; margin: 1rem auto; padding: 1rem; }
        .signals-section { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .signal-card { background-color: var(--card-bg); border-radius: 8px; padding: 0.8rem; }
        .coin-info { margin-bottom: 0.5rem; }
        .signal-price { font-size: 1.2rem; font-weight: bold; color: var(--secondary-color); }
        .signal-leverage { font-size: 0.9rem; color: #ffd700; }
        .signal-direction { font-weight: bold; }
        .buy { color: #00e676; }
        .sell { color: #ff5252; }
        .signal-targets { margin-top: 0.3rem; font-size: 0.9rem; }
        .positive { color: #00e676; }
        .negative { color: #ff5252; }
        .action-buttons { margin-top: 0.5rem; }
        button { background-color: var(--primary-color); color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 5px; cursor: pointer; font-size: 0.8rem; }
        .platinum-btn { background-color: #b0b0b0; color: black; }
        .futures-btn { background-color: #ff4500; color: white; }
        .wallet-section, .subscription-section, .futures-section, .features-display { background-color: var(--card-bg); padding: 1rem; border-radius: 8px; margin-top: 1rem; }
    </style>
</head>
<body>
    <header>
        <h1>EANNGY</h1>
        <p>Real-Time Crypto Signals</p>
    </header>
    <div class="container">
        <div class="subscription-section">
            <h2>Subscription</h2>
            {% if session.get('platinum') %}
                <p>Platinum active!</p>
            {% else %}
                <p>Get Platinum for more signals!</p>
                <form method="POST" action="/subscribe">
                    <button type="submit" class="platinum-btn">Get Platinum</button>
                </form>
            {% endif %}
            <p><a href="/futures"><button class="futures-btn">Futures Trading</button></a></p>
        </div>
        <div class="signals-section">
            <h2>Free Signals</h2>
            {% for signal in signals %}
            <div class="signal-card">
                <div class="coin-info">
                    <h3>{{ signal.pair }}</h3>
                    <p>{{ signal.name }}</p>
                </div>
                <p class="signal-price">{{ signal.price }}</p>
                <p>Entry Zone: <span>{{ signal.entry_zone[0] }} - {{ signal.entry_zone[1] }}</span></p>
                <p class="signal-leverage">Leverage: {{ signal.leverage }}x</p>
                <p class="signal-direction {{ 'buy' if signal.direction == 'BUY' else 'sell' }}">{{ signal.direction }}</p>
                <div class="signal-targets">
                    <p>Target 1: <span class="{{ 'positive' if signal.direction == 'BUY' else 'negative' }}">{{ signal.targets[0] }}</span></p>
                    <p>Target 2: <span class="{{ 'positive' if signal.direction == 'BUY' else 'negative' }}">{{ signal.targets[1] }}</span></p>
                    <p>Stop Loss: <span class="{{ 'negative' if signal.direction == 'BUY' else 'positive' }}">{{ signal.stop_loss }}</span></p>
                </div>
            </div>
            {% endfor %}
            <h2>Additional Free Cryptocurrencies</h2>
            {% for crypto in real_free_cryptos %}
            <div class="signal-card">
                <div class="coin-info">
                    <h3>{{ crypto.pair }}</h3>
                    <p>{{ crypto.name }}</p>
                </div>
                <p class="signal-price">{{ crypto.price }}</p>
                <p>Entry Zone: <span>{{ crypto.entry_zone[0] }} - {{ crypto.entry_zone[1] }}</span></p>
                <p class="signal-leverage">Leverage: {{ crypto.leverage }}x</p>
                <p class="signal-direction {{ 'buy' if crypto.direction == 'BUY' else 'sell' }}">{{ crypto.direction }}</p>
                <div class="signal-targets">
                    <p>Target 1: <span class="{{ 'positive' if crypto.direction == 'BUY' else 'negative' }}">{{ crypto.targets[0] }}</span></p>
                    <p>Target 2: <span class="{{ 'positive' if crypto.direction == 'BUY' else 'negative' }}">{{ crypto.targets[1] }}</span></p>
                    <p>Stop Loss: <span class="{{ 'negative' if crypto.direction == 'BUY' else 'positive' }}">{{ crypto.stop_loss }}</span></p>
                </div>
            </div>
            {% endfor %}
            {% if session.get('platinum') %}
            <h2>Platinum Crypto</h2>
            {% for crypto in real_platinum_cryptos %}
            <div class="signal-card">
                <div class="coin-info">
                    <h3>{{ crypto.pair }}</h3>
                    <p>{{ crypto.name }}</p>
                </div>
                <p class="signal-price">{{ crypto.price }}</p>
                <p>Entry Zone: <span>{{ crypto.entry_zone[0] }} - {{ crypto.entry_zone[1] }}</span></p>
                <p class="signal-leverage">Leverage: {{ crypto.leverage }}x</p>
                <p class="signal-direction {{ 'buy' if crypto.direction == 'BUY' else 'sell' }}">{{ crypto.direction }}</p>
                <div class="signal-targets">
                    <p>Target 1: <span class="{{ 'positive' if crypto.direction == 'BUY' else 'negative' }}">{{ crypto.targets[0] }}</span></p>
                    <p>Target 2: <span class="{{ 'positive' if crypto.direction == 'BUY' else 'negative' }}">{{ crypto.targets[1] }}</span></p>
                    <p>Stop Loss: <span class="{{ 'negative' if crypto.direction == 'BUY' else 'positive' }}">{{ crypto.stop_loss }}</span></p>
                </div>
            </div>
            {% endfor %}
            {% endif %}
        </div>
        {% if features %}
        <div class="features-display">
            <h2>EANNGY Features</h2>
            {% for feature in features %}
            <p>{{ feature.timestamp }} UTC</p>
            <p><span style="background-color: #00e676; color: white; padding: 0.2rem 0.5rem; border-radius: 3px;">{{ feature.direction }}</span> {{ feature.leverage }}x {{ feature.pair }}</p>
            <p style="color: #00e676;">+{{ feature.profit }}%</p>
            <p>Entry: {{ feature.entry_price }}</p>
            <p>Last: {{ feature.last_price }}</p>
            <hr>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            setInterval(function() {
                const prices = document.querySelectorAll('.signal-price');
                prices.forEach(price => {
                    const currentPrice = parseFloat(price.textContent.replace('$', '').replace(',', ''));
                    const change = (Math.random() - 0.5) * 5
                    const newPrice = (currentPrice + change).toFixed(2);
                    price.textContent = '$' + newPrice;
                    if (change > 0) {
                        price.classList.remove('negative');
                        price.classList.add('positive');
                    } else {
                        price.classList.remove('positive');
                        price.classList.add('negative');
                    }
                });
            }, 3000);
        });
    </script>
</body>
</html>
"""

futures_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EANNGY Futures</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 0; background-color: #0d1117; color: #e6edf3; }
        header { background-color: #5741d9; color: white; padding: 1rem; text-align: center; }
        .container { max-width: 600px; margin: 1rem auto; padding: 1rem; background-color: #161b22; border-radius: 8px; }
        h2 { color: #1de9b6; }
        label { display: block; margin-top: 0.5rem; }
        input[type="text"], input[type="number"], select, input[type="file"] { width: 100%; padding: 0.5rem; margin-top: 0.2rem; border: 1px solid #30363d; border-radius: 4px; background-color: #0d1117; color: #e6edf3; }
        button { background-color: #1de9b6; color: #0d1117; border: none; padding: 0.6rem 1rem; border-radius: 5px; cursor: pointer; margin-top: 1rem; }
        a button { background-color: #5741d9; color: white; }
        .futures-signal { background-color: #30363d; padding: 0.8rem; border-radius: 4px; margin-top: 0.5rem; }
    </style>
</head>
<body>
    <header>
        <h1>EANNGY Futures</h1>
    </header>
    <div class="container">
        {% if not session.get('futures_registered') %}
        <h2>Futures Registration</h2>
        <form method="POST" action="/futures">
            <label for="full_name">Full Name:</label>
            <input type="text" id="full_name" name="full_name" required>
            <label for="age">Age:</label>
            <input type="number" id="age" name="age" min="18" required>
            <label for="business_type">Business Type:</label>
            <select id="business_type" name="business_type" required>
                <option value="Individual">Individual</option>
                <option value="Trading Firm">Trading Firm</option>
                <option value="Investment Fund">Investment Fund</option>
            </select>
            <button type="submit">Register</button>
        </form>
        {% else %}
        <h2>Futures Trading</h2>
        <p>Welcome to futures trading!</p>
        {% for signal in signals %}
        <div class="futures-signal">
            <h3>{{ signal.pair }}</h3>
            <p>Price: {{ signal.price }}</p>
            <p>Entry Zone: <span>{{ signal.entry_zone[0] }} - {{ signal.entry_zone[1] }}</span></p>
            <p>Leverage: {{ signal.leverage }}x</p>
            <p>Direction: {{ signal.direction }}</p>
        </div>
        {% endfor %}
        {% endif %}
        <div style="text-align: center; margin-top: 1rem;">
            <a href="/"><button>Back to Signals</button></a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, signals=signals, real_free_cryptos=real_free_cryptos, real_platinum_cryptos=real_platinum_cryptos, features=features)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    session['platinum'] = True
    return redirect(url_for('home'))

@app.route('/futures', methods=['GET', 'POST'])
def futures():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        business_type = request.form.get('business_type')
        if full_name and age and business_type:
            futures_users.append({
                'full_name': full_name,
                'age': age,
                'business_type': business_type,
            })
            session['futures_registered'] = True
            return redirect(url_for('futures'))
    return render_template_string(futures_template, signals=signals)

@app.route('/create_feature', methods=['POST'])
def create_feature():
    pair = request.form.get('pair')
    name = request.form.get('name')
    price = request.form.get('price')
    direction = request.form.get('direction')

    try:
        entry_price = float(price.replace('$', '').replace(',', ''))
        last_price = entry_price * (1 + random.uniform(-0.1, 0.2))
        profit = ((last_price - entry_price) / entry_price * 100) if direction == 'BUY' else ((entry_price - last_price) / entry_price * 100)

        features.append({
            'pair': pair,
            'name': name,
            'direction': direction,
            'leverage': 15,
            'profit': f"{abs(profit):.2f}",
            'entry_price': f"{entry_price:.6f}",
            'last_price': f"{last_price:.6f}",
            'timestamp': datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        })
    except (ValueError, TypeError) as e:
        print(f"Error creating feature: {e}")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)