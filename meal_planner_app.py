import streamlit as st
import json
import pandas as pd

# Load meal plan data
def load_data():
    with open("weekly_meal_plan_data.json", "r") as f:
        return json.load(f)

data = load_data()
meal_plan = data["meal_plan"]
shopping_list = data["shopping_list"]

st.title("🥗 Weekly Meal Planner & Shopping List")

# Show Meal Plan
st.header("🗓️ Weekly Meal Plan")
for day, meals in meal_plan.items():
    st.subheader(day)
    if isinstance(meals, dict):
        for meal, ingredients in meals.items():
            st.markdown(f"**{meal}:**")
            st.markdown("- " + "\n- ".join(ingredients))
    else:
        st.markdown(f"*{meals}*")

# Show Shopping List
st.header("🛒 Shopping List")
sorted_items = sorted(shopping_list.items())
df = pd.DataFrame(sorted_items, columns=["Item", "Approx. Qty"])
st.dataframe(df, use_container_width=True)

# Download CSV button
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Shopping List (CSV)", csv, "shopping_list.csv", "text/csv")
