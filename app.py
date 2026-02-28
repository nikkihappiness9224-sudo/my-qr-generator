import streamlit as st

# --- INITIAL DATA ---
if 'menu' not in st.session_state:
    st.session_state.menu = [
        ["Tomato Soup", 120], ["Sweet Corn Soup", 130], ["Veg Manchurian", 180],
        ["Chicken 65", 220], ["Paneer Tikka", 240], ["Butter Naan", 40],
        ["Veg Biryani", 200], ["Paneer Butter Masala", 260], ["Dal Tadka", 180],
        ["Mixed Veg Curry", 220], ["Chicken Biryani", 260], ["Butter Chicken", 320],
        ["Chicken Curry", 280], ["Fish Fry", 300], ["Mutton Rogan Josh", 380],
        ["Veg Fried Rice", 190], ["Chicken Fried Rice", 220], ["Hakka Noodles Veg", 180],
        ["Hakka Noodles Chicken", 210], ["Gulab Jamun", 90], ["Ice Cream", 100],
        ["Brownie with Ice Cream", 160], ["Fresh Lime Soda", 80], ["Cold Coffee", 120],
        ["Masala Chai", 50], ["Soft Drinks", 60]
    ]

# --- SESSION STATE FOR DATA ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
    st.session_state.parcel = []
    st.session_state.daily_sales = 0.0
    st.session_state.daily_items_sold = 0
    st.session_state.total_bills = 0

# --- NAVIGATION STATE ---
# Step 0: Tables, 1: Menu, 2: Dine-in, 3: Parcel, 4: Bill, 5: Sales
if 'step' not in st.session_state:
    st.session_state.step = 0

def next_step():
    if st.session_state.step < 5:
        st.session_state.step += 1
    else:
        st.session_state.step = 0 # Loop back to start

# --- THE WEBSITE UI ---
st.set_page_config(page_title="Snake Scripters", page_icon="🐍")
st.title("🐍 SNAKE SCRIPTERS RESTAURANT")

# Display current progress
steps_names = ["Table Check", "View Menu", "Dine-in Order", "Parcel Order", "Generate Bill", "Daily Report"]
st.caption(f"Step {st.session_state.step + 1} of 6: **{steps_names[st.session_state.step]}**")
st.progress((st.session_state.step + 1) / 6)

# --- SCREEN 0: SHOW TABLES ---
if st.session_state.step == 0:
    st.header("1. Table Management")
    available = ["t1", "t3", "t5"]
    reserved = ["t2", "t4", "t6", "t7"]
    st.write(f"All Tables: t1, t2, t3, t4, t5, t6, t7")
    t = st.text_input("Enter the table number:").lower()
    if t:
        if t in available: st.success(f"Table {t} is AVAILABLE")
        elif t in reserved: st.error(f"Table {t} is RESERVED")
        else: st.warning("Table not found")

# --- SCREEN 1: SHOW MENU ---
elif st.session_state.step == 1:
    st.header("2. Restaurant Menu")
    st.table(st.session_state.menu)

# --- SCREEN 2: TAKE DINE-IN ORDER ---
elif st.session_state.step == 2:
    st.header("3. Take Dine-in Order")
    item_names = [item[0] for item in st.session_state.menu]
    order_selection = st.selectbox("Select item to add:", item_names)
    if st.button("Add to Dine-in Order"):
        item_data = next(i for i in st.session_state.menu if i[0] == order_selection)
        st.session_state.orders.append(item_data)
        st.toast(f"Confirmed: {order_selection}")
    
    st.subheader("Current Dine-in Items:")
    if not st.session_state.orders: st.info("No items added.")
    for o in st.session_state.orders:
        st.text(f"✅ {o[0]} - Rs {o[1]}")

# --- SCREEN 3: TAKE PARCEL ORDER ---
elif st.session_state.step == 3:
    st.header("4. Take Parcel Order")
    item_names = [item[0] for item in st.session_state.menu]
    parcel_selection = st.selectbox("Select item for Parcel:", item_names)
    if st.button("Add to Parcel"):
        item_data = next(i for i in st.session_state.menu if i[0] == parcel_selection)
        st.session_state.parcel.append(item_data)
        st.toast(f"Parcel Confirmed: {parcel_selection}")
    
    st.subheader("Current Parcel Items:")
    if not st.session_state.parcel: st.info("No items added.")
    for p in st.session_state.parcel:
        st.text(f"📦 {p[0]} - Rs {p[1]}")

# --- SCREEN 4: GENERATE BILL ---
elif st.session_state.step == 4:
    st.header("5. Final Bill Generation")
    order_total = sum(i[1] for i in st.session_state.orders)
    parcel_total = sum(i[1] for i in st.session_state.parcel)
    
    if order_total == 0 and parcel_total == 0:
        st.warning("No orders placed yet. Go back or add items to see the bill.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Dine-in")
            for item in st.session_state.orders: st.write(f"{item[0]} (Rs {item[1]})")
        with col2:
            st.write("### Parcel")
            for item in st.session_state.parcel: st.write(f"{item[0]} (Rs {item[1]})")
        
        parcel_charge = 50 if st.session_state.parcel else 0
        total = order_total + parcel_total + parcel_charge
        gst = total * 0.06
        final_bill = total + gst
        
        st.divider()
        st.subheader(f"Total Bill: Rs {round(final_bill, 2)}")
        st.write(f"(Includes Rs {parcel_charge} parcel fee and Rs {round(gst, 2)} GST)")
        
        if st.button("Complete Transaction & Reset Order"):
            st.session_state.daily_sales += final_bill
            st.session_state.daily_items_sold += len(st.session_state.orders) + len(st.session_state.parcel)
            st.session_state.total_bills += 1
            st.session_state.orders = [] # Clear for next customer
            st.session_state.parcel = [] # Clear for next customer
            st.success("Transaction Saved!")
            st.balloons()

# --- SCREEN 5: DAILY SALES REPORT ---
elif st.session_state.step == 5:
    st.header("6. Daily Sales Report")
    st.metric("Total Bills Generated", st.session_state.total_bills)
    st.metric("Total Items Sold Today", st.session_state.daily_items_sold)
    st.metric("Total Sales Today", f"Rs {round(st.session_state.daily_sales, 2)}")
    
    if st.button("Reset Sales Data for Tomorrow"):
        st.session_state.daily_sales = 0
        st.session_state.daily_items_sold = 0
        st.session_state.total_bills = 0
        st.rerun()

# --- NAVIGATION BUTTON ---
st.divider()
button_label = "Go to Next Step ➡️" if st.session_state.step < 5 else "Start New Customer 🔄"
if st.button(button_label, use_container_width=True):
    next_step()
    st.rerun()
# --- ADMIN SECTION: QR CODE FOR TABLE ---
with st.sidebar:
    st.divider()
    st.subheader("Restaurant QR Code")
    # This automatically gets your website's real URL
    current_url = "https://your-app-name.streamlit.app" 
    
    import qrcode
    from io import BytesIO
    
    qr = qrcode.make(current_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Scan to Open Menu")
    st.write("Print this and put it on your tables!")

