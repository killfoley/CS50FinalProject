from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///hardware.db")

@app.route("/")
@login_required
def index():
    return redirect("/inventory")

# --- Authentication ---
# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or password != confirmation:
            return "Invalid input", 400

        hash_pw = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return "Username already exists", 400

        return redirect("/login")
    else:
        return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return "Invalid username or password", 403

        session["user_id"] = rows[0]["id"]
        return redirect("/inventory")

    return render_template("login.html")

# Logout page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Inventory page
@app.route("/inventory")
@login_required
def inventory():
    products = db.execute("SELECT * FROM products ORDER BY name")
    return render_template("inventory.html", products=products)

# Add entries
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = session.get("user_id")
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if not rows:
        session.clear()
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        quantity = request.form.get("quantity")
        price = request.form.get("price")

        if not name or not quantity or not price:
            return "Missing fields", 400

        try:
            quantity = int(quantity)
            price = float(price)
        except:
            return "Invalid quantity or price", 400

        # Insert the new product
        db.execute(
            "INSERT INTO products (name, category, quantity, price, added_by, status) VALUES (?, ?, ?, ?, ?, ?)",
            name, category, quantity, price, user_id, "active"
        )

        # Get the product ID of the most recently added product for this user
        product = db.execute(
            "SELECT id FROM products WHERE added_by = ? ORDER BY id DESC LIMIT 1",
            user_id
        )

        # Log transaction
        if product:
            db.execute(
                "INSERT INTO transactions (product_id, change, action, user_id) VALUES (?, ?, ?, ?)",
                product[0]["id"], quantity, "add", user_id
            )

        return redirect("/inventory")

    return render_template("add.html")

# Edit entries
@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit(product_id):
    product = db.execute("SELECT * FROM products WHERE id = ?", product_id)[0]

    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        quantity = int(request.form.get("quantity"))
        price = float(request.form.get("price"))

        db.execute("""
            UPDATE products SET name = ?, category = ?, quantity = ?, price = ?
            WHERE id = ?
        """, name, category, quantity, price, product_id)

        # Log transaction
        db.execute("""
            INSERT INTO transactions (product_id, change, action, user_id)
            VALUES (?, ?, ?, ?)
        """, product_id, quantity - product["quantity"], "edit", session["user_id"])

        return redirect("/inventory")

    return render_template("edit.html", product=product)

# Delete entries
@app.route("/delete/<int:product_id>", methods=["POST"])
@login_required
def delete(product_id):
    product_rows = db.execute("SELECT * FROM products WHERE id = ?", product_id)

    if not product_rows:
        return "Product not found", 404

    product = product_rows[0]

    # Mark the product as discontinued instead of deleting
    db.execute("UPDATE products SET status = 'discontinued' WHERE id = ?", product_id)

    # Log the action in transaction history
    db.execute("""
        INSERT INTO transactions (product_id, change, action, user_id)
        VALUES (?, ?, ?, ?)
    """, product_id, -product["quantity"], "discontinue", session["user_id"])

    return redirect("/inventory")

# restore discontinued products
@app.route("/restore/<int:product_id>", methods=["POST"])
@login_required
def restore(product_id):
    db.execute("UPDATE products SET status = 'active' WHERE id = ?", product_id)

    db.execute("""
        INSERT INTO transactions (product_id, change, action, user_id)
        VALUES (?, ?, ?, ?)
    """, product_id, 0, "restore", session["user_id"])

    return redirect("/inventory")

# History
@app.route("/history")
@login_required
def history():
    rows = db.execute("""
        SELECT t.timestamp, p.name, t.change, t.action, u.username
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        JOIN users u ON t.user_id = u.id
        ORDER BY t.timestamp DESC
    """)
    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
