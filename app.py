import streamlit as st
from Food_Delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(
    page_title="Food Delivery OOP",
    page_icon="🍔",
    layout="wide"
)

# -----------------------------
# Session state
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Bawarchi", "MG Road")
    restaurant.add_item(MenuItem("Biryani", 250, False))
    restaurant.add_item(MenuItem("Kebab", 180, False))
    restaurant.add_item(MenuItem("Paneer Tikka", 220, True))
    restaurant.add_item(MenuItem("Veg Biryani", 200, True))
    st.session_state.restaurant = restaurant

if "order" not in st.session_state:
    st.session_state.order = None


st.title("🍔 Food Delivery System")
st.caption("Simple Streamlit interface for your Python OOP project")

restaurant = st.session_state.restaurant

# -----------------------------
# 1. Create Customer
# -----------------------------
st.header("1️⃣ Create Customer")

with st.form("customer_form"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")

    create_customer = st.form_submit_button("Create Customer")

if create_customer:
    if name and phone and address:
        st.session_state.customer = Customer(name, phone, address)
        st.success("Customer created successfully!")
    else:
        st.warning("Please enter all customer details.")

if st.session_state.customer:
    customer = st.session_state.customer
    st.info(
        f"Customer: {customer._name} | "
        f"Phone: {customer._phone} | "
        f"Wallet: ₹{customer._wallet_balance:.2f}"
    )


# -----------------------------
# 2. Add Wallet Balance
# -----------------------------
st.header("2️⃣ Add Wallet Balance")

if st.session_state.customer:
    amount = st.number_input(
        "Enter amount",
        min_value=0.0,
        step=100.0
    )

    if st.button("Add Money"):
        if amount > 0:
            st.session_state.customer.add_to_wallet(amount)
            st.success(f"₹{amount:.2f} added to wallet.")
            st.rerun()
        else:
            st.warning("Enter an amount greater than 0.")
else:
    st.warning("Create a customer first.")


# -----------------------------
# 3. Show Restaurant Menu
# -----------------------------
st.header("3️⃣ Restaurant Menu")

st.subheader(f"{restaurant.name} - {restaurant.location}")

menu_data = []

for item in restaurant.get_menu():
    menu_data.append({
        "Item": item.name,
        "Price": f"₹{item.price}",
        "Type": "Veg" if item.is_veg else "Non-Veg"
    })

st.table(menu_data)


# -----------------------------
# 4. Place Order
# -----------------------------
st.header("4️⃣ Place an Order")

if st.session_state.customer:

    menu_items = restaurant.get_menu()

    selected_names = st.multiselect(
        "Select food items",
        options=[item.name for item in menu_items]
    )

    if selected_names:
        selected_items = [
            item for item in menu_items
            if item.name in selected_names
        ]

        subtotal = sum(item.price for item in selected_items)
        gst = subtotal * 0.05
        packaging = 20
        total = subtotal + gst + packaging

        st.write(f"Subtotal: ₹{subtotal:.2f}")
        st.write(f"GST (5%): ₹{gst:.2f}")
        st.write(f"Packaging Fee: ₹{packaging:.2f}")
        st.write(f"### Total: ₹{total:.2f}")

        if st.button("Place Order"):

            customer = st.session_state.customer

            if customer._wallet_balance >= total:
                order = customer.place_order(
                    restaurant,
                    selected_items
                )

                customer._wallet_balance -= total
                st.session_state.order = order

                st.success(f"Order #{order._order_id} placed successfully!")

                # Show OTP only for this simple college/demo project.
                st.warning(f"Delivery OTP: {order._otp}")

                st.write(f"Order Status: **{order._status}**")
            else:
                st.error(
                    f"Insufficient wallet balance. "
                    f"Required ₹{total:.2f}, "
                    f"Available ₹{customer._wallet_balance:.2f}"
                )

else:
    st.warning("Create a customer first.")


# -----------------------------
# 5. Create Delivery Partner
# -----------------------------
st.header("5️⃣ Create Delivery Partner")

with st.form("delivery_form"):
    partner_name = st.text_input("Delivery Partner Name")
    partner_phone = st.text_input("Delivery Partner Phone")
    vehicle = st.selectbox(
        "Vehicle",
        ["Bike", "Scooter", "Cycle"]
    )

    create_partner = st.form_submit_button(
        "Create Delivery Partner"
    )

if create_partner:
    if partner_name and partner_phone:
        st.session_state.delivery_partner = DeliveryPartner(
            partner_name,
            partner_phone,
            vehicle
        )
        st.success("Delivery partner created successfully!")
    else:
        st.warning("Please enter name and phone number.")


# -----------------------------
# 6. Accept Order
# -----------------------------
st.header("6️⃣ Accept the Order")

order = st.session_state.order
partner = st.session_state.delivery_partner

if order and partner:

    st.write(f"Order ID: **#{order._order_id}**")
    st.write(f"Current Status: **{order._status}**")

    if st.button("Accept Order"):
        if partner.accept_order(order):
            st.success("Order accepted by delivery partner!")
            st.rerun()
        else:
            st.error("Delivery partner is not available.")

elif not order:
    st.warning("Place an order first.")
elif not partner:
    st.warning("Create a delivery partner first.")


# -----------------------------
# 7. Enter OTP and Complete Delivery
# -----------------------------
st.header("7️⃣ Complete Delivery")

if order and partner:

    st.write(f"Order ID: **#{order._order_id}**")
    st.write(f"Current Status: **{order._status}**")

    entered_otp = st.text_input(
        "Enter Delivery OTP",
        max_chars=4
    )

    if st.button("Complete Delivery"):

        if order._status != "Accepted":
            st.warning("Delivery partner must accept the order first.")

        elif entered_otp.isdigit() and len(entered_otp) == 4:

            if partner.deliver(order, int(entered_otp)):
                st.success("🎉 Delivery completed successfully!")
                st.write(f"Final Order Status: **{order._status}**")
                st.rerun()
            else:
                st.error("Incorrect OTP.")

        else:
            st.warning("Please enter a valid 4-digit OTP.")

elif not order:
    st.warning("Place an order first.")

# -----------------------------
# Current Order Summary
# -----------------------------
if st.session_state.order:
    st.header("📦 Current Order")

    order = st.session_state.order

    st.write(f"Order ID: **#{order._order_id}**")
    st.write(f"Status: **{order._status}**")
    st.write(f"Bill: **₹{order.calculate_bill():.2f}**")
    st.write(f"Estimated Time: **{order.estimated_time()} minutes**")

    if st.session_state.customer:
        st.write(
            f"Customer Wallet: "
            f"**₹{st.session_state.customer._wallet_balance:.2f}**"
        )
