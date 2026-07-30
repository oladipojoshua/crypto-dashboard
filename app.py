from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from api.coingecko import get_market_data, search_coin, get_coin_details, get_coin_chart, get_global_data

app = Flask(__name__)

cache = Cache(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300  # 5 minutes
})

@app.route("/")
def home():

    coins = cache.get("market_data")

    if coins is None:
        coins = get_market_data()
        cache.set("market_data", coins)

    global_data = cache.get("global_data")

    if global_data is None:
        global_data = get_global_data() or {}
        cache.set("global_data", global_data)

    return render_template(
        "index.html",
        coins=coins,
        global_data=global_data
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search")
def search():

    query = request.args.get("query", "").strip()

    cache_key = f"search_{query.lower()}"

    result = cache.get(cache_key)

    if result is None:
        result = search_coin(query)
        cache.set(cache_key, result)

    return render_template(
        "coin.html",
        result=result,
        query=query
    )

@app.route("/coin/<coin_id>")
def coin(coin_id):

    coin = cache.get(f"coin_{coin_id}")

    if coin is None:
        coin = get_coin_details(coin_id)

        if coin is not None:
            cache.set(f"coin_{coin_id}", coin)

        if not coin:
            return "Coin not found", 404

    return render_template(
        "coin_details.html",    
        coin=coin
    )

@app.route("/api/chart/<coin_id>/<int:days>")
def chart_api(coin_id, days):

    cache_key = f"chart_{coin_id}_{days}"

    chart = cache.get(cache_key)

    if chart is None:
        chart = get_coin_chart(coin_id, days)

        if chart is not None:
            cache.set(cache_key, chart)

    if not chart:
        return jsonify([])

    from datetime import datetime

    prices = [point[1] for point in chart["prices"]]

    labels = [
        datetime.fromtimestamp(point[0] / 1000).strftime("%b %d")
        for point in chart["prices"]
    ]

    return jsonify({
        "labels": labels,
        "prices": prices
    })

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

