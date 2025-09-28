import sqlite3

class DatabaseManager:
    def __init__(self, db_name="claims.db"):
        self.db_name = db_name
        self.setup_database()
    
    def setup_database(self):
        """Skapar databasen och tabellen om de inte finns"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            vehicle_class TEXT NOT NULL,
            claim_amount REAL NOT NULL,
            description TEXT
        )
        """)
        
        # Försök lägga till description-kolumn om den inte finns
        try:
            cursor.execute("ALTER TABLE claims ADD COLUMN description TEXT")
        except sqlite3.OperationalError:
            # Kolumnen finns redan, ignorerar felet
            pass
        
        conn.commit()
        conn.close()
    
    def add_claim(self, date, vehicle_class, claim_amount, description=""):
        """Lägger till en ny skadeanmälan i databasen"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO claims (date, vehicle_class, claim_amount, description)
        VALUES (?, ?, ?, ?)
        """, (date, vehicle_class, claim_amount, description))
        
        conn.commit()
        claim_id = cursor.lastrowid
        conn.close()
        
        return claim_id
    
    def get_all_claims(self):
        """Hämtar alla skadeanmälningar sorterade på datum"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM claims ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    def clear_database(self):
        """Rensar alla skadeanmälningar från databasen"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM claims")
        conn.commit()
        conn.close()
    
    def reset_database(self):
        """Återställer hela databasen (raderar och skapar ny tabell)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS claims")
        cursor.execute("""
        CREATE TABLE claims (
            claim_id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            vehicle_class TEXT NOT NULL,
            claim_amount REAL NOT NULL,
            description TEXT
        )
        """)
        
        conn.commit()
        conn.close()