from student_search import search_student_by_id

def main():
    while(True):
        search_student_by_id()
        
        choice = input("Do you want to search another student? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting program...")
            break

if __name__ == "__main__":
    main()
