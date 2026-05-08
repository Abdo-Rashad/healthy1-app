import streamlit as st
import pandas as pd
import joblib


model = joblib.load("model/diet_model.pkl")
columns = joblib.load("model/columns.pkl")

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Personalized Diet System",
    page_icon="🥗",
    layout="wide"
)

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("🥗 Menu")
page = st.sidebar.radio(
    "Go to",["Home", "Get Your Diet Plan", "Results"])

# =========================================
# PAGE 1: HOME
# =========================================
if page == "Home":

    st.title("🥗 Personalized Diet Recommendation System")

    st.markdown("""
    ### 💡 فكرة المشروع

    النظام بيستخدم Machine Learning + Rule-Based
    علشان يطلع لك نظام غذائي مناسب ليك.

    ---
    ### ⚙️ بيشتغل إزاي؟
    1. تدخل بياناتك  
    2. الموديل يحسب احتياجك  
    3. النظام يطلع لك 3 وجبات  
    """)

    st.success("👉 روح على صفحة Get Your Diet Plan")


# =========================================
# PAGE 2: INPUT
# =========================================
elif page == "Get Your Diet Plan":

    st.title("🧑‍⚕️ Enter Your Data")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 10, 100, 25)

        height = st.number_input("Height (cm)", 100, 220, 170)
        weight = st.number_input("Weight (kg)", 30, 200, 70)

        height_m = height / 100
        bmi = weight / (height_m ** 2)

        st.metric("Calculated BMI", f"{bmi:.2f}")

        systolic = st.number_input("Blood Pressure (Systolic)", 80, 200, 120)
        diastolic = st.number_input("Blood Pressure (Diastolic)", 50, 150, 80)

    with col2:
        cholesterol = st.number_input("Cholesterol Level", 100, 400, 180)
        sugar = st.number_input("Blood Sugar Level", 50, 300, 90)
        steps = st.number_input("Daily Steps", 0, 20000, 6000)
        exercise = st.number_input("Exercise Frequency", 0, 7, 3)
        sleep = st.number_input("Sleep Hours", 3.0, 12.0, 7.0)

        calories = st.number_input("Current Caloric Intake", 1000, 5000, 2000)
        protein = st.number_input("Current Protein Intake", 0, 300, 100)
        carbs = st.number_input("Current Carb Intake", 0, 500, 250)
        fat = st.number_input("Current Fat Intake", 0, 200, 70)

    if st.button("🚀 Generate Diet Plan"):

        new_person = {
            "Age": age,
            "Height_cm": height,
            "Weight_kg": weight,
            "BMI": bmi,
            "Blood_Pressure_Systolic": systolic,
            "Blood_Pressure_Diastolic": diastolic,
            "Cholesterol_Level": cholesterol,
            "Blood_Sugar_Level": sugar,
            "Daily_Steps": steps,
            "Exercise_Frequency": exercise,
            "Sleep_Hours": sleep,
            "Caloric_Intake": calories,
            "Protein_Intake": protein,
            "Carbohydrate_Intake": carbs,
            "Fat_Intake": fat
        }

        df_person = pd.DataFrame([new_person])
        df_person = df_person.reindex(columns=columns)
        df_person = df_person.fillna(0)

        pred = model.predict(df_person)[0]

        st.session_state["results"] = {
            "calories": pred[0],
            "protein": pred[1],
            "carbs": pred[2],
            "fats": pred[3]
        }

        st.success("✅ Plan Generated!")
        st.info("👉 Go to Results Page")


# =========================================
# PAGE 3: RESULTS
# =========================================
elif page == "Results":

    st.title("🍽️ Your Diet Plan")

    if "results" not in st.session_state:
        st.warning("⚠️ Please enter your data first")
    else:

        res = st.session_state["results"]

        # ===== Macros =====
        st.subheader("🔢 Recommended Intake")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Calories", round(res["calories"]))
        col2.metric("Protein (g)", round(res["protein"]))
        col3.metric("Carbs (g)", round(res["carbs"]))
        col4.metric("Fats (g)", round(res["fats"]))

        # ===== Food Data =====
        foods = {
            "rice": {"carbs": 28, "protein": 2.7, "fat": 0.3},
            "bread": {"carbs": 49, "protein": 9, "fat": 3.2},
            "chicken": {"carbs": 0, "protein": 27, "fat": 3.6},
            "beef": {"carbs": 0, "protein": 26, "fat": 15},
            "fish": {"carbs": 0, "protein": 22, "fat": 5},
            "salad": {"carbs": 5, "protein": 1, "fat": 0.2},
            "vegetables": {"carbs": 7, "protein": 2, "fat": 0.3},
            "olive_oil": {"carbs": 0, "protein": 0, "fat": 100}
        }

        def generate_meals(p, c, f):

            meals = []
            p, c, f = p / 3, c / 3, f / 3

            # Meal 1
            rice = (c / foods["rice"]["carbs"]) * 100
            fish = (p / foods["fish"]["protein"]) * 100
            oil = max(f - (fish / 100) * foods["fish"]["fat"], 0)

            meals.append({
                "name": "🍚 Rice + Fish + Salad",
                "rice": rice,
                "fish": fish,
                "salad": 100,
                "olive_oil": oil
            })

            # Meal 2
            rice = (c / foods["rice"]["carbs"]) * 100
            beef = (p / foods["beef"]["protein"]) * 100
            oil = max(f - (beef / 100) * foods["beef"]["fat"], 0)

            meals.append({
                "name": "🥩 Rice + Beef + Salad",
                "rice": rice,
                "beef": beef,
                "salad": 100,
                "olive_oil": oil
            })

            # Meal 3
            bread = (c / foods["bread"]["carbs"]) * 100
            chicken = (p / foods["chicken"]["protein"]) * 100
            oil = max(f - (chicken / 100) * foods["chicken"]["fat"], 0)

            meals.append({
                "name": "🍗 Bread + Chicken + Vegetables",
                "bread": bread,
                "chicken": chicken,
                "vegetables": 100,
                "olive_oil": oil
            })

            return meals


        meals = generate_meals(
            res["protein"],
            res["carbs"],
            res["fats"]
        )

        st.subheader("🍽️ Your Meals")

        for meal in meals:
            st.markdown(f"### {meal['name']}")

            for food, grams in meal.items():
                if food != "name":
                    st.write(f"{food.capitalize()}: {round(grams)} g")

            st.markdown("---")
