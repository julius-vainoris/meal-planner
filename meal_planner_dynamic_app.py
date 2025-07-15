
import streamlit as st
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="Weekly Meal Builder", layout="wide")

# --- Approved Foods ---
approved_foods = {
    "Proteins": ["Chicken breast", "Salmon", "Tofu", "Eggs", "Greek yogurt"],
    "Carbs": ["Quinoa", "Buckwheat", "Rye bread", "Sweet potato"],
    "Veggies": ["Spinach", "Kale", "Broccoli", "Zucchini", "Cabbage"],
    "Fats": ["Avocado", "Olive oil", "Almond butter", "Walnuts"]
}

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
meals = ["Breakfast", "Lunch", "Dinner", "Snack"]

st.title("🥗 Weekly Meal Planner & Shopping List")

st.markdown("### ✅ Step 1: Build your meals for each day")

# Session state to store selections
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {day: {meal: [] for meal in meals} for day in days_of_week}

# Dynamic UI for each day & meal
with st.expander("🗓️ Click to plan your meals", expanded=True):
    for day in days_of_week:
        st.subheader(day)
        cols = st.columns(4)
        for idx, meal in enumerate(meals):
            with cols[idx % 4]:
                selection = st.multiselect(
                    f"{meal}",
                    sum(approved_foods.values(), []),
                    default=st.session_state.meal_plan[day][meal],
                    key=f"{day}_{meal}"
                )
                st.session_state.meal_plan[day][meal] = selection

# --- Generate Shopping List ---
def generate_shopping_list(meal_plan):
    shopping = defaultdict(int)
    for day, meal_dict in meal_plan.items():
        for meal_items in meal_dict.values():
            for item in meal_items:
                shopping[item] += 1
    return shopping

shopping_list = generate_shopping_list(st.session_state.meal_plan)

# Display Meal Plan Table
st.markdown("### 📋 Your Weekly Meal Plan")
for day, meal_dict in st.session_state.meal_plan.items():
    st.write(f"**{day}**")
    for meal, items in meal_dict.items():
        if items:
            st.write(f" - {meal}: {', '.join(items)}")
        else:
            st.write(f" - {meal}: _(no selection)_")

# Display Shopping List
st.markdown("### 🛒 Combined Shopping List")
if shopping_list:
    df_shop = pd.DataFrame(sorted(shopping_list.items()), columns=["Item", "Times Used"])
    st.dataframe(df_shop, use_container_width=True)
    csv = df_shop.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Shopping List CSV", csv, "shopping_list.csv", "text/csv")
else:
    st.info("No items selected yet.")

st.markdown("---")
st.caption("✅ Select ingredients for each meal → See your plan & shopping list instantly!")
