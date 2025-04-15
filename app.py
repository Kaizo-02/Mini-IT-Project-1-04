from models import add_goal, add_habit, get_goals_by_user, get_habits_by_user
import time

def add_new_goal():
    print("Welcome to the Goal Planner!")
    goal_name = input("Enter the goal name: ")
    goal_description = input("Enter the goal description: ")
    goal_due_date = input("Enter the goal due date (YYYY-MM-DD): ")
    goal_priority = input("Enter the goal priority (Prioritize/To Do/Less Important/Not Important): ")
    user_id = 1  # assuming user ID is 1 for simplicity
    add_goal(user_id, goal_name, goal_description, goal_due_date, goal_priority)
    print("Goal added successfully!")

def add_new_habit():
    print("Welcome to the Habit Builder!")
    habit_name = input("Enter the habit name (e.g., Exercise, Read): ")
    habit_description = input("Enter the habit description: ")
    habit_frequency = input("Enter the habit frequency (Daily/Weekly/Monthly): ")
    user_id = 1  # assuming user ID is 1 for simplicity
    add_habit(user_id, habit_name, habit_description, habit_frequency)
    print("Habit added successfully!")

def pomodoro_timer():
    print("Starting Pomodoro Timer (25 minutes work, 5 minutes break)")

    for i in range(4):  # 4 Pomodoro sessions
        print(f"Pomodoro #{i+1}: Work for 25 minutes!")
        time.sleep(25 * 60)  # 25 minutes of work
        print(f"Pomodoro #{i+1}: Take a 5-minute break!")
        time.sleep(5 * 60)  # 5-minute break

    print("Pomodoro session completed! Great job!")

def view_goals():
    user_id = 1  # assuming user ID is 1 for simplicity
    goals = get_goals_by_user(user_id)
    print("\nYour Goals:")
    for goal in goals:
        print(f"Goal Name: {goal[2]}, Description: {goal[3]}, Due Date: {goal[4]}, Priority: {goal[5]}")
    print("\n")

def view_habits():
    user_id = 1  # assuming user ID is 1 for simplicity
    habits = get_habits_by_user(user_id)
    print("\nYour Habits:")
    for habit in habits:
        print(f"Habit Name: {habit[2]}, Description: {habit[3]}, Frequency: {habit[4]}")
    print("\n")

def main():
    print("Welcome to the Self-Improvement App!")
    print("Choose an option:")
    print("1. Add a new goal")
    print("2. Add a new habit")
    print("3. Start Pomodoro Timer")
    print("4. View all goals")
    print("5. View all habits")

    choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

    if choice == '1':
        add_new_goal()
    elif choice == '2':
        add_new_habit()
    elif choice == '3':
        pomodoro_timer()
    elif choice == '4':
        view_goals()
    elif choice == '5':
        view_habits()
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
