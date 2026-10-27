import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Electricity Analyzer", page_icon="⚡")
st.title("⚡ Electricity Consumption Analyzer")
st.write("Track power consumption patterns, visualize usage, and forecast bills.")

# 1. Base Data
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Units": [120, 135, 160, 210, 240, 190],
    "Rate": [7.5, 7.5, 7.5, 7.5, 7.5, 7.5]
}

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# 2. Add New Entry
st.subheader("➕ Record New Reading")
c1, c2, c3 = st.columns(3)
with c1:
    m = st.selectbox("Month", ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
with c2:
    u = st.number_input("Units Consumed (kWh)", min_value=1.0, value=150.0, step=5.0)
with c3:
    r = st.number_input("Rate per Unit (₹)", min_value=1.0, value=7.5, step=0.5)

if st.button("Add Record"):
    new_row = pd.DataFrame([[m, u, r]], columns=["Month", "Units", "Rate"])
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    st.success(f"Added reading for {m}!")
    st.rerun()

st.divider()

# 3. Consumption Summary
st.subheader("📊 Consumption Overview")
total_units = df["Units"].sum()
total_cost = (df["Units"] * df["Rate"]).sum()
avg_units = df["Units"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Units", f"{total_units:.0f} kWh")
col2.metric("Total Cost", f"₹ {total_cost:,.0f}")
col3.metric("Avg Monthly", f"{avg_units:.0f} kWh")

# 4. Chart
st.subheader("📈 Monthly Consumption Chart")
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.bar(df["Month"], df["Units"], color="#1f77b4", edgecolor="black")
ax.set_ylabel("Units (kWh)")
ax.set_xlabel("Month")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# 5. Projection & Tips
st.divider()
p1, p2 = st.columns(2)

with p1:
    st.subheader("🔮 Next Month Estimate")
    est_bill = avg_units * df["Rate"].iloc[-1]
    st.write(f"Based on your average past usage (**{avg_units:.0f} units**):")
    st.info(f"👉 Expected Next Bill: **₹ {est_bill:,.0f}**")

with p2:
    st.subheader("💡 Energy Saving Tips")
    if avg_units > 180:
        st.warning("⚠️ High average consumption detected!")
    st.write("• Set AC temperature to 24°C–26°C.")
    st.write("• Turn off appliances from the wall switch to cut phantom standby power.")
    st.write("• Ensure refrigerator door seals are tight.")
                             
