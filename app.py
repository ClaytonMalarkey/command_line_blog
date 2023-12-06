import mariadb
import sys
import dbcreds

# Function to establish a database connection
def connect_db():
    try:
        conn = mariadb.connect(
            user=dbcreds.user,
            password=dbcreds.password,
            host=dbcreds.host,
            port=dbcreds.port,
            database=dbcreds.database
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

# Function to close the database connection
def close_db(conn):
    conn.close()

# Function to log in a user
def login(cursor, conn):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("CALL select_user(?, ?);", (username, password))
    result = cursor.fetchall()

    if len(result) == 1:
        return result[0][0]
    else:
        return None

# Function to create a new post
def create_post(cursor, conn, client_id):
    title = input("Enter the title for your post: ")
    content = input("Enter the content for your post: ")

    cursor.execute("CALL insert_post(?, ?, ?);", (client_id, content, title))
    conn.commit()
    print("Post created successfully!")

# Function to retrieve all posts
def retrieve_all_posts(cursor, conn):
    cursor.execute("CALL retrieve_all_posts();")
    posts = cursor.fetchall()

    for post in posts:
        print(f"Title: {post[2]}\nContent: {post[1]}\n")

# Function to retrieve posts made by a specific user
def retrieve_posts_by_user(cursor, conn, username):
    cursor.execute("CALL retrieve_posts_by_user(?);", (username,))
    posts = cursor.fetchall()

    if posts:
        for post in posts:
            print(f"Title: {post[2]}\nContent: {post[1]}\n")
    else:
        print(f"No posts found for user {username}.")

# Function to retrieve all usernames in the system
def retrieve_all_usernames(cursor, conn):
    cursor.execute("CALL retrieve_all_usernames();")
    usernames = cursor.fetchall()

    if usernames:
        print("Usernames in the system:")
        for username in usernames:
            print(username[0])
    else:
        print("No usernames found in the system.")

# Main function
def main():
    conn = connect_db()
    cursor = conn.cursor()

    client_id = login(cursor, conn)

    if client_id is not None:
        while True:
            print("1. Insert a new post")
            print("2. Read all posts")
            print("3. Read my posts")
            print("4. Show all usernames")
            print("5. Quit")

            choice = input("Select an option (1/2/3/4/5): ")

            if choice == "1":
                create_post(cursor, conn, client_id)
            elif choice == "2":
                retrieve_all_posts(cursor, conn)
            elif choice == "3":
                retrieve_posts_by_user(cursor, conn, username)
            elif choice == "4":
                retrieve_all_usernames(cursor, conn)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

    cursor.close()
    close_db(conn)

if __name__ == "__main__":
    main()
