class Type:
    def __init__(self, type_name, description = None):
        self.type_name = type_name
        self.description = description

    def __str__(self):
        return f'\nDrone type is {self.type_name} - {self.description}.' if self.description else f'Drone type is {self.type_name}.'

class DroneInformation:
    def __init__(self, size = None, weight = None, max_speed = None, max_altitude = None):
        self.size = size
        self.weight = weight
        self.max_speed = max_speed
        self.max_altitude = max_altitude

    def __str__(self):
        info = {
            '  - size[cm]: ' : self.size,
            '  - weight[kg]: ' : self.weight,
            '  - max speed[m/s]: ' : self.max_speed,
            '  - max altitude[m]: ' : self.max_altitude
        }

        info_str = [f'{key}{value}' for key, value in info.items() if value is not None]
        return 'Drone information:\n' + '\n'.join(info_str) if info_str else 'no information given'

class Drone:
    def __init__(self, name, reliability, type: Type, information: DroneInformation = None, description = None):
        self.name = name
        self.reliability = reliability
        self.description = description
        self.type = type
        self.information = information

    def __str__(self):
        drone_str = f'Drone: {self.name} ({self.description})' if self.description else f'Drone {self.name}'
        info_str = f'\n----------------------\n{self.information}' if self.information else ''
        
        return f'\n{drone_str} \nReliability = {self.reliability}\n{self.type}{info_str}'
