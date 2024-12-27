# Fitness Tracker Application
A comprehensive desktop application built with Python and Tkinter for tracking fitness goals, nutrition, and workout progress with BMI-based recommendations.
## Features
## 1. Daily Tracking
- *Steps Counter*: Log daily steps and view distance covered
- *Workout Logger*: Track exercises, sets, reps, and weights
- *Nutrition Tracker*: Monitor food intake and calories
- *Hydration Tracker*: Track daily water consumption
## 2. BMI Calculator & Recommendations
- Calculates BMI based on height and weight
- Provides personalized recommendations:
  - Bulk (BMI < 18.5)
  - Maintain (BMI 18.5-24.9)
  - Cut (BMI ≥ 25)
- Activity level considerations:
  - Sedentary (1.2): Little/no exercise
  - Light Active (1.375): Light exercise 1-3 days/week
  - Moderately Active (1.55): Moderate exercise 3-5 days/week
  - Very Active (1.725): Heavy exercise 6-7 days/week
  - Extra Active (1.9): Very heavy exercise/training 2x/day
## 3. Diet Planner
- Customized meal plans based on:
  - BMI category
  - Dietary preference (Vegetarian/Non-Vegetarian)
  - Caloric needs
  - Fitness goals
- Includes:
  - Breakfast suggestions
  - Lunch options
  - Dinner recommendations
  - Healthy snacks
## 4. Workout Library
- Categorized exercises:
  - Beginner
  - Intermediate
  - Advanced
- Video tutorials via YouTube integration
- Detailed exercise descriptions
- Form guidance
## 5. Progress Tracking
- Visual progress reports
- Data export functionality
- Goal setting and monitoring
- Progress visualization
## Installation
1. Clone the repository:
git clone [repository-url]
2.Install required packages:
pip install -r requirements.txt
3.Run the application:
python tracker.py
## Requirements
- Python 3.x
- tkinter
- sqlite3
- matplotlib
- pandas
- PIL (Pillow)

## Usage

1. *Initial Setup*:
   - Launch the application
   - Enter your basic details (height, weight, age)
   - Select your activity level
   - Choose dietary preferences

2. *Daily Tracking*:
   - Log your daily activities
   - Track meals and water intake
   - Record workouts

3. *View Progress*:
   - Check daily/weekly reports
   - Monitor goal achievement
   - Export data for analysis

4. *Get Recommendations*:
   - BMI-based workout plans
   - Customized diet suggestions
   - Exercise tutorials
## Database Structure
The application uses SQLite with the following tables:
- step_counter
- workout_log
- nutrition## Acknowledgments

- Exercise tutorials linked to YouTube
- BMI calculations based on WHO standards
- Nutrition recommendations following standard dietary guidelines
## Future Enhancements
- User authentication system
- Cloud data synchronization
- Mobile application integration
- Social features for community engagement
- Advanced analytics and reporting
- hydration
- daily_goals
## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
