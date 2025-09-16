class Lessee:
    def __init__(self, lessee_id, unit_id, unit_label, lessee_name, addrL1, addrL2, city, state, zip, phone, active):
        self._lesseeId = int(lessee_id)
        self._unitId = int(unit_id)
        self._unitLabel = str(unit_label)
        self._lesseeName = str(lessee_name)
        self._addrL1 = str(addrL1)
        self._addrL2 = str(addrL2)
        self._city = str(city)
        self._state = str(state)
        self._zip = int(zip)
        self._phone = str(phone)
        self._active = bool(active)

    def get_lesseeId(self):
        return self._lesseeId
    
    def set_lesseeId(self, value):
        self._lesseeId = value

    def get_unitId(self):
        return self._unitId
    
    def set_unitId(self, value):
        self._unitId = value

    def get_unitLabel(self):
        return self._unitLabel
    
    def set_unitLabel(self, value):
        self._unitLabel = value

    def get_lesseeName(self):
        return self._lesseeName
    
    def set_lesseeName(self, value):
        self._lesseeName = value

    def get_addrL1(self):
        return self._addrL1
    
    def set_addrL1(self, value):
        self._addrL1 = value

    def get_addrL2(self):
        return self._addrL2
    
    def set_addrL2(self, value):
        self._addrL2 = value

    def get_addrL1(self):
        return self._addrL1
    
    def set_addrL1(self, value):
        self._addrL1 = value

    def get_city(self):
        return self._city
    
    def set_city(self, value):
        self._city = value

    def get_state(self):
        return self._state
    
    def set_state(self, value):
        self._state = value

    def get_zip(self):
        return self._zip
    
    def set_zip(self, value):
        self._zip = value    
        
    def get_phone(self):
        return self._phone
    
    def set_phone(self, value):
        self._phone = value

    def get_active(self):
        return self._active
    
    def set_active(self, value):
        self._active = value