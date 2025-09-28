from datetime import datetime

class ClaimValidator:
    @staticmethod
    def validate_date(date_string):
        """Validerar att datum är i korrekt format"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Ogiltigt datumformat! Använd YYYY-MM-DD"
    
    @staticmethod
    def validate_amount(amount_string):
        """Validerar att belopp är korrekt"""
        try:
            amount = float(amount_string)
            if amount <= 0:
                return False, "Belopp måste vara större än 0"
            return True, amount
        except ValueError:
            return False, "Ogiltigt belopp! Ange ett numeriskt värde."
    
    @staticmethod
    def validate_required_fields(date, vehicle_class, amount):
        """Validerar att obligatoriska fält är ifyllda"""
        if not all([date, vehicle_class, amount]):
            return False, "Vänligen fyll i alla obligatoriska fält!"
        return True, ""
    
    @staticmethod
    def validate_claim_data(date, vehicle_class, amount):
        """Validerar all claim-data"""
        # Validera obligatoriska fält
        is_valid, message = ClaimValidator.validate_required_fields(date, vehicle_class, amount)
        if not is_valid:
            return False, message
        
        # Validera datum
        is_valid, message = ClaimValidator.validate_date(date)
        if not is_valid:
            return False, message
        
        # Validera belopp
        is_valid, message = ClaimValidator.validate_amount(amount)
        if not is_valid:
            return False, message
        
        return True, message  # message innehåller nu det konverterade beloppet