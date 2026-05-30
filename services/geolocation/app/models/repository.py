import app.models.location as location

class Repository:

    def __init__(self):
        self.__locations = []
        self.__index = 0

        self.add_location(name="Sede calle 40", \
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 7 #40-62, Bogotá, Colombia", \
                                        latitude=4.648283, longitude=-74.062759)
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
                                     latitude=4.622224945654993, longitude=-74.06832485478414)
        self.add_location(name="Sede Tecnologica",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 68d Bis A Sur #49F - 70 Bloque 6, piso 1, Tecnológica, Bogotá", \
                                     latitude=4.580178800021666, longitude=-74.15763258885795)
        self.add_location(name="Sede Bosa",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 52 Sur #93d-39, Bogotá, Colombia", \
                                     latitude=4.638823980689703, longitude=-74.18633476692263)
        self.add_location(name="Sede Vivero",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 5 #15-82, Bogotá", \
                                     latitude=4.597661886496556, longitude=-74.06463098881974)
        self.add_location(name="Sede ASAB",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cra 15 #15-2, Bogotá, Colombia", \
                                     latitude=4.605336743055908, longitude=-74.0785487087344)
        self.add_location(name="Sede Paiba",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cl 13 #31-75, Bogotá, Colombia", \
                                     latitude=4.6159815636016175, longitude=-74.09321982318362)

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