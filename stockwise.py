import streamlit as st
from datetime import datetime, timedelta
from copy import deepcopy
import math

# ============================================================
# STOCKWISE - HTML-FREE STREAMLIT VERSION
# No pandas, numpy, altair, or custom HTML required.
# ============================================================

st.set_page_config(
    page_title="StockWise",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Demo store data
# ------------------------------------------------------------

DEMO_STORES = {
    "demo@stockwise.com": {
        "password": "demo123",
        "store_id": "greenmart",
        "store_name": "GreenMart",
        "owner": "Ananya Rao",
        "email": "demo@stockwise.com",
        "phone": "+91 98765 43210",
        "location": "Hyderabad, Telangana",
        "products": [
            {"id": 1, "name": "Rice 5kg", "category": "Groceries", "price": 420.0, "stock": 18, "reorder": 8, "daily_demand": 2.4},
            {"id": 2, "name": "Wheat Flour 5kg", "category": "Groceries", "price": 310.0, "stock": 7, "reorder": 10, "daily_demand": 1.5},
            {"id": 3, "name": "Cooking Oil 1L", "category": "Groceries", "price": 145.0, "stock": 24, "reorder": 10, "daily_demand": 3.1},
            {"id": 4, "name": "Milk 1L", "category": "Dairy", "price": 68.0, "stock": 12, "reorder": 15, "daily_demand": 5.2},
            {"id": 5, "name": "Bread", "category": "Bakery", "price": 45.0, "stock": 5, "reorder": 8, "daily_demand": 2.1},
            {"id": 6, "name": "Biscuits", "category": "Snacks", "price": 30.0, "stock": 35, "reorder": 12, "daily_demand": 4.0},
            {"id": 7, "name": "Tea 250g", "category": "Beverages", "price": 160.0, "stock": 9, "reorder": 8, "daily_demand": 1.3},
            {"id": 8, "name": "Coffee 200g", "category": "Beverages", "price": 225.0, "stock": 14, "reorder": 7, "daily_demand": 1.1},
        ],
        "sales": [
            {"id": 1, "product": "Rice 5kg", "qty": 2, "amount": 840.0, "date": "Today, 10:20 AM"},
            {"id": 2, "product": "Milk 1L", "qty": 4, "amount": 272.0, "date": "Today, 11:45 AM"},
            {"id": 3, "product": "Biscuits", "qty": 5, "amount": 150.0, "date": "Today, 12:30 PM"},
            {"id": 4, "product": "Cooking Oil 1L", "qty": 2, "amount": 290.0, "date": "Today, 1:15 PM"},
            {"id": 5, "product": "Bread", "qty": 3, "amount": 135.0, "date": "Today, 2:05 PM"},
        ],
    },
    "cafe@stockwise.com": {
        "password": "cafe123",
        "store_id": "beanbrew",
        "store_name": "Bean & Brew",
        "owner": "Riya Sharma",
        "email": "cafe@stockwise.com",
        "phone": "+91 91234 56789",
        "location": "Hyderabad, Telangana",
        "products": [
            {"id": 1, "name": "Arabica Coffee", "category": "Coffee", "price": 280.0, "stock": 16, "reorder": 8, "daily_demand": 2.7},
            {"id": 2, "name": "Cold Brew", "category": "Beverages", "price": 190.0, "stock": 6, "reorder": 10, "daily_demand": 2.2},
            {"id": 3, "name": "Chocolate Cake", "category": "Bakery", "price": 320.0, "stock": 4, "reorder": 6, "daily_demand": 1.4},
            {"id": 4, "name": "Croissant", "category": "Bakery", "price": 110.0, "stock": 12, "reorder": 8, "daily_demand": 2.5},
            {"id": 5, "name": "Green Tea", "category": "Tea", "price": 150.0, "stock": 20, "reorder": 7, "daily_demand": 1.6},
            {"id": 6, "name": "Muffin", "category": "Bakery", "price": 95.0, "stock": 7, "reorder": 8, "daily_demand": 1.9},
        ],
        "sales": [
            {"id": 1, "product": "Arabica Coffee", "qty": 3, "amount": 840.0, "date": "Today, 9:40 AM"},
            {"id": 2, "product": "Cold Brew", "qty": 2, "amount": 380.0, "date": "Today, 10:15 AM"},
            {"id": 3, "product": "Croissant", "qty": 4, "amount": 440.0, "date": "Today, 11:05 AM"},
        ],
    },
    "store@stockwise.com": {
        "password": "store123",
        "store_id": "freshbasket",
        "store_name": "FreshBasket",
        "owner": "Arjun Mehta",
        "email": "store@stockwise.com",
        "phone": "+91 99887 66554",
        "location": "Hyderabad, Telangana",
        "products": [
            {"id": 1, "name": "Apples 1kg", "category": "Fruits", "price": 180.0, "stock": 22, "reorder": 10, "daily_demand": 3.4},
            {"id": 2, "name": "Bananas 1 Dozen", "category": "Fruits", "price": 70.0, "stock": 9, "reorder": 12, "daily_demand": 4.1},
            {"id": 3, "name": "Tomatoes 1kg", "category": "Vegetables", "price": 55.0, "stock": 15, "reorder": 10, "daily_demand": 3.0},
            {"id": 4, "name": "Potatoes 1kg", "category": "Vegetables", "price": 42.0, "stock": 30, "reorder": 12, "daily_demand": 3.5},
            {"id": 5, "name": "Eggs 12 pack", "category": "Dairy", "price": 90.0, "stock": 6, "reorder": 10, "daily_demand": 2.8},
        ],
        "sales": [
            {"id": 1, "product": "Apples 1kg", "qty": 2, "amount": 360.0, "date": "Today, 9:25 AM"},
            {"id": 2, "product": "Bananas 1 Dozen", "qty": 3, "amount": 210.0, "date": "Today, 10:10 AM"},
            {"id": 3, "product": "Tomatoes 1kg", "qty": 2, "amount": 110.0, "date": "Today, 11:20 AM"},
        ],
    },
}

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "store_data" not in st.session_state:
    st.session_state.store_data = None

if "message" not in st.session_state:
    st.session_state.message = ""

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def money(value):
    return f"₹{value:,.0f}"


def get_store():
    return st.session_state.store_data


def save_store(store):
    st.session_state.store_data = store


def inventory_value(store):
    return sum(p["stock"] * p["price"] for p in store["products"])


def low_stock_products(store):
    return [p for p in store["products"] if p["stock"] <= p["reorder"]]


def critical_products(store):
    return [p for p in store["products"] if p["stock"] <= max(1, p["reorder"] * 0.5)]


def total_revenue(store):
    return sum(s["amount"] for s in store["sales"])


def forecast_for_product(product):
    daily = max(0.1, float(product["daily_demand"]))
    forecast_7 = daily * 7
    coverage = product["stock"] / daily
    target = math.ceil(daily * 14)
    reorder_qty = max(0, target - product["stock"])
    return forecast_7, coverage, reorder_qty


def status_for_product(product):
    if product["stock"] <= max(1, product["reorder"] * 0.5):
        return "Critical"
    if product["stock"] <= product["reorder"]:
        return "Low"
    return "Healthy"


def status_icon(status):
    if status == "Critical":
        return "🔴"
    if status == "Low":
        return "🟠"
    return "🟢"


def set_page(page):
    st.session_state.page = page


def show_message():
    if st.session_state.message:
        st.success(st.session_state.message)
        st.session_state.message = ""


# ------------------------------------------------------------
# Login
# ------------------------------------------------------------

def login_page():
    st.title("📦 StockWise")
    st.subheader("Smart inventory management for modern retailers")
    st.write("Track stock, record sales, predict demand, and know what to reorder before you run out.")

    st.divider()

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.header("🔐 Store Login")

        email = st.text_input("Email", placeholder="owner@yourstore.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login to StockWise", type="primary", use_container_width=True):
            account = DEMO_STORES.get(email.strip().lower())

            if account and account["password"] == password:
                st.session_state.logged_in = True
                st.session_state.email = email.strip().lower()
                st.session_state.store_data = deepcopy(account)
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Incorrect email or password.")

        st.divider()

        st.caption("Demo accounts")
        st.write("**GreenMart:** demo@stockwise.com / demo123")
        st.write("**Bean & Brew:** cafe@stockwise.com / cafe123")
        st.write("**FreshBasket:** store@stockwise.com / store123")


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

def sidebar():
    store = get_store()

    with st.sidebar:
        st.title("📦 StockWise")
        st.caption("Smart inventory intelligence")

        st.divider()

        st.write("**Store**")
        st.write(f"🏪 {store['store_name']}")
        st.caption(store["owner"])

        st.divider()

        pages = [
            ("🏠", "Dashboard"),
            ("📦", "Inventory"),
            ("💰", "Sales"),
            ("🤖", "AI Forecast"),
            ("🔔", "Alerts"),
            ("👤", "Profile"),
        ]

        for icon, page in pages:
            if st.button(
                f"{icon}  {page}",
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if st.session_state.page == page else "secondary",
            ):
                set_page(page)
                st.rerun()

        st.divider()

        critical = len(critical_products(store))
        low = len(low_stock_products(store))

        st.metric("Critical stock", critical)
        st.metric("Needs attention", low)

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.email = ""
            st.session_state.store_data = None
            st.session_state.page = "Dashboard"
            st.rerun()


# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------

def dashboard():
    store = get_store()

    st.title(f"Good day, {store['owner'].split()[0]} 👋")
    st.write(f"Here's what is happening at **{store['store_name']}** today.")
    show_message()

    revenue = total_revenue(store)
    inv_value = inventory_value(store)
    low = low_stock_products(store)
    critical = critical_products(store)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Today's revenue", money(revenue), "+12.4%")

    with c2:
        st.metric("Inventory value", money(inv_value))

    with c3:
        st.metric("Products", len(store["products"]))

    with c4:
        st.metric("Low stock", len(low), f"{len(critical)} critical")

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("📦 Inventory health")

        if not store["products"]:
            st.info("No products in inventory yet.")
        else:
            for product in store["products"]:
                status = status_for_product(product)
                percentage = min(100, int((product["stock"] / max(product["reorder"] * 2, 1)) * 100))

                a, b, c, d = st.columns([2.3, 1, 1, 1])

                with a:
                    st.write(f"**{product['name']}**")
                    st.caption(product["category"])

                with b:
                    st.write(f"{product['stock']} units")

                with c:
                    st.write(f"{status_icon(status)} {status}")

                with d:
                    st.progress(percentage / 100)

    with right:
        st.subheader("🤖 AI recommendations")

        recommendations = []

        for product in store["products"]:
            forecast, coverage, reorder = forecast_for_product(product)

            if product["stock"] <= product["reorder"]:
                recommendations.append(
                    f"**{product['name']}** needs attention. "
                    f"Suggested reorder: **{reorder} units**."
                )
            elif coverage < 7:
                recommendations.append(
                    f"**{product['name']}** may run low within a week."
                )

        if not recommendations:
            st.success("Inventory looks healthy. No urgent recommendations.")
        else:
            for item in recommendations[:5]:
                st.info(item)

        st.divider()

        st.subheader("⚡ Quick actions")

        q1, q2 = st.columns(2)

        with q1:
            if st.button("➕ Add product", use_container_width=True):
                set_page("Inventory")
                st.rerun()

        with q2:
            if st.button("💰 Record sale", use_container_width=True):
                set_page("Sales")
                st.rerun()

    st.divider()

    st.subheader("🧾 Recent sales")

    if not store["sales"]:
        st.info("No sales recorded yet.")
    else:
        for sale in store["sales"][:6]:
            a, b, c, d = st.columns([2.5, 1, 1, 1.5])

            with a:
                st.write(f"**{sale['product']}**")

            with b:
                st.write(f"{sale['qty']} units")

            with c:
                st.write(sale["date"])

            with d:
                st.write(f"**{money(sale['amount'])}**")


# ------------------------------------------------------------
# Inventory
# ------------------------------------------------------------

def inventory_page():
    store = get_store()

    st.title("📦 Inventory")
    st.write("Manage every product in your store.")

    show_message()

    top1, top2 = st.columns([3, 1])

    with top1:
        search = st.text_input("Search products", placeholder="Search by product or category...")

    with top2:
        status_filter = st.selectbox(
            "Status",
            ["All", "Healthy", "Low", "Critical"],
        )

    filtered = []

    for product in store["products"]:
        matches_search = (
            not search
            or search.lower() in product["name"].lower()
            or search.lower() in product["category"].lower()
        )

        matches_status = (
            status_filter == "All"
            or status_for_product(product) == status_filter
        )

        if matches_search and matches_status:
            filtered.append(product)

    st.write(f"Showing **{len(filtered)}** product(s)")
    st.divider()

    if filtered:
        for product in filtered:
            status = status_for_product(product)
            forecast, coverage, reorder = forecast_for_product(product)

            with st.container(border=True):
                a, b, c, d, e = st.columns([2.2, 1.2, 1.2, 1.4, 1.2])

                with a:
                    st.write(f"**{product['name']}**")
                    st.caption(product["category"])

                with b:
                    st.write("Price")
                    st.write(money(product["price"]))

                with c:
                    st.write("Stock")
                    st.write(f"**{product['stock']}** units")

                with d:
                    st.write("Status")
                    st.write(f"{status_icon(status)} {status}")

                with e:
                    st.write("Coverage")
                    st.write(f"{coverage:.1f} days")

                st.caption(
                    f"AI 7-day demand forecast: {forecast:.0f} units  •  "
                    f"Suggested reorder: {reorder} units"
                )
    else:
        st.info("No products match your search.")

    st.divider()

    st.subheader("➕ Add a product")

    with st.form("add_product_form"):
        a, b = st.columns(2)

        with a:
            name = st.text_input("Product name")
            category = st.text_input("Category")
            price = st.number_input("Selling price", min_value=0.0, step=1.0)

        with b:
            stock = st.number_input("Current stock", min_value=0, step=1)
            reorder = st.number_input("Reorder level", min_value=1, step=1)
            demand = st.number_input(
                "Estimated daily demand",
                min_value=0.1,
                value=1.0,
                step=0.1,
            )

        submitted = st.form_submit_button("Add product", type="primary")

        if submitted:
            if not name.strip():
                st.error("Please enter a product name.")
            else:
                new_id = max([p["id"] for p in store["products"]], default=0) + 1

                store["products"].append({
                    "id": new_id,
                    "name": name.strip(),
                    "category": category.strip() or "General",
                    "price": float(price),
                    "stock": int(stock),
                    "reorder": int(reorder),
                    "daily_demand": float(demand),
                })

                save_store(store)
                st.session_state.message = f"{name.strip()} was added to inventory."
                st.rerun()


# ------------------------------------------------------------
# Sales
# ------------------------------------------------------------

def sales_page():
    store = get_store()

    st.title("💰 Sales")
    st.write("Record a sale and StockWise automatically updates inventory.")

    show_message()

    st.subheader("Record a new sale")

    product_names = [p["name"] for p in store["products"]]

    if not product_names:
        st.warning("Add a product before recording a sale.")
        return

    with st.form("sale_form"):
        product_name = st.selectbox("Product", product_names)

        selected = next(
            p for p in store["products"]
            if p["name"] == product_name
        )

        st.write(
            f"Available stock: **{selected['stock']} units**  •  "
            f"Price: **{money(selected['price'])}**"
        )

        quantity = st.number_input(
            "Quantity sold",
            min_value=1,
            max_value=max(1, selected["stock"]),
            value=1,
            step=1,
        )

        submitted = st.form_submit_button(
            "Record sale",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if quantity > selected["stock"]:
                st.error("Not enough stock available.")
            else:
                selected["stock"] -= int(quantity)

                amount = selected["price"] * int(quantity)

                store["sales"].insert(0, {
                    "id": max([s["id"] for s in store["sales"]], default=0) + 1,
                    "product": selected["name"],
                    "qty": int(quantity),
                    "amount": amount,
                    "date": datetime.now().strftime("Today, %I:%M %p"),
                })

                save_store(store)
                st.session_state.message = (
                    f"Sale recorded: {quantity} × {selected['name']} = {money(amount)}"
                )
                st.rerun()

    st.divider()

    st.subheader("Recent transactions")

    if not store["sales"]:
        st.info("No transactions yet.")
    else:
        for sale in store["sales"]:
            with st.container(border=True):
                a, b, c, d = st.columns([2.5, 1, 1.5, 1.5])

                with a:
                    st.write(f"**{sale['product']}**")

                with b:
                    st.write(f"{sale['qty']} units")

                with c:
                    st.write(sale["date"])

                with d:
                    st.write(f"**{money(sale['amount'])}**")


# ------------------------------------------------------------
# AI Forecast
# ------------------------------------------------------------

def forecast_page():
    store = get_store()

    st.title("🤖 AI Demand Forecast")
    st.write(
        "StockWise estimates upcoming demand using product-level sales "
        "patterns and current inventory."
    )

    st.info(
        "Prototype note: this demo uses demand estimates stored for each "
        "product. A production version can replace this with a trained "
        "machine-learning model using historical sales."
    )

    st.divider()

    products = store["products"]

    if not products:
        st.info("Add products to generate forecasts.")
        return

    for product in products:
        forecast, coverage, reorder = forecast_for_product(product)

        with st.container(border=True):
            st.subheader(product["name"])

            a, b, c, d = st.columns(4)

            with a:
                st.metric("Current stock", f"{product['stock']} units")

            with b:
                st.metric("7-day demand", f"{forecast:.0f} units")

            with c:
                st.metric("Stock coverage", f"{coverage:.1f} days")

            with d:
                st.metric("Suggested reorder", f"{reorder} units")

            status = status_for_product(product)

            if status == "Critical":
                st.error(
                    f"Critical: stock is very low. Consider ordering "
                    f"{reorder} units."
                )
            elif status == "Low":
                st.warning(
                    f"Low stock: forecast suggests ordering around "
                    f"{reorder} units."
                )
            else:
                st.success("Stock level looks healthy.")

    st.divider()

    st.subheader("📈 7-day demand outlook")

    # Native Streamlit chart using a plain dictionary.
    # This avoids pandas/Altair dependencies.
    days = [(datetime.now() + timedelta(days=i)).strftime("%a") for i in range(7)]

    totals = []
    for i in range(7):
        daily_total = 0
        for product in products:
            daily = max(0.1, float(product["daily_demand"]))
            pattern = [0.90, 0.96, 1.00, 1.05, 1.12, 1.18, 0.98][i]
            daily_total += daily * pattern
        totals.append(round(daily_total, 1))

    # Lightweight text-based forecast bars; no Altair or chart imports.
    for i in range(len(days)):
        bar = "█" * max(1, int(totals[i] * 2))
        st.write(f"**{days[i]}**  {bar}  {totals[i]:.1f} units")

# ------------------------------------------------------------
# Alerts
# ------------------------------------------------------------

def alerts_page():
    store = get_store()

    st.title("🔔 Alerts")
    st.write("Important inventory events that need your attention.")

    critical = critical_products(store)
    low = [
        p for p in low_stock_products(store)
        if p not in critical
    ]

    if not critical and not low:
        st.success("🎉 No active inventory alerts.")
        return

    if critical:
        st.subheader("🔴 Critical alerts")

        for product in critical:
            forecast, coverage, reorder = forecast_for_product(product)

            with st.container(border=True):
                st.error(
                    f"{product['name']} has only {product['stock']} units left."
                )
                st.write(
                    f"Estimated coverage: **{coverage:.1f} days**  •  "
                    f"Suggested reorder: **{reorder} units**"
                )

    if low:
        st.subheader("🟠 Low-stock alerts")

        for product in low:
            forecast, coverage, reorder = forecast_for_product(product)

            with st.container(border=True):
                st.warning(
                    f"{product['name']} is below its reorder level."
                )
                st.write(
                    f"Current stock: **{product['stock']}**  •  "
                    f"Suggested reorder: **{reorder} units**"
                )


# ------------------------------------------------------------
# Profile
# ------------------------------------------------------------

def profile_page():
    store = get_store()

    st.title("👤 Store Profile")
    st.write("Manage your StockWise account and store information.")

    st.subheader("Account")

    with st.container(border=True):
        a, b = st.columns(2)

        with a:
            st.write("**Owner**")
            st.write(store["owner"])

            st.write("**Email**")
            st.write(store["email"])

        with b:
            st.write("**Phone**")
            st.write(store["phone"])

            st.write("**Location**")
            st.write(store["location"])

    st.divider()

    st.subheader("Store information")

    with st.container(border=True):
        st.write("**Store name**")
        st.write(store["store_name"])

        st.write("**Store ID**")
        st.code(store["store_id"])

        st.write("**Products managed**")
        st.write(str(len(store["products"])))

        st.write("**Total sales recorded**")
        st.write(str(len(store["sales"])))

    st.divider()

    st.subheader("🔒 Privacy & data")

    st.info(
        "Each account has its own store data in this prototype. "
        "A production StockWise backend would store this information "
        "in a secure database and enforce account-level access control."
    )


# ------------------------------------------------------------
# Main app
# ------------------------------------------------------------

if not st.session_state.logged_in:
    login_page()
else:
    sidebar()

    if st.session_state.page == "Dashboard":
        dashboard()
    elif st.session_state.page == "Inventory":
        inventory_page()
    elif st.session_state.page == "Sales":
        sales_page()
    elif st.session_state.page == "AI Forecast":
        forecast_page()
    elif st.session_state.page == "Alerts":
        alerts_page()
    elif st.session_state.page == "Profile":
        profile_page()

