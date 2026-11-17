from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    buy_score = None
    recommendation = None
    explanation = None
    result_class = None
    error = None

    product = None
    price = None
    income = None

    affordability_score = None
    need_score = None
    want_score = None
    existing_score = None

    

    if request.method == "POST":
        product = request.form["product"]
        price = float(request.form["price"])
        income = float(request.form["income"])
        need = int(request.form["need"])
        existing = request.form["existing"]
        want = int(request.form["want"])

        affordability = price / income

        price = float(request.form["price"])
        income = float(request.form["income"])

        if price <= 0 or income <= 0:
            error = "Price and income muct be greater than zero."
            return render_template("index.html", error = error)

        if affordability <= 0.10:
            affordability_score = 30
        elif affordability <= 0.20:
            affordability_score = 24
        elif affordability <= 0.30:
            affordability_score = 18
        elif affordability <= 0.50:
            affordability_score = 10
        else:
            affordability_score = 0

        need_score = need * 6
        want_score = want * 4

        if existing == "no":
            existing_score = 20
        else:
            existing_score = 0

        buy_score = (
            affordability_score
            + need_score
            + want_score
            + existing_score
        )

        if affordability_score == 0:
           explanation = "The product costs more than 50% of your monthly income. It may put pressure on your budget."
        
        
        elif existing_score == 0 and need_score <= 18:
           explanation = "You already own something similar, and your need for another one is relatively low."
        else:

            

         reasons = []

         if affordability_score >= 24:
            reasons.append("the product is affordable")
         elif affordability_score <= 10:
            reasons.append("the product is expensive compared to your income")

         if need_score >= 24:
            reasons.append("you need it")
         elif need_score <= 12:
            reasons.append("you don't really need it")

         if want_score >= 16:
            reasons.append("you really want it")

         if existing_score == 0:
            reasons.append("you already own something similar")

         if reasons:
            explanation = "This result is based on " + ", ".join(reasons) + "."
         else:
            explanation = "Your answers give a mixed result."

    return render_template(
        "index.html",
        buy_score=buy_score,
        recommendation=recommendation,
        explanation=explanation,
        result_class=result_class,
        error=error,
        product=product,
        price=price,
        income=income,
        affordability_score= affordability_score,
        need_score= need_score,
        want_score = want_score,
        existing_score= existing_score
    )


if __name__ == "__main__":
    app.run(debug=True)