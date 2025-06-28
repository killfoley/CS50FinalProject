# Hardware Store Inventory Manager
#### Video Demo: https://www.youtube.com/watch?v=g-Qgqm1bz-k  
#### GitHub Repository: https://github.com/killfoley/CS50FinalProject

#### Description:

This project is a web-based inventory management system built using **Flask**, **SQLite**, **HTML/CSS**, and **Bootstrap**. It allows a small hardware store to track products, log inventory changes, and manage stock statuses using a simple browser interface.

It was developed in the **CS50 IDE** and manually exported to GitHub, as Git integration is disabled in the CS50 environment.

---

## Features

- User Authentication (register, login, logout)  
- Add, Edit, and Restore Products  
- Discontinue Instead of Delete – realistic for actual hardware retail  
- Transaction History – every inventory change is logged and viewable  
- Product Status Tracking (`active` / `discontinued`)  
- Clean, responsive UI using Bootstrap 5  
- Session-based access control via flask_session

---

## How It Works

Upon logging in, users can:

- View Inventory: Shows all products with name, category, quantity, price, and status.
- Add Products: Adds a new product and automatically logs an "add" transaction.
- Edit Products: Modifies name, category, quantity, or price — logs an "edit" transaction.
- Discontinue Products: Marks a product as `discontinued` instead of deleting it.
- Restore Products: Reactivates discontinued products, logs a "restore" transaction.
- View History: The `/history` page displays all inventory activity, including timestamps, actions, and usernames.

---

## File Overview

- `app.py`: Main Flask app handling routes, database logic, and user flow.
- `helpers.py`: Contains `@login_required` decorator for protected views.
- `schema.sql`: SQL schema defining `users`, `products`, and `transactions` tables.
- `seed.sql`: (Optional) Adds starter products and an admin user for testing.
- `hardware.db`: SQLite database used during development.
- `requirements.txt`: List of required Python packages (generated via `pip freeze`).
- `templates/`: Jinja2 templates for all pages:
  - `layout.html`: Shared base template with nav
  - `login.html`, `register.html`: Auth pages
  - `inventory.html`: Product list with edit/discontinue/restore actions
  - `add.html`, `edit.html`: Product forms
  - `history.html`: Transaction log

---

## Design Choices

### Discontinuing Instead of Deleting

In early development, products were deleted outright. But this created problems:
- Foreign key constraints (e.g., with transactions)
- Real-world impracticality (shops rarely truly delete SKUs)

Instead, each product now has a `status` field, either 'active' or 'discontinued'. This preserves history and keeps the app realistic.

---

### Transaction Logging

Every action — add, edit, restore — generates a transaction row. This is vital for accountability and traceability. Logged details include:
- Timestamp
- Action (add, edit, restore)
- Product ID and quantity change
- User ID (joined with username for display)

The `/history` page shows these logs in reverse chronological order.

---

### Session Handling

Flask's `session` is used to track logged-in users, and routes are protected with a `@login_required` decorator. Sessions are stored server-side using `flask_session`, and `session.clear()` is used on logout or reset to maintain state integrity.

---

## Manual GitHub Upload

Since the CS50 IDE disables `git`, the project was manually zipped and uploaded to GitHub. This also explains the presence of `hardware.db` in the repository.

---

## Installation & Setup

1. Clone the repo:
   ```
   git clone https://github.com/killfoley/CS50FinalProject.git
   cd CS50FinalProject
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   sqlite3 hardware.db < schema.sql
   sqlite3 hardware.db < seed.sql  # Optional
   ```

4. Run the app:
   ```
   flask run
   ```

Then open your browser and go to http://127.0.0.1:5000

---

## Final Notes

This app is tailored for a small business like a hardware store, but the underlying logic is easily extendable to other retail contexts. Potential improvements:

- Checkout system with Stripe
- Logged-in user indicators
- Role-based permissions (admin vs. staff)
- CSV import/export
- Stock-level alerts or dashboards

---

### Conclusion

This project delivers a complete, working CRUD web app with thoughtful design decisions, secure user management, and a realistic business context. It fulfills CS50’s expectations and demonstrates strong full-stack fundamentals.
