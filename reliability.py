import math

# ci treba zadavat strukturu alebo nie
class Calculation:
    def __init__(self, structure: str, number_of_drones, number_of_types, connection_type, number_of_redundant = None, cu_reliability = None):
        self.structure = structure
        self.number_of_drones = number_of_drones
        self.number_of_types = number_of_types
        self.connection_type = connection_type
        self.number_of_redundant = number_of_redundant
        self.cu_reliability = cu_reliability

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
        self.calculate()

    def calculate(self):
        print(f'''structure: {self.structure}, n: {self.number_of_drones}, K: {self.number_of_types}, 
              connection type: {self.connection_type}, redundantnych: {self.number_of_redundant}, pCU: {self.cu_reliability}''')
        
        structure_parts = self.structure.split('_')
        connection = 'centralized' if self.cu_reliability else 'decentralized'
        operation = '_'.join([structure_parts[0], structure_parts[-1], connection])
        print(operation)
        

# pocet dronov, typ drona (z db spolahlivost)
    # pocet dronov n
    # spolahlivost dronov p
    def a_hoid(n: int, p: float) -> float:
        return p ** n

# pocet dronov, typ drona (z db spolahlivost), pr CU
    # pocet dronov n
    # spolahlivost CU pn
    # spolahlivost dronov p
    def a_hoic(n: int, pn: float, p: float) -> float:
        return math.pow(p, n - 1) * pn

# pocet dronov, typ drona (z db spolahlivost) + pocet pracujucich k typu, 
    # pocet dronov n
    # pocet funkcnych/pracujucich dronov v MDF k
    # pravdepodobnost dronov p
    def a_hord(n: int, k: int, p: float) -> float:
        return sum(math.comb(n, s) * math.pow(p, s) * math.pow(1 - p, n - s) for s in range(k, n + 1))

# pocet dronov, typ drona (z db spolahlivost) + pocet pracujucich k typu, pr CU
    # pocet dronov n
    # pocet funkcnych/pracujucich dronov v MDF k
    # pravdepodobnost dronov p
    # spolahlivost CU pn
    def a_horc(n: int, k: int, p: float, pn: float) -> float:
        return pn * sum(math.comb(n - 1, s) * math.pow(p, s) * math.pow(1 - p, n - s) for s in range(k, n))
    
# pocet dronov, typy dronov (list, odtial aj z db spolahlivost) + odtial pocet, pocty dronov typu (list),
    # pocet typov dronov K
    # pocet dronov typu r lr
    # spolahlivost dronov typu r pr
    def a_heid(K: int) -> float:
        result: float = 1.0
        # for r in range(1, K + 1):
        #     result *= pr ** lr
        return result

# typy dronov (list, odtial aj z db spolahlivost) + odtial pocet, pocty dronov typu (list), pr CU
    # pocet typov dronov K
    # pocet dronov typu r lr
    # spolahlivost dronov typu r pr
    # spolahlivost CU pn
    def a_heic(K: int, pn: float) -> float:
        result: float = 1.0
        # for r in range(1, K + 1):
        #     result *= pr ** lr
        return result * pn

# typy dronov (list, odtial aj z db spolahlivost) + odtial pocet, pocty dronov typu (list) + pocty pracujucich kazdeho typu,
    # pocet typov dronov K
    # celkovy pocet dronov typu r lr
    # pocet funkcnych/pracujucich dronov typu r v MDF kr
    # spolahlivost dronov typu r pr
    def a_herd(K: int) -> float:
        result: float = 1.0 # product , has to be 1 I guess
        for r in range(K + 1):
            temp: float = 0.0
            # for s in range(kr, lr + 1):
            #     comb: float = math.comb(lr, s)
            #     temp += comb * (pr ** s) * ((1 - pr) ** (lr - s))
            result *= temp
        return result
    
# typy dronov (list, odtial aj z db spolahlivost) + odtial pocet, pocty dronov typu (list) + pocty pracujucich kazdeho typu, pr CU
    # pocet typov dronov K
    # celkovy pocet dronov typu r lr
    # pocet funkcnych/pracujucich dronov typu r v MDF kr
    # spolahlivost dronov typu r pr
    # spolahlivost CU pn
    def a_herc(K: int, pn: float) -> float:
        result: float = 1.0 # product , has to be 1 I guess
        for r in range(r, K + 1):
            temp: float = 0.0
            # for s in range(kr, lr + 1):
            #     comb: float = math.comb(lr, s)
            #     temp += comb * (pr ** s) * ((1 - pr) ** (lr - s))
            result *= temp
        return result * pn