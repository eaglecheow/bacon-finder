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
        self.satelliteAmount: int = 0

    def checkDataValidity(self) -> bool:
        if (
            not self.timeStamp
            or not self.latitude
            or not self.latitudeDirection
            or not self.longitude
            or not self.longitudeDirection
            or not self.altitude
            or not self.altitudeUnits
            or not self.satelliteAmount
        ):
            return False
        return True
