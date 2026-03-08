
from database import connect_database
from datetime import datetime




def check_user(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None

def create_user(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (username) VALUES (%s)",
                    (username,)
        )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id


def user_add_review(username):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        user_id = check_user(username)
        if user_id is None:
            user_id = create_user(username)
        cursor.execute("SELECT tvshow_id, title FROM tvshow ORDER BY title")
        shows = cursor.fetchall()
        print("\nAvailable TV Shows:\n")
        for show in shows:
            print(f"{show[0]} - {show[1]}")
        show_id = input("\nEnter the ID of the show you want to review: ")
        while True:
            rating_input = input("Enter your rating (0-10): ")
            try:
                rating = float(rating_input)
                if 0 <= rating <= 10:
                    break
                else:
                    print("Rating must be between 0 and 10.")
            except ValueError:
                print("Rating must be a number.")
        while True:
            review_text = input("\nWrite your review for the tvshow: ").strip()
            if review_text:
                break
            else:
                print("Review cannot be empty.")
        try:
            cursor.execute("""
                INSERT INTO review
                (personal_rating, actual_review, user_id, tvshow_id)
                VALUES (%s, %s, %s, %s)
            """, (rating, review_text, user_id, show_id))
            conn.commit()
            print("\nReview added successfully!")
        except Exception as e:
            print("\nDatabase error:")
            print(e)
    finally:
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")



def show_reviews():
    conn = connect_database()
    cursor = conn.cursor()
    query = """
    SELECT 
        tvshow.title,
        user.username,
        review.personal_rating,
        review.actual_review,
        review.created_at
    FROM review
    JOIN user ON review.user_id = user.user_id
    JOIN tvshow ON review.tvshow_id = tvshow.tvshow_id
    ORDER BY review.created_at DESC
    """
    cursor.execute(query)
    reviews = cursor.fetchall()
    if not reviews:
        print("No reviews exist at this moment.. ")
        return
    print("\033[93m\n========== REVIEWS ==========\n\033[0m")
    for review in reviews:
        title = review[0]
        username = review[1]
        rating = review[2]
        text = review[3]
        date = review[4]
        print(f"Tvshow  : {title}")
        print(f"User    : {username}")
        print(f"Rating  : {rating}/10")
        print(f"Review  : {text}")
        print(f"Date    : {date}")
        print("-" * 40)
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")

def add_tvshow():
    print("Okej wonderful! Please fill in all required information.\n")
    while True:
        title = input("Title of Tv-show: ").strip()
        if title:
            break
        else:
            print("Title cannot be empty!")
    genre = input("Genre: ")
    while True:
        rating_input = input("Your rating: ").strip()
        try:
            rating = float(rating_input)
            break
        except ValueError:
            print("Rating must be a number!")
    description_of = input("Short summary of you tvshow: ")
    while True:
        released_at = input("Release date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(released_at, "%Y-%m-%d")
            break
        except ValueError:
            print("Date must be in YYYY-MM-DD format!")
    while True:
        ended_at = input("End date (leave empty if ongoing): ").strip()
        if not ended_at:
            ended_at = None
            break
        try:
            datetime.strptime(ended_at, "%Y-%m-%d")
            break
        except ValueError:
            print("Date must be in YYYY-MM-DD format!")
    try:
        conn = connect_database()
        cursor = conn.cursor()
        sql_insert = """
        INSERT INTO tvshow 
        (title, genre, rating, description_of, date_released, date_ended)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert, (
            title,
            genre,
            rating,
            description_of,
            released_at,
            ended_at
        ))
        conn.commit()
        print("\nTV-show added successfully!")
    except Exception as e:
        print("\nDatabase error:")
        print(e)
    finally:
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")


def show_actors_in_show():
    conn = connect_database()
    cursor = conn.cursor()
    show_name = input("Enter tvshow name: ")
    query = """
    SELECT actor.full_name, characters.full_name
    FROM actor
    JOIN actor_character
    ON actor.actor_id = actor_character.actor_id
    JOIN characters
    ON actor_character.character_id = characters.character_id
    JOIN character_tvshow
    ON characters.character_id = character_tvshow.character_id
    JOIN tvshow 
    ON character_tvshow.tvshow_id = tvshow.tvshow_id
    WHERE tvshow.title = %s
    """
    cursor.execute(query, (show_name,))
    results = cursor.fetchall()
    for actor in results:
        print(f"{actor[0]} as {actor[1]}")
    cursor.close()
    conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")

def show_average_ratings():
    conn = connect_database()
    cursor = conn.cursor()
    query = """
    SELECT tvshow.title,
    AVG(review.personal_rating) AS average_rating
    FROM review
    JOIN tvshow ON review.tvshow_id = tvshow.tvshow_id
    GROUP BY tvshow.title
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print("\nAverage Ratings\n")
    for row in results:
        print(f"{row[0]} - {round(row[1],2)}")
    cursor.close()
    conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")

def list_actors_tvshow_count():
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT full_name, actor_tvshow_count(actor_id) FROM actor ORDER BY full_name")
        actors = cursor.fetchall()
        print("\nActors and number of TV shows:\n")
        for actor in actors:
            name = actor[0]
            show_count = actor[1]
            print(f"{name} has appeared in {show_count} TV shows")
    except Exception as e:
        print("Database error:", e)
    finally:
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")

def available_shows():
    conn = connect_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, genre, rating, date_released, date_ended, description_of FROM tvshow ORDER BY title")
    rows = cursor.fetchall()
    for row in rows:
        print(f"""
    Title: {row["title"]}
    Genre: {row["genre"]}
    Rating: {row["rating"]}
    Released: {row["date_released"]}
    Ended: {row["date_ended"]}
    Description: {row["description_of"]}
    -----------------------------
    """)
        cursor.close()
        conn.close()
    input("\033[95m\nPress Enter to return to the menu...\033[0m")
