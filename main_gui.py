import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import DatabaseManager
from validators import ClaimValidator
from claims_window import ClaimsWindow

class ClaimsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skadeanmälan System")
        self.root.geometry("500x400")
        
        # Initiera databashanterare och andra komponenter
        self.db_manager = DatabaseManager()
        self.claims_window = ClaimsWindow(root, self.db_manager)
        
        # Skapa GUI-element
        self.create_widgets()
        
    def create_widgets(self):
        """Skapar alla GUI-element"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(main_frame, text="Skadeanmälan", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Formulärfält
        self.create_form_fields(main_frame)
        
        # Knappar
        self.create_buttons(main_frame)
        
        # Statusmeddelande
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
    
    def create_form_fields(self, parent):
        """Skapar formulärfälten"""
        # Datum
        ttk.Label(parent, text="Datum (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(parent, width=30)
        self.date_entry.grid(row=1, column=1, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Fordonsklass
        ttk.Label(parent, text="Fordonsklass:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.vehicle_class = ttk.Combobox(parent, width=27, 
                                        values=["Car", "Truck", "Bus", "Motorcycle", "Other"])
        self.vehicle_class.grid(row=2, column=1, pady=5)
        self.vehicle_class.set("Car")
        
        # Skadebelopp
        ttk.Label(parent, text="Skadebelopp (SEK):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(parent, width=30)
        self.amount_entry.grid(row=3, column=1, pady=5)
        
        # Beskrivning
        ttk.Label(parent, text="Beskrivning:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(parent, width=30, height=4)
        self.description_text.grid(row=4, column=1, pady=5)
    
    def create_buttons(self, parent):
        """Skapar knapparna"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Lägg till skadeanmälan", 
                  command=self.add_claim).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Visa alla anmälningar", 
                  command=self.show_all_claims).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rensa databas", 
                  command=self.clear_database).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Återställ databas", 
                  command=self.reset_database).pack(side=tk.LEFT, padx=5)
    
    def add_claim(self):
        """Lägger till en ny skadeanmälan i databasen"""
        try:
            # Hämta data från formuläret
            date = self.date_entry.get()
            vehicle_class = self.vehicle_class.get()
            amount = self.amount_entry.get()
            description = self.description_text.get("1.0", tk.END).strip()
            
            # Validera data
            is_valid, result = ClaimValidator.validate_claim_data(date, vehicle_class, amount)
            if not is_valid:
                messagebox.showerror("Fel", result)
                return
            
            # Lägg till i databasen
            claim_id = self.db_manager.add_claim(date, vehicle_class, result, description)
            
            # Rensa formuläret
            self.amount_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)
            
            # Visa bekräftelse
            self.status_label.config(text=f"Skadeanmälan lagrad! ID: {claim_id}")
            messagebox.showinfo("Lyckat", "Skadeanmälan har lagrats i databasen!")
            
        except Exception as e:
            messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def show_all_claims(self):
        """Visar alla skadeanmälningar"""
        try:
            self.claims_window.show_all_claims()
        except Exception as e:
            messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def clear_database(self):
        """Rensar databasen efter bekräftelse"""
        if messagebox.askyesno("Bekräfta", "Vill du verkligen rensa alla skadeanmälningar?"):
            try:
                self.db_manager.clear_database()
                self.status_label.config(text="Databasen har rensats!")
                messagebox.showinfo("Lyckat", "Alla skadeanmälningar har raderats!")
            except Exception as e:
                messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")
    
    def reset_database(self):
        """Återställer hela databasen"""
        if messagebox.askyesno("Bekräfta", "Vill du verkligen återställa hela databasen? All data kommer försvinna."):
            try:
                self.db_manager.reset_database()
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