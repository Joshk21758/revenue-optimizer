import requests
import streamlit as st

st.set_page_config(
    page_title="Revenue Optimization App", layout="wide"
)

st.title("Dynamic Pricing & Revenue Control")
st.markdown(
    "Simulate real-time market conditions to compute optimal pricing strategies."
)

col1, col2 = st.columns(2)

with col1:
  st.subheader("Market & Cost Inputs")
  base_cost = st.number_input("Base Cost (K)", min_value=1.0, value=50.0)
  competitor_price = st.number_input(
      "Competitor Price (K)", min_value=1.0, value=75.0
  )
  inventory_count = st.slider("Inventory Stock Level", 0, 500, 120)
  demand_index = st.slider("Estimated Demand Score", 0.1, 5.0, 1.2, 0.1)
  day_of_week = st.selectbox(
      "Day of Week",
      options=[
          ("Monday", 0),
          ("Tuesday", 1),
          ("Wednesday", 2),
          ("Thursday", 3),
          ("Friday", 4),
          ("Saturday", 5),
          ("Sunday", 6),
      ],
      format_func=lambda x: x[0],
  )[1]

# API payload construction
payload = {
    "base_cost": base_cost,
    "competitor_price": competitor_price,
    "inventory_count": inventory_count,
    "demand_index": demand_index,
    "day_of_week": day_of_week,
}

with col2:
  st.subheader("Optimization Output")
  if st.button("Calculate Optimal Price", type="primary"):
    try:
      # Point to your local or deployed FastAPI instance
      response = requests.post(
          "http://localhost:8000/predict-price", json=payload
      )
      if response.status_code == 200:
        res_data = response.json()

        st.metric(
            label="Recommended Optimal Price",
            value=f"K{res_data['recommended_price']}",
            delta=f"{round(((res_data['recommended_price'] - base_cost) / base_cost) * 100, 1)}% markup",
        )

        st.metric(
            label="Projected Revenue Impact",
            value=f"K{res_data['projected_revenue']}",
        )

        st.info(
            f"Applied Demand Multiplier Factor: {res_data['demand_multiplier']}x"
        )
      else:
        st.error(f"API Error: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
      st.error(
          "Could not connect to the FastAPI backend. Ensure it is running on"
          " port 8000."
      )