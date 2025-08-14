import subprocess
from config import OLLAMA_MODEL, GOAL_MAP
from exercise_api import fetch_exercises_for_goal

exercise_cache = {}

def generate_simple_template(goal, duration_type, duration_value, exercises):
   
    exercise_list = exercises['name'].head(6).tolist()
    
    if duration_type == "days":
        return generate_daily_plan(goal, duration_value, exercise_list)
    else:
        return generate_weekly_plan(goal, duration_value, exercise_list)

def generate_daily_plan(goal, days, exercise_list):
    # plan for X days
    plan = f"# {days}-Day {goal.title()} Workout Plan\n\n"
    
    for day in range(1, days + 1):
        plan += f"## Day {day}\n\n"
        
        if goal == "strength":
            # rotate exercises
            day_exercises = exercise_list[:3]  # 3 exercises per day
            for i, exercise in enumerate(day_exercises):
                sets = 3 if i < 2 else 2
                reps = "8-10" if i < 2 else "12-15"
                plan += f"- {exercise}: {sets} sets × {reps} reps\n"
            plan += "- Rest: 60-90 seconds between sets\n\n"
        
        elif goal == "cardio":
            # cardio routine
            exercise = exercise_list[day % len(exercise_list)]
            duration = 20 + (day * 2)  
            plan += f"- {exercise}: {duration} minutes\n"
            plan += f"- Intensity: Moderate to High\n\n"
        
        elif goal == "flexibility":
            # Flexibility 
            for exercise in exercise_list[:4]:
                plan += f"- {exercise}: Hold for 30-45 seconds\n"
            plan += "- Repeat circuit 2-3 times\n\n"
    
    return plan

def generate_weekly_plan(goal, weeks, exercise_list):
    """Generate a plan for X weeks"""
    plan = f"# {weeks}-Week {goal.title()} Workout Plan\n\n"
    
    for week in range(1, weeks + 1):
        plan += f"## Week {week}\n\n"
        
        if goal == "strength":
            plan += "**Schedule: 3 days per week**\n\n"
            for day in ["Monday", "Wednesday", "Friday"]:
                plan += f"**{day}:**\n"
                for i, exercise in enumerate(exercise_list[:4]):
                    sets = 3 + (week - 1) // 2  # progressive overload
                    reps = "6-8" if i < 2 else "10-12"
                    plan += f"- {exercise}: {sets} sets × {reps} reps\n"
                plan += "\n"
        
        elif goal == "cardio":
            plan += "**Schedule: 4 days per week**\n\n"
            for day, exercise in zip(["Mon", "Tue", "Thu", "Fri"], exercise_list[:4]):
                duration = 25 + (week * 5)
                plan += f"**{day}:** {exercise} - {duration} minutes\n"
            plan += "\n"
        
        elif goal == "flexibility":
            plan += "**Schedule: Daily (7 days)**\n\n"
            for exercise in exercise_list[:5]:
                duration = 30 + (week * 5)
                plan += f"- {exercise}: {duration} seconds × 3 sets\n"
            plan += "\n"
    
    return plan

def generate_workout_plan(goal, duration_type="days", duration_value=3):
    global exercise_cache
    
    if goal not in exercise_cache:
        exercise_df = fetch_exercises_for_goal(goal)
        if exercise_df.empty:
            return f"No exercises available for {goal}."
        exercise_cache[goal] = exercise_df
    else:
        exercise_df = exercise_cache[goal]
    

    exercise_list = exercise_df['name'].head(4).tolist()
    
    if duration_type == "days":
        prompt = f"{duration_value} day {goal} plan: {', '.join(exercise_list)}. Brief format."
    else:
        prompt = f"{duration_value} week {goal} plan: {', '.join(exercise_list)}. Brief format."
    
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=45  # Shorter timeout
        )
        
        if result.returncode == 0 and len(result.stdout.strip()) > 100:
            return result.stdout.strip()
        else:
            # Use fast template fallback
            return generate_simple_template(goal, duration_type, duration_value, exercise_df)
            
    except:
        return generate_simple_template(goal, duration_type, duration_value, exercise_df)