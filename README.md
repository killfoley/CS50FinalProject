# Hardware Store Inventory Manager
#### Video Demo: https://www.youtube.com/watch?v=g-Qgqm1bz-k
#### Description:

This project is a web-based inventory management system built using **Flask**, **SQLite**, **HTML/CSS**, and **Bootstrap**. It allows a small hardware store to track products, log updates, and manage inventory status using a simple browser interface.

It was developed in the **CS50 IDE** and manually exported to GitHub, as Git integration is disabled in the CS50 environment.

---

## Features

**User Authentication** (register, login, logout)
**Add, Edit, and Restore Products**
**Discontinue Instead of Delete** – realistic for actual hardware retail
**Transaction History** – every inventory change is logged and viewable
**Product Status Tracking** (`active` / `discontinued`)
Clean and responsive UI using **Bootstrap 5**
Session-based access control with `flask_session`

---

## How It Works

Upon logging in, users can:

- **View Inventory**: Shows all products with name, category, quantity, price, and status.
- **Add Products**: Adds a new product with automatic `"add"` transaction logging.
- **Edit Products**: Changes quantity, name, category, or price — logs a `"edit"` transaction.
- **Discontinue Products**: Marks products as `discontinued` instead of deleting, preserving history.
- **Restore Products**: Reactivates discontinued items.
- **View Transaction History**: Shows a complete log of all inventory changes, including user and timestamp.

All interactions update the database and create a clear audit trail for accountability.

---

## File Overview

- `app.py`: The main Flask application handling all routes, authentication, inventory logic, and database interactions.
- `helpers.py`: Contains the `@login_required` decorator to protect routes and ensure users are authenticated.
- `schema.sql`: Defines the SQLite schema including `users`, `products`, and `transactions` tables.
- `seed.sql`: (Optional) Used to insert initial data, including a default `admin` user and starter products.
- `hardware.db`: The live SQLite database used during development and demo.
- `requirements.txt`: Generated using `pip freeze`, lists all required Python packages.
- `templates/`: Folder containing all Jinja2 HTML templates:
  - `layout.html`: Shared base layout
  - `login.html`, `register.html`: Authentication pages
  - `inventory.html`: Displays all products with options to edit, discontinue, or restore
  - `add.html`, `edit.html`: Forms for adding/editing product entries
  - `history.html`: Shows the full transaction log

---

## Design Choices

### Discontinuing Instead of Deleting

Originally, products were deleted from the database. However, this posed issues with referential integrity and realistic business practices. In the real world, items are usually out of stock, archived, or marked inactive — they’re rarely deleted permanently. This led to the decision to **use a `status` field** (`active`, `discontinued`) instead of deletion.

### Transaction Logging

Rather than silently updating values, each change logs a transaction in a separate table. This provides a full **audit trail**, which is essential for accountability in a retail environment.

Each transaction includes:
- `timestamp`
- `product_id`
- `change` in quantity
- `action` (`add`, `edit`, `delete`, `restore`)
- `user_id`

This table is joined with `products` and `users` to show human-readable logs in the `/history` view.

### Session Handling

To avoid stale sessions (e.g., after a database reset), the app includes checks on every route to validate the session’s `user_id`. If the session is invalid, the user is logged out automatically. This ensures smooth operation, especially during local development or demos.

---

## Manual GitHub Upload

Because this project was built entirely inside the **CS50 IDE**, and Git is disabled in that environment, the project was exported manually and uploaded to GitHub. Any README references to commits or version control are purely local to the exported folder.

---

## Final Notes

This project was scoped for a small-scale retail business like a hardware store, but the core structure is extendable. Additional improvements could include:

- Checkout system using Stripe's hosted checkout
- Information on logged in user
- Role-based permissions (e.g., manager vs. staff), including super user edit user permissions
- CSV import/export for stock data

Overall, this submission demonstrates a complete web app with CRUD functionality, secure user management, and thoughtful real-world tradeoffs.
