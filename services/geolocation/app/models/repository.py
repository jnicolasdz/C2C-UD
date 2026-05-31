import app.models.location as location

class Repository:

    def __init__(self):
        self.__locations = []
        self.__index = 0

        self.add_location(name="Sede calle 40", \
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 7 #40-62, Bogotá, Colombia", \
                                        latitude=4.628101562385973, longitude=-74.06592693333083)
        self.add_location(name="Sede macarena A",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 3 #N26A-40, Bogotá, Colombia", \
                                     latitude=4.613573017288183, longitude=-74.06404637326503)
        self.add_location(name="Sede macarena B",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 3A #26B-1, Bogotá, Colombia", \
                                     latitude=4.6135794463079245,longitude=-74.06526948179399)
        self.add_location(name="Sede calle 34",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 34 #13-15, Bogotá, Colombia", \
                                     latitude=4.621984336272019, longitude=-74.06837850449529)
        self.add_location(name="Sede Tecnologica",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 68d Bis A Sur #49F - 70 Bloque 6, piso 1, Tecnológica, Bogotá", \
                                     latitude=4.579922365316238, longitude=-74.15757937482532)
        self.add_location(name="Sede Bosa",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 52 Sur #93d-39, Bogotá, Colombia", \
                                     latitude=4.6384071630332, longitude=-74.1862601018121)
        self.add_location(name="Sede Vivero",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 5 #15-82, Bogotá", \
                                     latitude=4.597362864708261, longitude=-74.06460621077917)
        self.add_location(name="Sede ASAB",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cra 15 #15-2, Bogotá, Colombia", \
                                     latitude=4.6048557389443046, longitude=-74.07873154783844)
        self.add_location(name="Sede Paiba",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cl 13 #31-75, Bogotá, Colombia", \
                                     latitude=4.615281339898904, longitude=-74.09331682907303)

    def create_location(self, name: str, description: str, address: str, \
                        latitude: float, longitude: float) -> location.Location:
        self.__index +=1
        return location.Location(id=self.__index, name=name, description=description, \
                                 address=address, latitude=latitude, longitude=longitude)
    
    def add_location(self, name: str, description: str, address: str, \
                     latitude: float, longitude: float) -> None:
        
        self.__locations.append(self.create_location(name=name, description=description, address=address, \
                                                  latitude=latitude, longitude=longitude))
    
    def get_location_by_id(self, location_id: int) -> location.Location:
        for loc in self.__locations:
            if loc.id == location_id:
                return loc
        return None
    
    def get_location_by_name(self, name: str) -> location.Location:
        for loc in self.__locations:
            if loc.name == name:
                return loc
        return None
    
    def get_location_by_address(self, address: str) -> location.Location:
        for loc in self.__locations:
            if loc.address == address:
                return loc
        return None
    
    def get_location_by_coordinates(self, latitude: float, longitude: float) -> location.Location:
        for loc in self.__locations:
            if loc.latitude == latitude and loc.longitude == longitude:
                return loc
        return None
    
    def delete_location(self, location_id: int) -> bool:
        for i, loc in enumerate(self.__locations):
            if loc.id == location_id:
                del self.__locations[i]
                return True
        return False