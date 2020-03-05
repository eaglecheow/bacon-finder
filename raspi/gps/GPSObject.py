class GPSObject:
    def __init__(self):
        super().__init__()

        self.timeStamp: int = 0
        self.latitude: float = None
        self.latitudeDirection: str = None
        self.longitude: float = None
        self.longitudeDirection: str = None
        self.altitude: float = None
        self.altitudeUnits: str = None
        self.speed: float = None
        self.satelliteAmount: int = 0

    def checkDataValidity(self) -> bool:
        if not self.timeStamp:
            return False
        return True
