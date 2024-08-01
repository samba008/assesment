import sqlite3
import json

# Database file
DATABASE_FILE = 'sat_results.db'


class SATResults:
    def __init__(self):
        self.create_table()

    def connect_db(self):
        return sqlite3.connect(DATABASE_FILE)

    def create_table(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sat_results (
                    name TEXT PRIMARY KEY,
                    address TEXT,
                    city TEXT,
                    country TEXT,
                    pincode TEXT,
                    sat_score REAL,
                    passed TEXT
                )
            ''')
            conn.commit()

    def insert_data(self):
        name = input("Enter Name: ").strip()
        address = input("Enter Address: ").strip()
        city = input("Enter City: ").strip()
        country = input("Enter Country: ").strip()
        pincode = input("Enter Pincode: ").strip()
        sat_score = float(input("Enter SAT score: ").strip())

        passed = 'Pass' if sat_score > 30 else 'Fail'

        with self.connect_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO sat_results (name, address, city, country, pincode, sat_score, passed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, address, city, country, pincode, sat_score, passed))
                conn.commit()
                print("Data inserted successfully.")
            except sqlite3.IntegrityError:
                print("Record with this name already exists.")

    def view_all_data(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sat_results')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            print(json.dumps(data, indent=4))

    def get_rank(self):
        name = input("Enter Name to get rank: ").strip()
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, sat_score FROM sat_results ORDER BY sat_score DESC
            ''')
            rows = cursor.fetchall()
            sorted_data = {row[0]: idx + 1 for idx, row in enumerate(rows)}
            if name in sorted_data:
                print(f"Rank of {name}: {sorted_data[name]}")
            else:
                print("Record not found.")

    def update_score(self):
        name = input("Enter Name to update score: ").strip()
        new_score = float(input("Enter new SAT score: ").strip())
        passed = 'Pass' if new_score > 30 else 'Fail'

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE sat_results
                SET sat_score = ?, passed = ?
                WHERE name = ?
            ''', (new_score, passed, name))
            conn.commit()
            if cursor.rowcount > 0:
                print("Score updated successfully.")
            else:
                print("Record not found.")

    def delete_record(self):
        name = input("Enter Name to delete record: ").strip()

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sat_results WHERE name = ?', (name,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Record for {name} deleted successfully.")
            else:
                print("Record not found.")

    def calculate_average(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT AVG(sat_score) FROM sat_results')
            average_score = cursor.fetchone()[0]
            if average_score is not None:
                print(f"Average SAT score: {average_score:.2f}")
            else:
                print("No data available.")

    def filter_by_status(self):
        status = input("Enter status to filter by (Pass/Fail): ").strip()
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sat_results WHERE passed = ?', (status,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            print(json.dumps(data, indent=4))

    def main_menu(self):
        while True:
            print("\n--- SAT Results Management ---")
            print("1. Insert data")
            print("2. View all data")
            print("3. Get rank")
            print("4. Update score")
            print("5. Delete one record")
            print("6. Calculate Average SAT Score")
            print("7. Filter records by Pass/Fail Status")
            print("8. Exit")

            choice = input("Enter your choice (1-8): ").strip()

            if choice == '1':
                self.insert_data()
            elif choice == '2':
                self.view_all_data()
            elif choice == '3':
                self.get_rank()
            elif choice == '4':
                self.update_score()
            elif choice == '5':
                self.delete_record()
            elif choice == '6':
                self.calculate_average()
            elif choice == '7':
                self.filter_by_status()
            elif choice == '8':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    manager = SATResults()
    manager.main_menu()
