import app.models.repository as repository_module

class GeolocationService:

    def __init__(self):
        self.repository = repository_module.Repository()

    def get_location_by_id(self, location_id: int):
        if self.repository.get_location_by_id(location_id=location_id) is None:
            raise ValueError("Location with the given ID does not exist.")
        return self.repository.get_location_by_id(location_id=location_id).to_dict()
    
    def get_location_by_name(self, name: str):
        if self.repository.get_location_by_name(name=name) is None:
            raise ValueError("Location with the given name does not exist.")
        return self.repository.get_location_by_name(name=name).to_dict()
    
    def get_location_by_address(self, address: str):
        if self.repository.get_location_by_address(address=address) is None:
            raise ValueError("Location with the given address does not exist.")
        return self.repository.get_location_by_address(address=address).to_dict()

    def get_all_locations(self):
        if self.repository.get_all_locations() is None or len(self.repository.get_all_locations()) == 0:
            raise ValueError("No locations available.")
        return [loc.to_dict() for loc in self.repository.get_all_locations()]
    
    def create_location(self, name: str, description: str, address: str, latitude: float, longitude: float):
        if self.repository.get_location_by_coordinates(latitude=latitude, longitude=longitude) is not None:
            raise ValueError("A location with the same coordinates already exists.")
        else:
            self.repository.add_location(name=name, description=description, address=address, latitude=latitude, longitude=longitude)

    def delete_location(self, location_id: int):
        if self.repository.delete_location(location_id=location_id):
            return True
        else:
            raise ValueError("Location with the given ID does not exist.")
        


