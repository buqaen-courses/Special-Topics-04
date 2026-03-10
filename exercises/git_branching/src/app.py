from auth.login import login
from auth.logout import logout
from ui.header import header

def main():
    print("=== Application Started (v2) ===")
    header()
    print("User flow starting...")
    login()
    logout()

if __name__ == "__main__":
    main()