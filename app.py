import streamlit as st
import sqlite3

# --- Database Setup ---
def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Login Check ---
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# --- Register User ---
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- Get All Users ---
def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    result = cursor.fetchall()
    conn.close()
    return result

# --- Delete User ---
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

# --- UI Setup ---
def main():
    st.title("🔐 Login & Register App")
    st.write("Using **Streamlit + SQLite**")

    st.sidebar.title("Menu")
    menu = ["Login", "Register", "👑 Admin Panel"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login_user(username, password)
            if result:
                st.success(f"Welcome, {username}!")
            else:
                st.error("Incorrect username or password")

    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful! You can now login.")
            else:
                st.warning("Username already exists.")

    elif choice == "👑 Admin Panel":
        st.subheader("Admin Login")
        admin_pass = st.text_input("Enter Admin Password", type="password")

        # Hardcoded admin password (you can change it)
        if admin_pass == "admin123":
            st.success("Access Granted")

            users = get_all_users()
            if users:
                st.subheader("👥 Registered Users")
                for user_id, username in users:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"👤 {username}")
                    with col2:
                        if st.button("Delete", key=user_id):
                            delete_user(user_id)
                            st.success(f"User '{username}' deleted.")
                            st.experimental_rerun()
            else:
                st.info("No users registered.")
        else:
            st.warning("Enter correct admin password to access user list.")

# Run setup
setup_db()

# Run app
if __name__ == "__main__":
    main()
