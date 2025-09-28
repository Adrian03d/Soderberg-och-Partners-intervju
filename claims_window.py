import tkinter as tk
from tkinter import ttk

class ClaimsWindow:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        
    def show_all_claims(self):
        """Visar alla skadeanmälningar i ett nytt fönster"""
        try:
            rows = self.db_manager.get_all_claims()
            
            # Skapa nytt fönster
            claims_window = tk.Toplevel(self.parent)
            claims_window.title("Alla Skadeanmälningar")
            claims_window.geometry("800x400")
            
            # Skapa trädvy för att visa data
            tree = ttk.Treeview(claims_window, 
                              columns=("ID", "Datum", "Fordonsklass", "Belopp", "Beskrivning"), 
                              show="headings")
            
            # Konfigurera kolumner
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
            raise e