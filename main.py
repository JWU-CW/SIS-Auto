from student_search import search_student_by_id
from google_admin import create_google_account

def main():
    res = search_student_by_id()
    # create_google_account(res.first_name, res.last_name, res.email, res.password)

    create_google_account('John', 'Test', '12345', 'abcd1234')

if __name__ == "__main__":
    main()
