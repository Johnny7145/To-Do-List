import pandas as pd
import os

FILE_NAME = "to_do_list.csv"

def load_file():
    """Load the CSV or create it if it doesn't exist."""
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        df = pd.DataFrame(columns=["Task", "Status"])
        df.to_csv(FILE_NAME, index=False)
        return df

def save_file(df):
    """Save the current DataFrame to CSV."""
    df.to_csv(FILE_NAME, index=False)

def show_menu():
    print("\n====== TO-DO LIST APP ======")
    print("1. Add Task")
    print("3. Delete Task")
    print("4. View task")
    print("5. Exit app")
    choice = input("Select an option (1-4): ")
    print("")
    return choice

def add_task():
    df = load_file()
    task = input("Enter the task: ").strip()

    if not task: 
        print("You entered an empty task. Not added.")
        return

    if task in df["Task"].values:
        print(f"'{task}' is already on the list.")
        return

    new_row = pd.DataFrame({"Task": [task], "Status": ["Pending"]}) #The isin() function is one of the most commonly used methods for filtering data based on a list of values.
    df = pd.concat([df, new_row], ignore_index=True)
    save_file(df)
    print(f"Added: '{task}' (Pending)")

def view_tasks():
    df = load_file()
    if df.empty:
        print("Your to-do list is empty.")
        return

    print("Your Tasks:")
    for i, row in df.iterrows():
        num = i + 1
        task = row["Task"]
        status = row["Status"]
        print(f"{num}. {task}  -->  {status}")

def pick_task(df, action_text):
    """Helper: ask user for index of task and return that index, or None if invalid."""
    if df.empty:
        print("No tasks available yet.")
        return None

    view_tasks()
    try:
        selection = int(input(f"Enter the number of the task to {action_text}: "))
        idx = selection - 1
        if idx < 0 or idx >= len(df):
            print("That number doesn't exist.")
            return None
        return idx
    except ValueError:
        print("Invalid input. Please type a number.")
        return None

def delate_task():
    df = load_file()
    idx_to_delete = pick_task(df, "delete")
    if idx_to_delete is not None:
        task = df.loc[idx_to_delete, "Task"]
        df = df.drop(idx_to_delete).reset_index(drop=True)
        save_file(df)
        print(f"Deleted: '{task}'")

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            add_task()
        elif choice == "3":
            delate_task()
        elif choice == "4":
            view_tasks()
        elif choice == "5":
            print("Exiting To-Do List App. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
    