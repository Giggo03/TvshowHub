import temp
import admin
import os
from getpass import getpass

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    user_type = input ("""
        Hello there! 
        user or Admin mode?
        If admin please type secret password
        """).strip().lower()
    if user_type == "admin":
        admin_feature()
    else:
        username = user_type
        user_alternatives(username)

def user_alternatives(username):
    while True:
        clear()
        logo()
        print("="*55)
        print(f" Welcome {username}!")
        print("="*55)
        print("1  - See all TV shows")
        print("2  - Add a new TV show")
        print("3  - See all user reviews")
        print("4  - Add a review for a TV show")
        print("5  - See actors and how many shows they appear in")
        print("6  - Show actors and their characters in a Tv show")
        print("0  - Exit program")
        print("="*50)
        menu_choice = input("\033[93mSelect an option: \033[0m").strip().lower()
        print()
        if menu_choice == "1":
            temp.available_shows()
        elif menu_choice == "2":
            temp.add_tvshow()
        elif menu_choice == "3":
            temp.show_reviews()
        elif menu_choice == "4" or menu_choice == "review":
            temp.user_add_review(username)
        elif menu_choice == "5":
            temp.list_actors_tvshow_count()
        elif menu_choice == "6":
            temp.show_actors_in_show()
        elif menu_choice == "0" or menu_choice == "exit":
            print("\nThank you for using TV Series Hub!\n")
            exit()
        else:
            print("Invalid option. Please try again.\n")



def admin_feature():
    Password = getpass("Very well, Please enter password: ")
    while True:
        if Password != admin.get_password():
            choice = getpass("Password incorrect, Please try again... or Type ‘Back’ to return to the previous menu.  ").strip()
            if choice == "back":
                main()
            elif choice == admin.get_password():
                admin.admin_alternatives()
        elif Password == admin.get_password():
            admin.admin_alternatives()




def logo():
    print("\033[92m")
    print("""
████████╗██╗   ██╗     ███████╗██╗  ██╗ ██████╗ ██╗    ██╗    ██╗  ██╗██╗   ██╗██████╗ 
╚══██╔══╝██║   ██║     ██╔════╝██║  ██║██╔═══██╗██║    ██║    ██║  ██║██║   ██║██╔══██╗
   ██║   ██║   ██║     ███████╗███████║██║   ██║██║ █╗ ██║    ███████║██║   ██║██████╔╝
   ██║   ╚██╗ ██╔╝     ╚════██║██╔══██║██║   ██║██║███╗██║    ██╔══██║██║   ██║██╔══██╗
   ██║    ╚████╔╝      ███████║██║  ██║╚██████╔╝╚███╔███╔╝    ██║  ██║╚██████╔╝██████╔╝
   ╚═╝     ╚═══╝       ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝

                        📺  TV SHOW HUB  📺
    """)
    print("\033[0m")



















if __name__ == "__main__":
    main()