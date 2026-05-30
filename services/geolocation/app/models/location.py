from pydantic import BaseModel

class Location(BaseModel):
    id : int 
    name : str
    description : str
    address : str
    latitude : float
    longitude : float

    def __str__(self):
        return f"Location(id={self.id}, name='{self.name}', description='{self.description}', address='{self.address}', latitude={self.latitude}, longitude={self.longitude})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
    
    

    
