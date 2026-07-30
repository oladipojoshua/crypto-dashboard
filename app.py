from flask import Flask, render_template, request, jsonify
from api.coingecko import get_market_data, search_coin, get_coin_details, get_coin_chart, get_global_data

app = Flask(__name__)


@app.route("/")
def home():

    coins = get_market_data()
    global_data = get_global_data()

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

    query = request.args.get("query")

    result = search_coin(query)

    return render_template(
        "coin.html",
        result=result,
        query=query
    )

@app.route("/coin/<coin_id>")
def coin(coin_id):

    coin = get_coin_details(coin_id)

    if not coin:
        return "Coin not found", 404

    return render_template(
        "coin_details.html",
        coin=coin
    )

@app.route("/api/chart/<coin_id>/<int:days>")
def chart_api(coin_id, days):

    chart = get_coin_chart(coin_id, days)

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

