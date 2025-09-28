import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ClaimsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skadeanmälan System")
        self.root.geometry("500x400")
        
        # Skapa databas och tabell om de inte finns
        self.setup_database()
        
        # Skapa GUI-element
        self.create_widgets()
        
    def setup_database(self):
        """Skapar databasen och tabellen om de inte finns"""
        conn = sqlite3.connect("claims.db")
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
    
    def create_widgets(self):
        """Skapar alla GUI-element"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(main_frame, text="Skadeanmälan", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Datum
        ttk.Label(main_frame, text="Datum (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=30)
        self.date_entry.grid(row=1, column=1, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Sätt dagens datum
        
        # Fordonsklass
        ttk.Label(main_frame, text="Fordonsklass:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.vehicle_class = ttk.Combobox(main_frame, width=27, values=["Car", "Truck", "Bus", "Motorcycle", "Other"])
        self.vehicle_class.grid(row=2, column=1, pady=5)
        self.vehicle_class.set("Car")  # Standardvärde
        
        # Skadebelopp
        ttk.Label(main_frame, text="Skadebelopp (SEK):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(main_frame, width=30)
        self.amount_entry.grid(row=3, column=1, pady=5)
        
        # Beskrivning
        ttk.Label(main_frame, text="Beskrivning:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(main_frame, width=30, height=4)
        self.description_text.grid(row=4, column=1, pady=5)
        
        # Knappar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Lägg till skadeanmälan", 
                  command=self.add_claim).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Visa alla anmälningar", 
                  command=self.show_all_claims).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rensa databas", 
                  command=self.clear_database).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Återställ databas", 
                  command=self.reset_database).pack(side=tk.LEFT, padx=5)
        
        # Statusmeddelande
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
    
    def add_claim(self):
        """Lägger till en ny skadeanmälan i databasen"""
        try:
            # Hämta data från formuläret
            date = self.date_entry.get()
            vehicle_class = self.vehicle_class.get()
            amount = self.amount_entry.get()
            description = self.description_text.get("1.0", tk.END).strip()
            
            # Validera input
            if not all([date, vehicle_class, amount]):
                messagebox.showerror("Fel", "Vänligen fyll i alla obligatoriska fält!")
                return
            
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Fel", "Ogiltigt datumformat! Använd YYYY-MM-DD")
                return
            
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Belopp måste vara större än 0")
            except ValueError:
                messagebox.showerror("Fel", "Ogiltigt belopp! Ange ett numeriskt värde.")
                return
            
            # Lägg till i databasen
            conn = sqlite3.connect("claims.db")
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT INTO claims (date, vehicle_class, claim_amount, description)
            VALUES (?, ?, ?, ?)
            """, (date, vehicle_class, amount, description))
            
            conn.commit()
            conn.close()
            
            # Rensa formuläret
            self.amount_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)
            
            # Visa bekräftelse
            self.status_label.config(text=f"Skadeanmälan lagrad! ID: {cursor.lastrowid}")
            messagebox.showinfo("Lyckat", "Skadeanmälan har lagrats i databasen!")
            
        except sqlite3.OperationalError as e:
            if "no such column: description" in str(e):
                # Om description-kolumnen saknas, återställ databasen
                messagebox.showwarning("Databasuppdatering", 
                                      "Databasen behöver uppdateras. Återställer nu...")
                self.reset_database()
                # Försök igen efter reset
                self.add_claim()
            else:
                messagebox.showerror("Databasfel", f"Ett fel uppstod: {str(e)}")
        except Exception as e:
            messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def show_all_claims(self):
        """Visar alla skadeanmälningar i ett nytt fönster"""
        try:
            conn = sqlite3.connect("claims.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM claims ORDER BY date DESC")
            rows = cursor.fetchall()
            conn.close()
            
            # Skapa nytt fönster
            claims_window = tk.Toplevel(self.root)
            claims_window.title("Alla Skadeanmälningar")
            claims_window.geometry("800x400")
            
            tree = ttk.Treeview(claims_window, columns=("ID", "Datum", "Fordonsklass", "Belopp", "Beskrivning"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Datum", text="Datum")
            tree.heading("Fordonsklass", text="Fordonsklass")
            tree.heading("Belopp", text="Belopp (SEK)")
            tree.heading("Beskrivning", text="Beskrivning")
            
            tree.column("ID", width=50)
            tree.column("Datum", width=100)
            tree.column("Fordonsklass", width=100)
            tree.column("Belopp", width=100)
            tree.column("Beskrivning", width=350)
            
            # Lägg till data
            for row in rows:
                tree.insert("", tk.END, values=row)
            
            tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Lägg till knapp för att stänga
            ttk.Button(claims_window, text="Stäng", 
                      command=claims_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def clear_database(self):
        """Rensar databasen efter bekräftelse"""
        if messagebox.askyesno("Bekräfta", "Vill du verkligen rensa alla skadeanmälningar?"):
            try:
                conn = sqlite3.connect("claims.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM claims")
                conn.commit()
                conn.close()
                
                self.status_label.config(text="Databasen har rensats!")
                messagebox.showinfo("Lyckat", "Alla skadeanmälningar har raderats!")
                
            except Exception as e:
                messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def reset_database(self):
        """Återställer hela databasen (raderar och skapar ny tabell)"""
        if messagebox.askyesno("Bekräfta", "Vill du verkligen återställa hela databasen? All data kommer försvinna."):
            try:
                conn = sqlite3.connect("claims.db")
                cursor = conn.cursor()
                
                # Radera och skapa ny tabell
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
                
                self.status_label.config(text="Databasen har återställts!")
                messagebox.showinfo("Lyckat", "Databasen har återställts med ny struktur!")
                
            except Exception as e:
                messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")

def main():
    """Startar GUI-applikationen"""
    root = tk.Tk()
    app = ClaimsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()