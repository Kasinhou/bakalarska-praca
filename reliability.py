import math
from data_manager import DataManager

class Calculation:
    def __init__(self, swarmInfo):
        self.swarmInfo = swarmInfo
        data_manager = DataManager()
        # data_manager.get_all_information()
        self.drones = data_manager.get_drones()
        data_manager.close_connection()

        self.operations = {
            "homogenous_irredundant_decentralized": self.a_hoid,
            "homogenous_irredundant_centralized": self.a_hoic,
            "homogenous_redundant_decentralized": self.a_hord,
            "homogenous_redundant_centralized": self.a_horc,
            "heterogenous_irredundant_decentralized": self.a_heid,
            "heterogenous_irredundant_centralized": self.a_heic,
            "heterogenous_redundant_decentralized": self.a_herd,
            "heterogenous_redundant_centralized": self.a_herc,
        }

    def validate_data(self):
        pass

    def calculate(self):
        print(self.swarmInfo)
        structure_parts = self.swarmInfo['structure'].split('_')
        operation = '_'.join([structure_parts[0], structure_parts[-1], self.swarmInfo['connection']])
        print(operation)
        print('Reliability of this structure is: ' + str(self.operations[operation]()))
        

    # pocet dronov n
    # spolahlivost dronov p
    def a_hoid(self) -> float:
        droneName = self.swarmInfo['typesInfo'][0]['droneType']
        reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
        if reliability is None:
            print('Problem heree')
            return 0
        return reliability ** int(self.swarmInfo['dronesCount'])

    # pocet dronov n
    # spolahlivost CU pn
    # spolahlivost dronov p
    def a_hoic(self) -> float:
        droneName = self.swarmInfo['typesInfo'][0]['droneType']
        reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
        if reliability is None:
            print('Problem heree')
            return 0
        return math.pow(reliability, int(self.swarmInfo['dronesCount']) - 1) * float(self.swarmInfo['cuReliability'])

    # pocet dronov n
    # pocet pracujucich dronov v MDF k
    # pravdepodobnost dronov p
    def a_hord(self) -> float:
        n = int(self.swarmInfo['dronesCount'])
        droneName = self.swarmInfo['typesInfo'][0]['droneType']
        p = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
        k = int(self.swarmInfo['typesInfo'][0]['redundantCount'])
        return sum(math.comb(n, s) * math.pow(p, s) * math.pow(1 - p, n - s) for s in range(k, n + 1)) 

    # pocet dronov n
    # pocet pracujucich dronov v MDF k
    # pravdepodobnost dronov p
    # spolahlivost CU pn
    def a_horc(self) -> float:
        n = int(self.swarmInfo['dronesCount'])
        droneName = self.swarmInfo['typesInfo'][0]['droneType']
        p = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
        k = int(self.swarmInfo['typesInfo'][0]['redundantCount'])
        return float(self.swarmInfo['cuReliability']) * sum(math.comb(n - 1, s) * math.pow(p, s) * math.pow(1 - p, n - s) for s in range(k, n))
    
    # pocet typov dronov K
    # pocet dronov typu r lr
    # spolahlivost dronov typu r pr
    def a_heid(self) -> float:
        result: float = 1.0
        for r in range(int(self.swarmInfo['typesCount'])):
            droneName = self.swarmInfo['typesInfo'][r]['droneType']
            numberOfType = int(self.swarmInfo['typesInfo'][r]['typeCount'])
            reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
            result *= reliability ** numberOfType
        return result

    # pocet typov dronov K
    # pocet dronov typu r lr
    # spolahlivost dronov typu r pr
    # spolahlivost CU pn
    def a_heic(self) -> float:
        result: float = 1.0
        for r in range(int(self.swarmInfo['typesCount'])):
            droneName = self.swarmInfo['typesInfo'][r]['droneType']
            numberOfType = int(self.swarmInfo['typesInfo'][r]['typeCount'])
            reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
            result *= reliability ** numberOfType
        return result * float(self.swarmInfo['cuReliability'])

    # pocet typov dronov K
    # celkovy pocet dronov typu r lr
    # pocet pracujucich dronov typu r v MDF kr
    # spolahlivost dronov typu r pr
    def a_herd(self) -> float:
        result: float = 1.0
        for r in range(int(self.swarmInfo['typesCount'])):
            droneName = self.swarmInfo['typesInfo'][r]['droneType']
            numberOfType = int(self.swarmInfo['typesInfo'][r]['typeCount'])
            reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
            redundant = int(self.swarmInfo['typesInfo'][r]['redundantCount'])
            tempSum: float = 0.0
            for s in range(redundant, numberOfType + 1):
                comb: float = math.comb(numberOfType, s)
                tempSum += comb * (reliability ** s) * ((1 - reliability) ** (numberOfType - s))
            result *= tempSum
        return result
    
    # pocet typov dronov K
    # celkovy pocet dronov typu r lr
    # pocet pracujucich dronov typu r v MDF kr
    # spolahlivost dronov typu r pr
    # spolahlivost CU pn
    def a_herc(self) -> float:
        result: float = 1.0
        for r in range(int(self.swarmInfo['typesCount'])):
            droneName = self.swarmInfo['typesInfo'][r]['droneType']
            numberOfType = int(self.swarmInfo['typesInfo'][r]['typeCount'])
            reliability = next((drone[1] for drone in self.drones if drone[0] == droneName), None)
            redundant = int(self.swarmInfo['typesInfo'][r]['redundantCount'])
            tempSum: float = 0.0
            for s in range(redundant, numberOfType + 1):
                comb: float = math.comb(numberOfType, s)
                tempSum += comb * (reliability ** s) * ((1 - reliability) ** (numberOfType - s))
            result *= tempSum
        return result * float(self.swarmInfo['cuReliability'])