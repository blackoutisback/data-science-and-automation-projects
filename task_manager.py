# ===== Importing external modules ===========
import datetime
import os

# Constant format for consistent date parsing and formatting
DATETIME_FORMAT = "%d %b %Y"


# ============================================
# ==== Helper Functions ======================
# ============================================

def get_task_list():
    '''Reads tasks from tasks.txt and returns a list of task dictionaries.'''
    tasks = []
    if not os.path.exists("tasks.txt"):
        return tasks
        
    with open('tasks.txt', 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(', ')
                tasks.append({
                    'username': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'assigned_date': parts[3],
                    'due_date': parts[4],
                    'completed': parts[5]
                })
    return tasks


def save_task_list(tasks):
    '''Writes the updated list of task dictionaries back to tasks.txt.'''
    with open('tasks.txt', 'w') as f:
        task_lines = []
        for t in tasks:
            line = f"{t['username']}, {t['title']}, {t['description']}, {t['assigned_date']}, {t['due_date']}, {t['completed']}"
            task_lines.append(line)
        f.write("\n".join(task_lines))


def print_task_details(task, index=None):
    '''Formats and prints task information in a user-friendly layout.'''
    header = f"Task {index}:" if index is not None else "Task:"
    print("-" * 50)
    print(f"{header:<20} {task['title']}")
    print(f"Assigned to:         {task['username']}")
    print(f"Date assigned:       {task['assigned_date']}")
    print(f"Due date:            {task['due_date']}")
    print(f"Task Complete?       {task['completed']}")
    print(f"Task description:    {task['description']}")
    print("-" * 50)


# ============================================
# ==== Part 3 Modular Functions ==============
# ============================================

def reg_user(user_data):
    '''Registers a new user to user.txt with duplicate username validation.'''
    while True:
        new_username = input("Enter a new username: ").strip()
        
        # Check for duplicate username
        if new_username in user_data:
            print("\nError: That username already exists! Please enter a unique username.\n")
            continue
        
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm password: ")

        if new_password == confirm_password:
            with open('user.txt', 'a') as f:
                f.write(f"\n{new_username}, {new_password}")
            user_data[new_username] = new_password
            print(f"\nUser '{new_username}' registered successfully!")
            break
        else:
            print("\nPasswords do not match! Please try again.\n")


def add_task(user_data):
    '''Prompts for task details and appends a new task to tasks.txt.'''
    while True:
        task_user = input("Name of person assigned to task: ").strip()
        if task_user not in user_data:
            print("User does not exist. Please assign to a valid registered user.")
            continue
        break

    title = input("Title of Task: ")
    desc = input("Description of Task: ")
    
    # Defensive programming for due date input
    while True:
        try:
            due_date_str = input("Due date (e.g., 10 Oct 2026): ").strip()
            datetime.datetime.strptime(due_date_str, DATETIME_FORMAT)
            break
        except ValueError:
            print("Invalid date format! Please use 'DD MMM YYYY' format (e.g., 10 Oct 2026).")

    date_today = datetime.date.today().strftime(DATETIME_FORMAT)
    
    with open('tasks.txt', 'a') as f:
        f.write(f"\n{task_user}, {title}, {desc}, {date_today}, {due_date_str}, No")
    print("\nTask added successfully!")


def view_all():
    '''Displays all tasks stored in tasks.txt.'''
    tasks = get_task_list()
    if not tasks:
        print("\nNo tasks found.")
        return
        
    print("\n================ ALL TASKS ================")
    for i, task in enumerate(tasks, 1):
        print_task_details(task, i)


def view_mine(curr_user):
    '''Displays user-assigned tasks with options to mark complete or edit.'''
    tasks = get_task_list()
    user_tasks = []
    
    # Filter tasks specific to the logged-in user
    for index, task in enumerate(tasks):
        if task['username'] == curr_user:
            user_tasks.append((index, task))
            
    if not user_tasks:
        print("\nYou currently have no assigned tasks.")
        return

    print(f"\n================ MY TASKS ({curr_user}) ================")
    for display_num, (orig_idx, task) in enumerate(user_tasks, 1):
        print_task_details(task, display_num)

    while True:
        try:
            choice = int(input("\nEnter task number to edit/complete, or -1 to return to main menu: "))
            if choice == -1:
                return
            
            if 1 <= choice <= len(user_tasks):
                target_orig_idx, target_task = user_tasks[choice - 1]
                
                action = input("Enter 'c' to mark as complete, or 'e' to edit task: ").strip().lower()
                
                # Option 1: Mark Task Complete
                if action == 'c':
                    tasks[target_orig_idx]['completed'] = 'Yes'
                    save_task_list(tasks)
                    print("\nTask marked as complete successfully!")
                    break
                    
                # Option 2: Edit Task
                elif action == 'e':
                    if target_task['completed'] == 'Yes':
                        print("\nCannot edit task: This task has already been completed.")
                        break
                        
                    edit_choice = input("Edit (u)sername, (d)ue date, or (b)oth? ").strip().lower()
                    
                    if edit_choice in ['u', 'b']:
                        new_assigned_user = input("Enter new assigned username: ").strip()
                        tasks[target_orig_idx]['username'] = new_assigned_user
                        
                    if edit_choice in ['d', 'b']:
                        while True:
                            try:
                                new_date = input("Enter new due date (e.g., 10 Oct 2026): ").strip()
                                datetime.datetime.strptime(new_date, DATETIME_FORMAT)
                                tasks[target_orig_idx]['due_date'] = new_date
                                break
                            except ValueError:
                                print("Invalid date format! Try again.")
                                
                    save_task_list(tasks)
                    print("\nTask updated successfully!")
                    break
                else:
                    print("Invalid action selected. Choose 'c' or 'e'.")
            else:
                print("Invalid task number! Please select a valid task number.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def view_completed():
    '''Admin functionality to view all completed tasks.'''
    tasks = get_task_list()
    completed_tasks = [t for t in tasks if t['completed'] == 'Yes']
    
    if not completed_tasks:
        print("\nNo completed tasks found.")
        return
        
    print("\n================ COMPLETED TASKS ================")
    for i, task in enumerate(completed_tasks, 1):
        print_task_details(task, i)


def delete_task():
    '''Admin functionality to select and delete a task.'''
    tasks = get_task_list()
    if not tasks:
        print("\nNo tasks available to delete.")
        return
        
    print("\n================ DELETE A TASK ================")
    for i, task in enumerate(tasks, 1):
        print_task_details(task, i)
        
    while True:
        try:
            choice = int(input("\nEnter task number to delete (-1 to cancel): "))
            if choice == -1:
                return
            if 1 <= choice <= len(tasks):
                removed_task = tasks.pop(choice - 1)
                save_task_list(tasks)
                print(f"\nTask '{removed_task['title']}' deleted successfully!")
                break
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid integer.")


def generate_reports():
    '''Generates task_overview.txt and user_overview.txt report files.'''
    tasks = get_task_list()
    today = datetime.datetime.today()

    # 1. Generate task_overview.txt
    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t['completed'] == 'Yes')
    uncompleted = total_tasks - completed
    
    overdue = 0
    for t in tasks:
        if t['completed'] == 'No':
            try:
                due_dt = datetime.datetime.strptime(t['due_date'], DATETIME_FORMAT)
                if due_dt < today:
                    overdue += 1
            except ValueError:
                pass
                
    pct_incomplete = (uncompleted / total_tasks * 100) if total_tasks > 0 else 0
    pct_overdue = (overdue / total_tasks * 100) if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as f:
        f.write("================ TASK OVERVIEW ================\n")
        f.write(f"Total tasks tracked:                    {total_tasks}\n")
        f.write(f"Total completed tasks:                  {completed}\n")
        f.write(f"Total uncompleted tasks:                {uncompleted}\n")
        f.write(f"Total uncompleted & overdue tasks:      {overdue}\n")
        f.write(f"Percentage of incomplete tasks:         {pct_incomplete:.2f}%\n")
        f.write(f"Percentage of overdue tasks:            {pct_overdue:.2f}%\n")
        f.write("===============================================\n")

    # 2. Generate user_overview.txt
    user_data = {}
    if os.path.exists('user.txt'):
        with open('user.txt', 'r') as uf:
            for line in uf:
                if line.strip():
                    u, p = line.strip().split(', ')
                    user_data[u] = p
                
    total_users = len(user_data)
    
    with open("user_overview.txt", "w") as f:
        f.write("================ USER OVERVIEW ================\n")
        f.write(f"Total users registered:                 {total_users}\n")
        f.write(f"Total tasks tracked:                    {total_tasks}\n")
        f.write("-----------------------------------------------\n")
        
        for user in user_data:
            user_tasks = [t for t in tasks if t['username'] == user]
            u_total = len(user_tasks)
            
            pct_assigned = (u_total / total_tasks * 100) if total_tasks > 0 else 0
            u_completed = sum(1 for t in user_tasks if t['completed'] == 'Yes')
            pct_u_comp = (u_completed / u_total * 100) if u_total > 0 else 0
            pct_u_incomp = ((u_total - u_completed) / u_total * 100) if u_total > 0 else 0
            
            u_overdue = 0
            for t in user_tasks:
                if t['completed'] == 'No':
                    try:
                        due_dt = datetime.datetime.strptime(t['due_date'], DATETIME_FORMAT)
                        if due_dt < today:
                            u_overdue += 1
                    except ValueError:
                        pass
                        
            pct_u_overdue = (u_overdue / u_total * 100) if u_total > 0 else 0

            f.write(f"User: {user}\n")
            f.write(f"  - Tasks assigned:                      {u_total}\n")
            f.write(f"  - % of total tasks:                   {pct_assigned:.2f}%\n")
            f.write(f"  - % completed:                        {pct_u_comp:.2f}%\n")
            f.write(f"  - % to be completed:                  {pct_u_incomp:.2f}%\n")
            f.write(f"  - % incomplete & overdue:             {pct_u_overdue:.2f}%\n\n")
            
        f.write("===============================================\n")
        
    print("\nReports successfully generated (task_overview.txt & user_overview.txt).")


def display_stats():
    '''Reads and displays task and user overview statistics to the screen.'''
    # If report files do not exist yet, generate them first
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()
        
    print("\n")
    with open("task_overview.txt", "r") as f:
        print(f.read())
        
    print("\n")
    with open("user_overview.txt", "r") as f:
        print(f.read())


# ============================================
# ==== Main Program Execution ================
# ============================================

# Read credentials from user.txt
user_data = {}
if os.path.exists('user.txt'):
    with open('user.txt', 'r') as user_file:
        for line in user_file:
            if line.strip():
                username, password = line.strip().split(', ')
                user_data[username] = password

# Authentication Loop
curr_user = None
while curr_user is None:
    username_input = input("Enter username: ").strip()
    password_input = input("Enter password: ").strip()
    
    if username_input in user_data and user_data[username_input] == password_input:
        print(f"\nLogin Successful! Welcome, {username_input}.")
        curr_user = username_input
    else:
        print("\nInvalid username or password. Please try again.\n")

# Main Application Loop
while True:
    # Present administrative menu options if logged in as 'admin'
    if curr_user == 'admin':
        menu = input('''\nPlease select one of the following options:
r   - register user
a   - add task
va  - view all tasks
vm  - view my tasks
vc  - view completed tasks
del - delete a task
ds  - display statistics
gr  - generate reports
e   - exit
: ''').strip().lower()
    else:
        menu = input('''\nPlease select one of the following options:
a   - add task
va  - view all tasks
vm  - view my tasks
e   - exit
: ''').strip().lower()

    # Option Routing
    if menu == 'r' and curr_user == 'admin':
        reg_user(user_data)
    elif menu == 'a':
        add_task(user_data)
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(curr_user)
    elif menu == 'vc' and curr_user == 'admin':
        view_completed()
    elif menu == 'del' and curr_user == 'admin':
        delete_task()
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports()
    elif menu == 'ds' and curr_user == 'admin':
        display_stats()
    elif menu == 'e':
        print('\nGoodbye!')
        break
    else:
        print("\nInvalid option or unauthorized action. Please try again.")