from models import add_user, get_all_users, add_goal, get_goals_by_user

# Example of adding a new user
add_user('john_doe', 'john@example.com', 'hashedpassword123')

# Example of getting all users
users = get_all_users()
print(users)

# Example of adding a new goal
add_goal(1, 'Learn Python', 'Complete a Python course', '2025-12-31', 'Prioritize')

# Example of getting all goals for a user
goals = get_goals_by_user(1)
print(goals)
