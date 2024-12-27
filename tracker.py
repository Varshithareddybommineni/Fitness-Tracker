import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime, timedelta
import calendar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import json
from PIL import Image, ImageTk
import webbrowser
import csv
import os

# Initialize Database
def initialize_database():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS step_counter (
        date TEXT PRIMARY KEY,
        steps INTEGER,
        distance REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_log (
        date TEXT,
        exercise TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrition (
        date TEXT,
        food TEXT,
        calories INTEGER
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hydration (
        date TEXT,
        water_consumed REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sleep (
        date TEXT,
        hours REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_goals (
        date TEXT PRIMARY KEY,
        steps_goal INTEGER,
        water_goal REAL,
        calories_goal INTEGER,
        workout_goal TEXT
    )""")
    conn.commit()
    conn.close()

# Step Counter
def log_steps():
    def save_steps():
        date = entry_date.get()
        steps = int(entry_steps.get())
        distance = steps * 0.0008  # Assuming average step length of 0.8 meters
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO step_counter (date, steps, distance) VALUES (?, ?, ?)",
                       (date, steps, distance))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Steps logged for {date}.")
        step_window.destroy()

    step_window = tk.Toplevel()
    step_window.title("Log Steps")
    tk.Label(step_window, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(step_window)
    entry_date.pack()
    tk.Label(step_window, text="Steps:").pack()
    entry_steps = tk.Entry(step_window)
    entry_steps.pack()
    tk.Button(step_window, text="Save", command=save_steps).pack()

# Workout Log
def log_workout():
    def save_workout():
        date = entry_date.get()
        exercise = entry_exercise.get()
        sets = int(entry_sets.get())
        reps = int(entry_reps.get())
        weight = float(entry_weight.get())
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workout_log (date, exercise, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
                       (date, exercise, sets, reps, weight))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Workout logged for {date}.")
        workout_window.destroy()

    workout_window = tk.Toplevel()
    workout_window.title("Log Workout")
    tk.Label(workout_window, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(workout_window)
    entry_date.pack()
    tk.Label(workout_window, text="Exercise:").pack()
    entry_exercise = tk.Entry(workout_window)
    entry_exercise.pack()
    tk.Label(workout_window, text="Sets:").pack()
    entry_sets = tk.Entry(workout_window)
    entry_sets.pack()
    tk.Label(workout_window, text="Reps:").pack()
    entry_reps = tk.Entry(workout_window)
    entry_reps.pack()
    tk.Label(workout_window, text="Weight (kg):").pack()
    entry_weight = tk.Entry(workout_window)
    entry_weight.pack()
    tk.Button(workout_window, text="Save", command=save_workout).pack()

# Nutrition Tracker
def log_nutrition():
    def save_food():
        date = entry_date.get()
        food = entry_food.get()
        calories = int(entry_calories.get())
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO nutrition (date, food, calories) VALUES (?, ?, ?)",
                       (date, food, calories))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Nutrition logged for {date}.")
        nutrition_window.destroy()

    nutrition_window = tk.Toplevel()
    nutrition_window.title("Log Nutrition")
    tk.Label(nutrition_window, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(nutrition_window)
    entry_date.pack()
    tk.Label(nutrition_window, text="Food:").pack()
    entry_food = tk.Entry(nutrition_window)
    entry_food.pack()
    tk.Label(nutrition_window, text="Calories:").pack()
    entry_calories = tk.Entry(nutrition_window)
    entry_calories.pack()
    tk.Button(nutrition_window, text="Save", command=save_food).pack()

# Hydration Tracker
def log_hydration():
    def save_hydration():
        date = entry_date.get()
        water = float(entry_water.get())
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hydration (date, water_consumed) VALUES (?, ?)", (date, water))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Hydration logged for {date}.")
        hydration_window.destroy()

    hydration_window = tk.Toplevel()
    hydration_window.title("Log Hydration")
    tk.Label(hydration_window, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(hydration_window)
    entry_date.pack()
    tk.Label(hydration_window, text="Water Consumed (L):").pack()
    entry_water = tk.Entry(hydration_window)
    entry_water.pack()
    tk.Button(hydration_window, text="Save", command=save_hydration).pack()

# Add this new function for setting and viewing goals
def manage_goals():
    def save_goals():
        date = entry_date.get()
        steps = int(entry_steps_goal.get())
        water = float(entry_water_goal.get())
        calories = int(entry_calories_goal.get())
        workout = entry_workout_goal.get()
        
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO daily_goals 
        (date, steps_goal, water_goal, calories_goal, workout_goal) 
        VALUES (?, ?, ?, ?, ?)""",
        (date, steps, water, calories, workout))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Goals set for {date}")
        
        # Show recommendations
        show_recommendations(date)
        goals_window.destroy()

    def show_recommendations(date):
        recommendations = f"""
Daily Goals and Recommendations for {date}:

🎯 Your Goals:
- Steps: {entry_steps_goal.get()} steps
- Water: {entry_water_goal.get()}L
- Calories: {entry_calories_goal.get()} kcal
- Workout: {entry_workout_goal.get()}

💪 Recommended Schedule:
Morning:
- Drink 0.5L water upon waking
- Light stretching or yoga
- Healthy breakfast (~400 calories)

Afternoon:
- Take a walk during lunch break
- Stay hydrated (0.5L water)
- Balanced lunch (~600 calories)

Evening:
- Complete your planned workout
- Stay hydrated (0.5L water)
- Nutritious dinner (~600 calories)
- Light walking after dinner

Remember to:
- Take regular breaks to walk
- Keep a water bottle nearby
- Log your progress in the tracker
"""
        messagebox.showinfo("Daily Recommendations", recommendations)

    goals_window = tk.Toplevel()
    goals_window.title("Set Daily Goals")
    goals_window.geometry("300x400")

    tk.Label(goals_window, text="Date (YYYY-MM-DD):").pack()
    entry_date = tk.Entry(goals_window)
    entry_date.pack()

    tk.Label(goals_window, text="Steps Goal:").pack()
    entry_steps_goal = tk.Entry(goals_window)
    entry_steps_goal.insert(0, "10000")  # Default healthy goal
    entry_steps_goal.pack()

    tk.Label(goals_window, text="Water Goal (L):").pack()
    entry_water_goal = tk.Entry(goals_window)
    entry_water_goal.insert(0, "2.5")  # Default healthy goal
    entry_water_goal.pack()

    tk.Label(goals_window, text="Calories Goal:").pack()
    entry_calories_goal = tk.Entry(goals_window)
    entry_calories_goal.insert(0, "2000")  # Default healthy goal
    entry_calories_goal.pack()

    tk.Label(goals_window, text="Workout Goal:").pack()
    entry_workout_goal = tk.Entry(goals_window)
    entry_workout_goal.insert(0, "30 min cardio + strength training")  # Default goal
    entry_workout_goal.pack()

    tk.Button(goals_window, text="Set Goals", command=save_goals).pack(pady=20)

# Add this new function for viewing data
def view_progress():
    view_window = tk.Toplevel()
    view_window.title("View Progress")
    view_window.geometry("600x400")

    def get_data_for_date():
        date = entry_date.get()
        result_text.delete(1.0, tk.END)  # Clear previous results
        
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        
        # Fetch goals
        cursor.execute("SELECT * FROM daily_goals WHERE date=?", (date,))
        goals = cursor.fetchone()
        
        # Fetch steps
        cursor.execute("SELECT steps, distance FROM step_counter WHERE date=?", (date,))
        steps = cursor.fetchone()
        
        # Fetch workouts
        cursor.execute("SELECT exercise, sets, reps, weight FROM workout_log WHERE date=?", (date,))
        workouts = cursor.fetchall()
        
        # Fetch nutrition
        cursor.execute("SELECT food, calories FROM nutrition WHERE date=?", (date,))
        nutrition = cursor.fetchall()
        
        # Fetch hydration
        cursor.execute("SELECT water_consumed FROM hydration WHERE date=?", (date,))
        hydration = cursor.fetchone()
        
        # Display results
        result = f"📊 Progress Report for {date}\n"
        result += "=" * 40 + "\n\n"
        
        if goals:
            result += "🎯 Daily Goals:\n"
            result += f"Steps Goal: {goals[1]}\n"
            result += f"Water Goal: {goals[2]}L\n"
            result += f"Calories Goal: {goals[3]}\n"
            result += f"Workout Goal: {goals[4]}\n\n"
        
        if steps:
            result += "👣 Steps Tracked:\n"
            result += f"Steps: {steps[0]}\n"
            result += f"Distance: {steps[1]:.2f} km\n\n"
        
        if workouts:
            result += "💪 Workouts:\n"
            for workout in workouts:
                result += f"- {workout[0]}: {workout[1]} sets × {workout[2]} reps @ {workout[3]}kg\n"
            result += "\n"
        
        if nutrition:
            result += "🍎 Nutrition:\n"
            total_calories = 0
            for food in nutrition:
                result += f"- {food[0]}: {food[1]} calories\n"
                total_calories += food[1]
            result += f"Total Calories: {total_calories}\n\n"
        
        if hydration:
            result += "💧 Hydration:\n"
            result += f"Water Consumed: {hydration[0]}L\n"
        
        if not any([goals, steps, workouts, nutrition, hydration]):
            result += "No data found for this date."
            
        result_text.insert(tk.END, result)
        conn.close()

    # Date input
    frame_top = tk.Frame(view_window)
    frame_top.pack(pady=10)
    
    tk.Label(frame_top, text="Enter Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
    entry_date = tk.Entry(frame_top)
    entry_date.pack(side=tk.LEFT, padx=5)
    
    tk.Button(frame_top, text="View Progress", 
              command=get_data_for_date,
              bg="#ADD8E6").pack(side=tk.LEFT, padx=5)

    # Results area
    result_text = tk.Text(view_window, height=20, width=60)
    result_text.pack(pady=10, padx=10)

    # Add scrollbar
    scrollbar = tk.Scrollbar(view_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    result_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_text.yview)

# Add this new function for BMI calculator
def calculate_bmi():
    bmi_window = tk.Toplevel()
    bmi_window.title("BMI & Fitness Goal Calculator")
    bmi_window.geometry("500x700")

    def calculate_and_recommend():
        try:
            weight = float(entry_weight.get())
            height = float(entry_height.get()) / 100  # convert cm to meters
            age = int(entry_age.get())
            activity = activity_var.get()
            gender = gender_var.get()
            experience = experience_var.get()
            
            bmi = weight / (height * height)
            
            # Determine BMI category and recommendations
            if bmi < 18.5:
                category = "Underweight"
                recommendation = "BULK"
                color = "#FFB6C1"  # Light red
                workout_split = "Full Body 3x/week"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
                if body_type_var.get() == "Skinny Fat":
                    recommendation = "RECOMP"
                    color = "#98FB98"  # Light green
                    workout_split = "Upper/Lower 4x/week"
                else:
                    recommendation = "LEAN BULK"
                    color = "#87CEEB"  # Light blue
                    workout_split = "Push/Pull/Legs"
            elif 25 <= bmi < 30:
                category = "Overweight"
                recommendation = "CUT"
                color = "#FFA500"  # Orange
                workout_split = "Full Body + HIIT"
            else:
                category = "Obese"
                recommendation = "CUT"
                color = "#FF4500"  # Orange Red
                workout_split = "Full Body + Low Impact Cardio"

            # Calculate TDEE
            if gender == "Male":
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161

            activity_multipliers = {
                "Sedentary": 1.2,
                "Light Active": 1.375,
                "Moderately Active": 1.55,
                "Very Active": 1.725,
                "Extra Active": 1.9
            }
            
            tdee = bmr * activity_multipliers[activity]

            # Calculate macros based on goal and experience
            if recommendation == "BULK":
                if experience == "Beginner":
                    surplus = 300
                else:
                    surplus = 500
                target_calories = tdee + surplus
                protein = weight * 2.2  # 2.2g per kg
                carbs = weight * 4.5    # Higher carbs for bulking
                fats = weight * 0.9
            elif recommendation == "CUT":
                if experience == "Beginner":
                    deficit = 300
                else:
                    deficit = 500
                target_calories = tdee - deficit
                protein = weight * 2.5  # Higher protein for cutting
                carbs = weight * 2.5
                fats = weight * 0.7
            else:  # RECOMP
                target_calories = tdee
                protein = weight * 2.2
                carbs = weight * 3.5
                fats = weight * 0.8

            # Display results
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"BMI Results & Recommendations\n")
            result_text.insert(tk.END, "="*40 + "\n\n")
            result_text.insert(tk.END, f"Your BMI: {bmi:.1f}\n")
            result_text.insert(tk.END, f"Category: {category}\n")
            result_text.insert(tk.END, f"Recommended Goal: {recommendation}\n\n")
            
            result_text.insert(tk.END, "Daily Targets:\n")
            result_text.insert(tk.END, f"Maintenance Calories: {tdee:.0f} kcal\n")
            result_text.insert(tk.END, f"Target Calories: {target_calories:.0f} kcal\n")
            result_text.insert(tk.END, f"Protein: {protein:.0f}g\n")
            result_text.insert(tk.END, f"Carbs: {carbs:.0f}g\n")
            result_text.insert(tk.END, f"Fats: {fats:.0f}g\n\n")

            result_text.insert(tk.END, "Training Recommendations:\n")
            result_text.insert(tk.END, f"Suggested Split: {workout_split}\n\n")

            # Goal-specific recommendations
            if recommendation == "BULK":
                result_text.insert(tk.END, """Bulking Guidelines:
• Progressive overload is crucial
• Focus on compound movements
• Aim for 8-12 reps per set
• Rest 2-3 minutes between sets
• Track weight weekly
• Increase calories if not gaining
• Sleep 7-9 hours minimum
• Protein shake post-workout
• Meal timing: Eat every 3-4 hours
""")
            elif recommendation == "CUT":
                result_text.insert(tk.END, """Cutting Guidelines:
• Maintain lifting intensity
• Add 20-30 mins cardio post-workout
• Keep protein high to preserve muscle
• Consider intermittent fasting
• Track measurements weekly
• Drink water before meals
• Focus on food volume
• Get enough sleep
• Plan meals in advance
""")
            else:
                result_text.insert(tk.END, """Recomp Guidelines:
• Focus on progressive overload
• Mix strength and hypertrophy
• Keep protein high
• Stay consistent with diet
• Take progress photos
• Track measurements
• Be patient with changes
• Quality sleep is crucial
""")

        except:
            messagebox.showerror("Error", "Please enter valid numbers")

    # Input fields with better organization
    input_frame = ttk.Frame(bmi_window)
    input_frame.pack(pady=10, padx=20, fill='x')

    # Basic measurements
    ttk.Label(input_frame, text="Basic Measurements", font=('Arial', 11, 'bold')).pack()
    
    ttk.Label(input_frame, text="Weight (kg):").pack()
    entry_weight = ttk.Entry(input_frame)
    entry_weight.pack()

    ttk.Label(input_frame, text="Height (cm):").pack()
    entry_height = ttk.Entry(input_frame)
    entry_height.pack()

    ttk.Label(input_frame, text="Age:").pack()
    entry_age = ttk.Entry(input_frame)
    entry_age.pack()

    # Additional information
    ttk.Label(input_frame, text="\nAdditional Information", font=('Arial', 11, 'bold')).pack()
    
    ttk.Label(input_frame, text="Gender:").pack()
    gender_var = tk.StringVar(value="Male")
    ttk.Radiobutton(input_frame, text="Male", variable=gender_var, value="Male").pack()
    ttk.Radiobutton(input_frame, text="Female", variable=gender_var, value="Female").pack()

    ttk.Label(input_frame, text="Training Experience:").pack()
    experience_var = tk.StringVar(value="Beginner")
    ttk.Radiobutton(input_frame, text="Beginner", variable=experience_var, value="Beginner").pack()
    ttk.Radiobutton(input_frame, text="Intermediate", variable=experience_var, value="Intermediate").pack()
    ttk.Radiobutton(input_frame, text="Advanced", variable=experience_var, value="Advanced").pack()

    ttk.Label(input_frame, text="Activity Level:").pack()
    activity_var = tk.StringVar(value="Moderately Active")
    activities = ["Sedentary", "Light Active", "Moderately Active", "Very Active", "Extra Active"]
    for activity in activities:
        ttk.Radiobutton(input_frame, text=activity, variable=activity_var, value=activity).pack()

    ttk.Label(input_frame, text="Current Body Type:").pack()
    body_type_var = tk.StringVar(value="Normal")
    ttk.Radiobutton(input_frame, text="Normal", variable=body_type_var, value="Normal").pack()
    ttk.Radiobutton(input_frame, text="Skinny Fat", variable=body_type_var, value="Skinny Fat").pack()

    # Calculate button
    ttk.Button(input_frame, text="Calculate & Get Recommendations", 
              command=calculate_and_recommend).pack(pady=10)

    # Results area
    result_text = tk.Text(bmi_window, height=20, width=50)
    result_text.pack(pady=10, padx=10)

    # Add scrollbar to results
    scrollbar = ttk.Scrollbar(bmi_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_text.yview)

# Add this function for statistics and graphs
def view_statistics():
    stats_window = tk.Toplevel()
    stats_window.title("Fitness Statistics")
    stats_window.geometry("800x600")

    def generate_stats():
        start_date = entry_start.get()
        end_date = entry_end.get()
        
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()

        # Create figure with subplots
        fig = Figure(figsize=(10, 8))
        fig.subplots_adjust(hspace=0.5)

        # Steps graph
        cursor.execute("""
        SELECT date, steps FROM step_counter 
        WHERE date BETWEEN ? AND ?
        ORDER BY date""", (start_date, end_date))
        steps_data = cursor.fetchall()
        
        if steps_data:
            ax1 = fig.add_subplot(311)
            dates = [row[0] for row in steps_data]
            steps = [row[1] for row in steps_data]
            ax1.plot(dates, steps, 'b-o')
            ax1.set_title('Daily Steps')
            ax1.tick_params(axis='x', rotation=45)

        # Calories graph
        cursor.execute("""
        SELECT date, SUM(calories) 
        FROM nutrition 
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date""", (start_date, end_date))
        calories_data = cursor.fetchall()
        
        if calories_data:
            ax2 = fig.add_subplot(312)
            dates = [row[0] for row in calories_data]
            calories = [row[1] for row in calories_data]
            ax2.bar(dates, calories, color='g', alpha=0.7)
            ax2.set_title('Daily Calories')
            ax2.tick_params(axis='x', rotation=45)

        # Water consumption graph
        cursor.execute("""
        SELECT date, water_consumed 
        FROM hydration 
        WHERE date BETWEEN ? AND ?
        ORDER BY date""", (start_date, end_date))
        water_data = cursor.fetchall()
        
        if water_data:
            ax3 = fig.add_subplot(313)
            dates = [row[0] for row in water_data]
            water = [row[1] for row in water_data]
            ax3.plot(dates, water, 'r-o')
            ax3.set_title('Daily Water Consumption (L)')
            ax3.tick_params(axis='x', rotation=45)

        # Create canvas and show plot
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        conn.close()

    # Date range inputs
    frame_dates = tk.Frame(stats_window)
    frame_dates.pack(pady=10)

    tk.Label(frame_dates, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
    entry_start = tk.Entry(frame_dates)
    entry_start.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_dates, text="End Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
    entry_end = tk.Entry(frame_dates)
    entry_end.pack(side=tk.LEFT, padx=5)

    # Set default date range (last 7 days)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    entry_start.insert(0, week_ago.strftime('%Y-%m-%d'))
    entry_end.insert(0, today.strftime('%Y-%m-%d'))

    tk.Button(stats_window, text="Generate Statistics", 
              command=generate_stats,
              bg="#DDA0DD").pack(pady=10)

# Add this function for weekly planning
def weekly_planner():
    planner_window = tk.Toplevel()
    planner_window.title("Weekly Workout Planner")
    planner_window.geometry("400x500")

    def save_plan():
        plan = ""
        for day, entry in day_entries.items():
            plan += f"{day}: {entry.get()}\n"
        messagebox.showinfo("Weekly Plan", f"Your Weekly Plan:\n\n{plan}")

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_entries = {}

    # Example workouts for different days
    example_workouts = [
        "Cardio: 30min running + core exercises",
        "Upper body: chest, shoulders, triceps",
        "Rest day + light stretching",
        "Lower body: squats, lunges, calves",
        "Cardio: 30min cycling + HIIT",
        "Full body workout + abs",
        "Active recovery: yoga/walking"
    ]

    tk.Label(planner_window, text="Weekly Workout Plan", 
             font=("Arial", 12, "bold")).pack(pady=10)

    for i, day in enumerate(days):
        frame = tk.Frame(planner_window)
        frame.pack(pady=5)
        tk.Label(frame, text=f"{day}:").pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, width=30)
        entry.insert(0, example_workouts[i])
        entry.pack(side=tk.LEFT, padx=5)
        day_entries[day] = entry

    tk.Button(planner_window, text="Save Weekly Plan", 
              command=save_plan,
              bg="#98FB98").pack(pady=20)

# Add this new class for handling subscriptions
class SubscriptionManager:
    def __init__(self):
        self.plans = [
            {
                'name': 'Beginner Package',
                'description': 'Perfect for fitness newcomers',
                'duration': '3 months',
                'price': 4999,  # ₹4,999
                'features': [
                    'Basic workout plans',
                    'Indian diet guidelines',
                    'WhatsApp support',
                    'Yoga basics',
                    'Daily exercise reminders'
                ]
            },
            {
                'name': 'Intermediate Package',
                'description': 'For regular gym-goers',
                'duration': '6 months',
                'price': 8999,  # ₹8,999
                'features': [
                    'Customized workout plans',
                    'Personalized Indian diet plans',
                    'Weekly WhatsApp check-ins',
                    'Video guides',
                    'Advanced yoga sessions',
                    'Festival-special diet plans'
                ]
            },
            {
                'name': 'Pro Package',
                'description': 'For serious fitness enthusiasts',
                'duration': '12 months',
                'price': 14999,  # ₹14,999
                'features': [
                    'Personal training sessions',
                    'Custom meal plans (veg & non-veg)',
                    '24/7 WhatsApp support',
                    'Progress tracking',
                    'Video consultations',
                    'Premium yoga classes',
                    'Seasonal diet adjustments',
                    'Family diet recommendations'
                ]
            }
        ]

    def show_plans_window(self):
        plans_window = tk.Toplevel()
        plans_window.title("Fitness Plans")
        plans_window.geometry("800x600")

        # Create notebook for tabbed interface
        notebook = ttk.Notebook(plans_window)
        notebook.pack(pady=10, expand=True)

        # Create a tab for each plan
        for plan in self.plans:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=plan['name'])

            # Plan details
            tk.Label(frame, text=plan['description'], font=('Arial', 12)).pack(pady=10)
            tk.Label(frame, text=f"Duration: {plan['duration']}", font=('Arial', 10)).pack()
            tk.Label(frame, text=f"Price: ₹{plan['price']:,}", font=('Arial', 14, 'bold')).pack(pady=10)

            # EMI Option
            monthly_emi = plan['price'] / 3  # 3-month EMI option
            tk.Label(frame, text=f"EMI Available: ₹{monthly_emi:,.2f}/month", 
                    font=('Arial', 10, 'italic')).pack()

            # Features
            tk.Label(frame, text="Features:", font=('Arial', 11, 'bold')).pack(pady=5)
            for feature in plan['features']:
                tk.Label(frame, text=f"✓ {feature}", font=('Arial', 10)).pack()

            # Subscribe button
            tk.Button(frame, text="Subscribe Now", 
                     command=lambda p=plan: self.show_payment_window(p),
                     bg="#90EE90", font=('Arial', 11, 'bold')).pack(pady=20)

    def show_payment_window(self, plan):
        payment_window = tk.Toplevel()
        payment_window.title("Subscribe to " + plan['name'])
        payment_window.geometry("400x600")

        # Payment form
        tk.Label(payment_window, text="Payment Details", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(payment_window, text="Email:").pack()
        email_entry = tk.Entry(payment_window, width=40)
        email_entry.pack(pady=5)

        tk.Label(payment_window, text="Mobile Number:").pack()
        mobile_entry = tk.Entry(payment_window, width=40)
        mobile_entry.pack(pady=5)

        # Payment method selection
        tk.Label(payment_window, text="Select Payment Method:", font=('Arial', 11, 'bold')).pack(pady=10)
        payment_method = tk.StringVar(value="upi")
        
        tk.Radiobutton(payment_window, text="UPI", variable=payment_method, 
                      value="upi").pack()
        tk.Radiobutton(payment_window, text="Card", variable=payment_method, 
                      value="card").pack()
        tk.Radiobutton(payment_window, text="Net Banking", variable=payment_method, 
                      value="netbanking").pack()
        tk.Radiobutton(payment_window, text="EMI (3 months)", variable=payment_method, 
                      value="emi").pack()

        # Card details frame (initially hidden)
        card_frame = tk.Frame(payment_window)
        def show_card_details():
            if payment_method.get() == "card":
                card_frame.pack(pady=10)
            else:
                card_frame.pack_forget()

        payment_method.trace('w', lambda *args: show_card_details())

        tk.Label(card_frame, text="Card Number:").pack()
        card_entry = tk.Entry(card_frame, width=40)
        card_entry.pack(pady=5)

        # Expiry and CVV in same row
        frame_card = tk.Frame(card_frame)
        frame_card.pack(pady=5)

        tk.Label(frame_card, text="Expiry (MM/YY):").pack(side=tk.LEFT, padx=5)
        expiry_entry = tk.Entry(frame_card, width=10)
        expiry_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_card, text="CVV:").pack(side=tk.LEFT, padx=5)
        cvv_entry = tk.Entry(frame_card, width=5)
        cvv_entry.pack(side=tk.LEFT, padx=5)

        # Order summary
        tk.Label(payment_window, text="Order Summary", font=('Arial', 12, 'bold')).pack(pady=20)
        tk.Label(payment_window, text=f"Plan: {plan['name']}").pack()
        tk.Label(payment_window, text=f"Duration: {plan['duration']}").pack()
        tk.Label(payment_window, text=f"Total: ₹{plan['price']:,}", 
                font=('Arial', 12, 'bold')).pack(pady=5)
        
        # GST info
        gst = plan['price'] * 0.18
        total_with_gst = plan['price'] + gst
        tk.Label(payment_window, text=f"GST (18%): ₹{gst:,.2f}").pack()
        tk.Label(payment_window, text=f"Final Amount: ₹{total_with_gst:,.2f}", 
                font=('Arial', 12, 'bold')).pack(pady=10)

        def process_payment():
            # In a real application, you would process the payment here
            messagebox.showinfo("Success", 
                              f"Thank you for subscribing to {plan['name']}!\n\n"
                              "Your payment has been processed successfully.\n"
                              "You will receive a WhatsApp message with further instructions.")
            payment_window.destroy()

        tk.Button(payment_window, text="Complete Payment", 
                 command=process_payment,
                 bg="#90EE90", font=('Arial', 10, 'bold')).pack(pady=20)

class WorkoutLibrary:
    def __init__(self):
        self.exercises = {
            'Beginner': {
                'Surya Namaskar': {
                    'description': 'Traditional yoga sequence with 12 poses',
                    'tutorial': 'surya+namaskar+for+beginners'
                },
                'Jumping Jacks': {
                    'description': 'Basic cardio exercise',
                    'tutorial': 'proper+jumping+jacks+form'
                },
                'Body Weight Squats': {
                    'description': 'Lower body strengthening',
                    'tutorial': 'how+to+do+bodyweight+squats+properly'
                },
                'Modified Push-ups': {
                    'description': 'Upper body exercise for beginners',
                    'tutorial': 'knee+pushups+proper+form'
                },
                'Walking': {
                    'description': '30-minute brisk walking',
                    'tutorial': 'proper+walking+form+fitness'
                }
            },
            'Intermediate': {
                'Power Yoga': {
                    'description': 'Advanced yoga poses with flow',
                    'tutorial': 'power+yoga+intermediate+workout'
                },
                'HIIT Circuit': {
                    'description': '20-min high intensity interval training',
                    'tutorial': 'HIIT+workout+intermediate+level'
                },
                'Strength Training': {
                    'description': 'Dumbbell exercises for full body',
                    'tutorial': 'dumbbell+full+body+workout'
                },
                'Core Workout': {
                    'description': 'Planks and ab exercises',
                    'tutorial': 'intermediate+core+workout'
                },
                'Running': {
                    'description': '5km running program',
                    'tutorial': '5k+running+training+plan'
                }
            },
            'Advanced': {
                'CrossFit WOD': {
                    'description': 'Workout of the day',
                    'tutorial': 'crossfit+workout+advanced'
                },
                'Advanced Yoga': {
                    'description': 'Complex asanas and meditation',
                    'tutorial': 'advanced+yoga+poses'
                },
                'Strength Program': {
                    'description': 'Heavy lifting routine',
                    'tutorial': 'advanced+strength+training+program'
                },
                'Marathon Training': {
                    'description': 'Long distance running plan',
                    'tutorial': 'marathon+training+guide'
                },
                'Sports Specific': {
                    'description': 'Sport-focused training',
                    'tutorial': 'sports+specific+training+advanced'
                }
            }
        }

    def show_library(self):
        library_window = tk.Toplevel()
        library_window.title("Workout Library")
        library_window.geometry("700x500")

        notebook = ttk.Notebook(library_window)
        notebook.pack(pady=10, expand=True, fill='both')

        for level, exercises in self.exercises.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=level)

            for exercise, details in exercises.items():
                exercise_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1)
                exercise_frame.pack(fill='x', padx=5, pady=5)

                tk.Label(exercise_frame, text=exercise, 
                        font=('Arial', 11, 'bold')).pack(anchor='w')
                tk.Label(exercise_frame, text=details['description'], 
                        wraplength=500).pack(anchor='w', padx=20)
                
                # Add tutorial button that opens YouTube
                tk.Button(exercise_frame, text="Watch Tutorial", 
                         command=lambda q=details['tutorial']: open_youtube_link(q),
                         bg="#FF0000", fg="white").pack(pady=5)  # YouTube colors

class DietPlanner:
    def __init__(self):
        self.meal_suggestions = {
            'Bulk': {
                'Vegetarian': {
                    'Breakfast': ['Oats with banana, nuts and protein shake', 'Paneer paratha with curd', 'Protein smoothie with dry fruits', 'Masala dosa with potato and chutney', 'Chickpea pancakes with protein shake'],
                    'Lunch': ['Rice with dal makhani and paneer', 'Quinoa pulao with rajma', 'Chole bhature with raita', 'Veg biryani with soya chunks', 'Rice with kadai paneer'],
                    'Dinner': ['Roti with paneer butter masala', 'Mixed dal khichdi with ghee', 'Protein pasta with cheese sauce', 'Veg pulao with paneer tikka', 'Multigrain roti with dal fry'],
                    'Snacks': ['Protein shake with nuts', 'Peanut butter sandwich', 'Greek yogurt with fruits', 'Mixed dry fruits', 'Protein bar']
                },
                'Non-Vegetarian': {
                    'Breakfast': ['6 egg whites + 2 whole eggs with toast', 'Chicken sandwich with protein shake', 'Egg bhurji with paratha', 'Protein smoothie with banana', 'Chicken keema paratha'],
                    'Lunch': ['Chicken biryani with raita', 'Fish curry with rice', 'Mutton curry with roti', 'Egg curry with rice', 'Chicken rice bowl'],
                    'Dinner': ['Grilled chicken with roti', 'Fish tikka with mint chutney', 'Egg curry with paratha', 'Chicken curry with rice', 'Turkey kebabs with hummus'],
                    'Snacks': ['Protein shake', 'Boiled eggs', 'Chicken sandwich', 'Protein bar', 'Mixed nuts']
                }
            },
            'Cut': {
                'Vegetarian': {
                    'Breakfast': ['Sprouts salad with protein shake', 'Besan chilla with mint chutney', 'Vegetable upma with protein shake', 'Moong dal cheela', 'Protein smoothie with berries'],
                    'Lunch': ['Quinoa with mixed vegetables', 'Brown rice with dal', 'Roti with mixed veg curry', 'Keto cauliflower rice', 'Salad with tofu'],
                    'Dinner': ['Mixed vegetable soup', 'Grilled paneer salad', 'Roti with dal and vegetables', 'Tofu stir fry', 'Protein-rich salad'],
                    'Snacks': ['Green tea', 'Cucumber slices', 'Roasted chickpeas', 'Protein shake', 'Mixed seeds']
                },
                'Non-Vegetarian': {
                    'Breakfast': ['Egg white omelette', 'Protein smoothie', 'Boiled eggs with toast', 'Grilled chicken breast', 'Fish fillet'],
                    'Lunch': ['Grilled chicken salad', 'Tuna with quinoa', 'Chicken breast with vegetables', 'Fish with brown rice', 'Turkey wrap'],
                    'Dinner': ['Baked fish with vegetables', 'Chicken soup', 'Egg white curry', 'Grilled chicken breast', 'Protein salad'],
                    'Snacks': ['Protein shake', 'Boiled eggs', 'Grilled chicken strips', 'Sugar-free yogurt', 'Mixed seeds']
                }
            },
            'Maintain': {
                'Vegetarian': {
                    'Breakfast': ['Oats with fruits', 'Idli sambar', 'Poha', 'Besan chilla', 'Upma'],
                    'Lunch': ['Dal rice with vegetables', 'Roti sabzi', 'Pulao', 'Khichdi', 'Curd rice'],
                    'Dinner': ['Multigrain roti with dal', 'Vegetable soup', 'Quinoa bowl', 'Salad', 'Mixed veg curry'],
                    'Snacks': ['Fruits', 'Nuts', 'Roasted chana', 'Yogurt', 'Sprouts']
                },
                'Non-Vegetarian': {
                    'Breakfast': ['Egg bhurji', 'Chicken sandwich', 'Protein smoothie', 'Omelette', 'Fish curry'],
                    'Lunch': ['Chicken rice bowl', 'Fish curry', 'Grilled chicken salad', 'Egg curry', 'Mutton curry'],
                    'Dinner': ['Grilled fish', 'Chicken stir fry', 'Turkey wrap', 'Protein bowl', 'Egg bhurji'],
                    'Snacks': ['Boiled eggs', 'Chicken strips', 'Protein bar', 'Mixed nuts', 'Greek yogurt']
                }
            }
        }

        # Add YouTube tutorial links for each goal
        self.tutorial_links = {
            'Bulk': {
                'Meal Prep': 'bulking+meal+prep+guide',
                'Protein Foods': 'high+protein+indian+foods',
                'Mass Gaining': 'how+to+gain+weight+healthy',
                'Supplement Guide': 'supplements+for+bulking'
            },
            'Cut': {
                'Meal Prep': 'cutting+diet+meal+prep',
                'Low Calorie': 'low+calorie+indian+meals',
                'Fat Loss': 'healthy+fat+loss+diet',
                'Portion Control': 'portion+control+guide'
            },
            'Maintain': {
                'Balanced Diet': 'balanced+diet+plan+indian',
                'Healthy Cooking': 'healthy+cooking+methods',
                'Meal Timing': 'meal+timing+for+fitness',
                'Nutrition Basics': 'basic+nutrition+guide'
            }
        }

    def show_diet_planner(self):
        diet_window = tk.Toplevel()
        diet_window.title("BMI-Based Diet Planner")
        diet_window.geometry("700x800")

        def calculate_and_plan():
            try:
                weight = float(weight_entry.get())
                height = float(height_entry.get()) / 100  # convert cm to meters
                age = int(age_entry.get())
                gender = gender_var.get()
                activity = activity_var.get()
                diet_type = diet_var.get()

                # Calculate BMI
                bmi = weight / (height * height)

                # Determine goal based on BMI
                if bmi < 18.5:
                    goal = "Bulk"
                    color = "#FFB6C1"  # Light red
                elif bmi >= 25:
                    goal = "Cut"
                    color = "#FFA500"  # Orange
                else:
                    goal = "Maintain"
                    color = "#98FB98"  # Light green

                # Calculate TDEE
                if gender == "Male":
                    bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
                else:
                    bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161

                activity_multipliers = {
                    "Sedentary": 1.2,
                    "Light Active": 1.375,
                    "Moderately Active": 1.55,
                    "Very Active": 1.725,
                    "Extra Active": 1.9
                }
                
                tdee = bmr * activity_multipliers[activity]

                # Adjust calories based on goal
                if goal == "Bulk":
                    target_calories = tdee + 500
                    protein = weight * 2.2  # g/kg
                    carbs = weight * 4    # g/kg
                    fats = weight * 0.9   # g/kg
                elif goal == "Cut":
                    target_calories = tdee - 500
                    protein = weight * 2.5
                    carbs = weight * 2
                    fats = weight * 0.7
                else:
                    target_calories = tdee
                    protein = weight * 2
                    carbs = weight * 3
                    fats = weight * 0.8

                # Display results and meal plan
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"BMI Analysis and Meal Plan\n")
                result_text.insert(tk.END, "="*40 + "\n\n")
                result_text.insert(tk.END, f"Your BMI: {bmi:.1f}\n")
                result_text.insert(tk.END, f"Recommended Goal: {goal}\n")
                result_text.insert(tk.END, f"Daily Calories: {target_calories:.0f} kcal\n")
                result_text.insert(tk.END, f"Protein: {protein:.0f}g\n")
                result_text.insert(tk.END, f"Carbs: {carbs:.0f}g\n")
                result_text.insert(tk.END, f"Fats: {fats:.0f}g\n\n")

                result_text.insert(tk.END, "7-Day Meal Plan:\n\n")
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                
                for day in days:
                    result_text.insert(tk.END, f"\n{day}:\n")
                    for meal in ['Breakfast', 'Lunch', 'Dinner', 'Snacks']:
                        meal_choice = random.choice(self.meal_suggestions[goal][diet_type][meal])
                        result_text.insert(tk.END, f"{meal}: {meal_choice}\n")

                # Add nutrition tips based on goal
                result_text.insert(tk.END, f"\nNutrition Tips for {goal}:\n")
                if goal == "Bulk":
                    result_text.insert(tk.END, """
• Eat every 2-3 hours
• Include protein with every meal
• Focus on calorie-dense foods
• Drink calories (smoothies, shakes)
• Eat before bed
• Track your progress weekly
""")
                elif goal == "Cut":
                    result_text.insert(tk.END, """
• High protein to preserve muscle
• Focus on fiber-rich foods
• Drink water before meals
• Use smaller plates
• Avoid liquid calories
• Plan meals in advance
""")
                else:
                    result_text.insert(tk.END, """
• Balance your macros
• Eat mindfully
• Stay hydrated
• Regular meal timing
• Monitor portion sizes
""")

                # Add tutorial buttons based on goal
                def add_tutorial_buttons(goal):
                    tutorial_frame = ttk.Frame(diet_window)
                    tutorial_frame.pack(pady=10)
                    
                    ttk.Label(tutorial_frame, text="Helpful Tutorials:", 
                             font=('Arial', 11, 'bold')).pack()
                    
                    for topic, search_query in self.tutorial_links[goal].items():
                        ttk.Button(tutorial_frame, text=f"Watch {topic} Guide",
                                  command=lambda q=search_query: open_youtube_link(q)).pack(pady=2)

                add_tutorial_buttons(goal)

            except:
                messagebox.showerror("Error", "Please enter valid numbers")

        # Input fields
        input_frame = ttk.Frame(diet_window)
        input_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(input_frame, text="Enter Your Details", font=('Arial', 12, 'bold')).pack()

        ttk.Label(input_frame, text="Weight (kg):").pack()
        weight_entry = ttk.Entry(input_frame)
        weight_entry.pack()

        ttk.Label(input_frame, text="Height (cm):").pack()
        height_entry = ttk.Entry(input_frame)
        height_entry.pack()

        ttk.Label(input_frame, text="Age:").pack()
        age_entry = ttk.Entry(input_frame)
        age_entry.pack()

        ttk.Label(input_frame, text="Gender:").pack()
        gender_var = tk.StringVar(value="Male")
        ttk.Radiobutton(input_frame, text="Male", variable=gender_var, value="Male").pack()
        ttk.Radiobutton(input_frame, text="Female", variable=gender_var, value="Female").pack()

        ttk.Label(input_frame, text="Activity Level:").pack()
        activity_var = tk.StringVar(value="Moderately Active")
        activities = ["Sedentary", "Light Active", "Moderately Active", "Very Active", "Extra Active"]
        for activity in activities:
            ttk.Radiobutton(input_frame, text=activity, variable=activity_var, value=activity).pack()

        ttk.Label(input_frame, text="Diet Type:").pack()
        diet_var = tk.StringVar(value="Vegetarian")
        ttk.Radiobutton(input_frame, text="Vegetarian", variable=diet_var, value="Vegetarian").pack()
        ttk.Radiobutton(input_frame, text="Non-Vegetarian", variable=diet_var, value="Non-Vegetarian").pack()

        ttk.Button(input_frame, text="Generate Diet Plan", 
                  command=calculate_and_plan).pack(pady=20)

        # Results area
        result_text = tk.Text(diet_window, height=30, width=60)
        result_text.pack(pady=10, padx=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(diet_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=result_text.yview)

def export_progress():
    def export():
        start_date = start_entry.get()
        end_date = end_entry.get()
        
        conn = sqlite3.connect("fitness_tracker.db")
        cursor = conn.cursor()
        
        # Fetch all data
        data = {
            'steps': {},
            'workouts': {},
            'nutrition': {},
            'hydration': {}
        }
        
        # Get steps data
        cursor.execute("SELECT * FROM step_counter WHERE date BETWEEN ? AND ?", 
                      (start_date, end_date))
        for row in cursor.fetchall():
            data['steps'][row[0]] = {'steps': row[1], 'distance': row[2]}
            
        # Get other data similarly...
        
        # Export to CSV
        filename = f"fitness_progress_{start_date}_to_{end_date}.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Steps', 'Distance', 'Calories', 'Water'])
            
            current = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            while current <= end:
                date_str = current.strftime('%Y-%m-%d')
                steps_data = data['steps'].get(date_str, {'steps': 0, 'distance': 0})
                
                writer.writerow([
                    date_str,
                    steps_data['steps'],
                    steps_data['distance'],
                    # Add other data here
                ])
                
                current += timedelta(days=1)
        
        messagebox.showinfo("Success", f"Data exported to {filename}")
        export_window.destroy()

    export_window = tk.Toplevel()
    export_window.title("Export Progress")
    export_window.geometry("400x200")

    tk.Label(export_window, text="Export Data", font=('Arial', 12, 'bold')).pack(pady=10)

    tk.Label(export_window, text="Start Date (YYYY-MM-DD):").pack()
    start_entry = tk.Entry(export_window)
    start_entry.pack()

    tk.Label(export_window, text="End Date (YYYY-MM-DD):").pack()
    end_entry = tk.Entry(export_window)
    end_entry.pack()

    tk.Button(export_window, text="Export to CSV", 
              command=export,
              bg="#ADD8E6").pack(pady=20)

# Add this function at the top level
def open_youtube_link(search_query):
    # Format the search query for URL
    formatted_query = search_query.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={formatted_query}"
    webbrowser.open(url)

# Modify main_app to include new features
def main_app():
    initialize_database()
    root = tk.Tk()
    root.title("Fitness Tracker")
    root.geometry("300x700")  # Made taller to accommodate new buttons
    
    subscription_manager = SubscriptionManager()
    workout_library = WorkoutLibrary()
    diet_planner = DietPlanner()
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)
    
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Add all buttons to scrollable_frame instead of root
    tk.Button(scrollable_frame, text="Set Daily Goals", command=manage_goals, 
             bg="#90EE90", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Button(scrollable_frame, text="Log Steps", command=log_steps).pack(pady=5)
    tk.Button(scrollable_frame, text="Log Workout", command=log_workout).pack(pady=5)
    tk.Button(scrollable_frame, text="Log Nutrition", command=log_nutrition).pack(pady=5)
    tk.Button(scrollable_frame, text="Log Hydration", command=log_hydration).pack(pady=5)
    
    # Add new feature buttons
    tk.Button(scrollable_frame, text="View Progress", command=view_progress,
             bg="#ADD8E6", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Button(scrollable_frame, text="View Fitness Plans", 
             command=subscription_manager.show_plans_window,
             bg="#FFB6C1", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Button(scrollable_frame, text="Workout Library", 
             command=workout_library.show_library,
             bg="#DDA0DD", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Button(scrollable_frame, text="Diet Planner", 
             command=diet_planner.show_diet_planner,
             bg="#98FB98", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Button(scrollable_frame, text="Export Progress", 
             command=export_progress,
             bg="#F0E68C", font=("Arial", 10, "bold")).pack(pady=5)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main_app()
