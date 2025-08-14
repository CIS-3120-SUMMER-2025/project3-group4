import requests
import pandas as pd
from config import NINJA_API_TOKEN, GOAL_MAP

API_URL = "https://api.api-ninjas.com/v1/exercises"
LIMIT = 50
# MAX_PAGES = 5

def fetch_exercises_for_goal(goal, limit_per_type=8):
    headers = {"X-Api-Key": NINJA_API_TOKEN}
    
    # types we need for this goal
    needed_types = GOAL_MAP.get(goal.lower(), [])
    if not needed_types:
        return pd.DataFrame()
    
    all_exercises = []
    
    for exercise_type in needed_types:
        try:
            params = {"type": exercise_type, "limit": limit_per_type}
            resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            for ex in data:
                ex["goal_type"] = ex["type"].lower().strip()
            
            all_exercises.extend(data)
            print(f"Fetched {len(data)} {exercise_type} exercises")
            
        except Exception as e:
            print(f"Error fetching {exercise_type}: {e}")
            continue
    
    if all_exercises:
        df = pd.DataFrame(all_exercises)
        print(f"Total exercises for {goal}: {len(df)}")
        return df
    else:
        return pd.DataFrame()