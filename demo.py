from food_delivery import Customer, DeliveryPartner, Restaurant, FoodItem, Order


# 1. Register customer Priya
priya = Customer(
    name="Priya",
    phone="9876543210",
    address="Bangalore"
)

print("Customer registered:", priya.name)


# 2. Register delivery partner Rajesh
rajesh = DeliveryPartner(
    name="Rajesh",
    vehicle="Bike"
)

print("Delivery partner registered:", rajesh.name)


# 3. Create Bawarchi and add food items
bawarchi = Restaurant(
    name="Bawarchi",
    address="MG Road"
)

biryani = FoodItem(
    name="Biryani",
    price=250
)

kebab = FoodItem(
    name="Kebab",
    price=150
)

bawarchi.add_item(biryani)
bawarchi.add_item(kebab)

print("Restaurant created:", bawarchi.name)
print("Food items added: Biryani, Kebab")


# 4. Top up Priya's wallet
print("\n--- Wallet ---")

priya.top_up_wallet(500)

# Attempt invalid negative top-up
priya.top_up_wallet(-100)

print("Wallet balance:", priya.wallet)


# 5. Priya places an order
order = Order(
    customer=priya,
    restaurant=bawarchi,
    items=[biryani, kebab]
)

print("\n--- Order Placed ---")
print("Customer:", priya.name)
print("Restaurant:", bawarchi.name)


# 6. Print bill details
print("\n--- Bill Details ---")

print("Subtotal:", order.calculate_subtotal())
print("GST:", order.calculate_gst())
print("Packaging Fee:", order.calculate_packaging_fee())
print("Total:", order.calculate_total())
print("Estimated Delivery Time:", order.estimated_delivery_time())


# 7. Rajesh accepts the order
print("\n--- Delivery ---")

rajesh.accept_order(order)

print("Trying wrong OTP:")
rajesh.deliver_order(order, "9999")

print("Trying correct OTP:")
rajesh.deliver_order(order, "1234")


# 8. Notify Priya and Rajesh
print("\n--- Notifications ---")

priya.notify("Order delivered")
rajesh.notify("Order delivered")
