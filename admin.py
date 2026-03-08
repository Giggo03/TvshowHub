import temp
import main
from database import connect_database
from datetime import datetime

def get_password():
    password = "Gifflar67"
    return password

def admin_alternatives():
    while True:
        main.clear()
        print("\n" + "="*50)
        print("                ADMIN CONTROL PANEL")
        print("="*50)
        print("1  - Add a new TV show")
        print("2  - Delete a TV show")
        print("3  - Edit database tables")
        print("0  - Return to main menu")
        print("="*50)
        choice = input("Select an option: ").strip().lower()
        if choice == "1" or choice == "add":
            temp.add_tvshow()
        elif choice == "2" or choice == "delete":
            delete_show()
        elif choice == "3" or choice == "edit":
            edit_feature()
        elif choice == "0" or choice == "back":
            main.main()
            break
        else:
            print("\nInvalid option, please try again.")


def edit_feature():
    allowed_tables = ["tvshow", "actor", "characters"]
    table_name = input("""
    Which table do you want to edit?
    tvshow
    actor
    characters
    Type table name: 
    """).strip().lower()
    if table_name not in allowed_tables:
        print("Invalid table name...")
        return
    id_column = f"{table_name}_id"
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if not rows:
            print("No data found.")
            return
        print("\nCurrent Data:\n")
        for col in columns:
            print(f"{col:<20}", end="")
        print()
        print("-" * (20 * len(columns)))
        for row in rows:
            formatted_row = []
            for i, value in enumerate(row):
                if value is None:
                    value = "None"
                value = str(value)
                if columns[i] == "description_of":
                    words = value.split()
                    value = " ".join(words[:3]) + "..."
                if len(value) > 20:
                    value = value[:17] + "..."
                formatted_row.append(f"{value:<20}")
            print("".join(formatted_row))
        selected_id = input(f"\nEnter {id_column} to edit: ").strip()
        if not selected_id.isdigit():
            print("Invalid ID...")
            return
        editable_columns = [col for col in columns if col != id_column]
        print("\nEditable columns:")
        for col in editable_columns:
            print("-", col)
        column_choice = input("\nWhich column do you want to edit? ").strip()
        if column_choice not in editable_columns:
            print("Invalid column...")
            return
        new_value = input("Enter new value: ").strip()
        confirm = input("Are you sure you want to update? (y/n): ").strip().lower()
        if confirm not in ["y", "yes"]:
            print("Update cancelled.")
            return
        sql = f"""
        UPDATE {table_name}
        SET {column_choice} = %s
        WHERE {id_column} = %s
        """
        cursor.execute(sql, (new_value, selected_id))
        conn.commit()
        print("\nUpdated successfully!")
    except Exception as e:
        print("\nDatabase error...")
        print(e)
    finally:
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")
    admin_alternatives()

def delete_show():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT tvshow_id, title FROM tvshow")
        shows = cursor.fetchall()
        if not shows:
            print("No shows was found ")
            admin_alternatives()
        print("--Available Tv-shows--")
        for show in shows:
            print(f"ID:{show[0]} - {show[1]}")
        tvshow_id = input("Input the ID for removal: ")
        cursor.execute("SELECT title FROM tvshow WHERE tvshow_id = %s", (tvshow_id,))
        show = cursor.fetchone()
        show_title = show[0]
        confirmation = input(f"\n\033[91mAre you sure you wanna delete {show_title}? (y/n):\033[0m\n ").strip().lower()
        if confirmation in ["n", "no"]:
            print("Deletion cancelled")
            admin_alternatives()
        elif confirmation in ["y", "yes"]:
            cursor.execute("DELETE FROM tvshow WHERE tvshow_id = %s", (tvshow_id, ))
            conn.commit()
            print(f"Successfully deleted {show_title}")
        else:
            print("Invalid pick: ")
            admin_alternatives()
    except Exception as e:
        print("Error while deleting... ")
        print(e)
    finally:
        cursor.close()
        conn.close()
        input("\033[95m\nPress Enter to return to the menu...\033[0m")
        admin_alternatives()





