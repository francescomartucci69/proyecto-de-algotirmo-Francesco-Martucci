class Estadio:
    """
    Clase que representa un estadio, incluyendo su información básica, mapas de asientos y restaurantes.
    
    Atributos:
        id (int): El identificador del estadio.
        nombre (str): El nombre del estadio.
        ciudad (str): La ciudad donde se encuentra el estadio.
        mapaGnral (list): El mapa de asientos de la zona general.
        mapaVip (list): El mapa de asientos de la zona VIP.
        restaurantes (list): Una lista de restaurantes dentro del estadio.
    """
    def __init__(self, id, nombre, ciudad, mapaGnral, mapaVip, restaurantes):
        """
        Inicializa una instancia de la clase Estadio.
        
        Args:
            id (int): El identificador del estadio.
            nombre (str): El nombre del estadio.
            ciudad (str): La ciudad donde se encuentra el estadio.
            mapaGnral (list): El mapa de asientos de la zona general.
            mapaVip (list): El mapa de asientos de la zona VIP.
            restaurantes (list): Una lista de restaurantes dentro del estadio.
        """
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.mapaGnral = mapaGnral
        self.mapaVip = mapaVip
        self.restaurantes = restaurantes
    
    def mostrar_mapas(self):
        """
        Muestra los mapas de asientos tanto de la zona general como de la zona VIP.
        """
        self.mostrar_mapa_gnral()
        print("\n")
        self.mostrar_mapa_vip()

    def mostrar_mapa_gnral(self):
        """
        Genera una representación en cadena del mapa de asientos de la zona general.
        
        Returns:
            str: Una cadena que representa el mapa de la zona general.
        """
        mapa_gnral = "General\n"
        for i in range(len(self.mapaGnral)):
            if i < 10:
                mapa_gnral += f"Fila 0{i+1}:\n"
            else:
                mapa_gnral += f"Fila {i+1}:\n"

            for j in self.mapaGnral[i]:
                if j != "XX":
                    if int(j) < 10:
                        mapa_gnral += f"0{j} "
                    else:
                        mapa_gnral += f"{j} "
                else:
                    mapa_gnral += f"{j} "
            mapa_gnral += "\n"
            
        return mapa_gnral

    def mostrar_mapa_vip(self):
        """
        Genera una representación en cadena del mapa de asientos de la zona VIP.
        
        Returns:
            str: Una cadena que representa el mapa de la zona VIP.
        """
        mapa_vip = "VIP\n"
        for i in range(len(self.mapaVip)):
            if i < 10:
                mapa_vip += f"Fila 0{i+1}:\n"
            else:
                mapa_vip += f"Fila {i+1}:\n"

            for j in self.mapaVip[i]:
                if j != "XX":
                    if int(j) < 10:
                        mapa_vip += f"0{j} "
                    else:
                        mapa_vip += f"{j} "
                else:
                    mapa_vip += f"{j} "
            mapa_vip += "\n"

        return mapa_vip

    def verificar_fila_llena(self, fila, tipo_entrada):
        """
        Verifica si una fila específica está completamente ocupada.
        
        Args:
            fila (int): El número de fila a verificar.
            tipo_entrada (str): El tipo de entrada, puede ser "General" o "VIP".
        
        Returns:
            bool: True si la fila está completamente ocupada, False de lo contrario.
        """
        if tipo_entrada == "General":
            count = 0
            for i in self.mapaGnral[fila]:
                if i == "XX":
                    count += 1
            if count == len(self.mapaGnral[fila]):
                return True
            else:
                return False
        else:
            count = 0
            for i in self.mapaVip[fila]:
                if i == "XX":
                    count += 1
            if count == len(self.mapaVip[fila]):
                return True
            else:
                return False
    
    def asiento_ocupado(self, fila, asiento, tipo_entrada):
        """
        Verifica si un asiento específico está ocupado.
        
        Args:
            fila (int): El número de fila del asiento.
            asiento (int): El número del asiento.
            tipo_entrada (str): El tipo de entrada, puede ser "General" o "VIP".
        
        Returns:
            bool: True si el asiento está ocupado, False de lo contrario.
        """
        if tipo_entrada == "General":
            if self.mapaGnral[fila][asiento] != "XX":
                return False
            else:
                return True
        else:
            if self.mapaVip[fila][asiento] != "XX":
                return False
            else:
                return True
            
    def ocupar_asiento(self, fila, asiento, tipo_entrada):
        """
        Marca un asiento específico como ocupado.
        
        Args:
            fila (int): El número de fila del asiento.
            asiento (int): El número del asiento.
            tipo_entrada (str): El tipo de entrada, puede ser "General" o "VIP".
        """
        if tipo_entrada == "General":
            self.mapaGnral[fila][asiento] = "XX"
        else:
            self.mapaVip[fila][asiento] = "XX"

    def mostrar_restaurantes(self):
        """
        Muestra los atributos de cada restaurante en el estadio.
        """
        for restaurante in self.restaurantes:
            print(restaurante.mostrar_atributos())

    def mostrar(self):
        """
        Muestra el nombre y la ubicación del estadio.
        
        Returns:
            str: Una cadena con el nombre y la ciudad del estadio.
        """
        return f"-Nombre: {self.nombre}\n-Ubicacion: {self.ciudad}\n"
    
    def disponibilidad_restaurant(self):
        """
        Verifica si hay disponibilidad de productos en los restaurantes del estadio.
        
        Returns:
            bool: True si al menos un restaurante tiene productos disponibles, False de lo contrario.
        """
        count = 0
        for restaurante in self.restaurantes:
            if restaurante.verificar_stock_productos():
                count += 1
        
        if count == 0:
            return False
        else:
            return True
        
    def calcular_capacidad(self):
        capacidad_general = 0
        capacidad_vip = 0
        
        for i in range(len(self.mapaGnral)):
            for j in range(len(self.mapaGnral[i])):
                capacidad_general += 1
        
        for i in range(len(self.mapaVip)):
            for j in range(len(self.mapaVip[i])):
                capacidad_vip += 1

        capacidad = [capacidad_general, capacidad_vip]
        
        return capacidad
    
    def convertir_restaurants(self):
        restaurants = []
        for restaurante in self.restaurantes:
            restaurants.append(restaurante.diccionario())
        
        return restaurants
        
    def diccionario(self):
        """
        Crea un diccionario con los datos de la instancia de la clase Estadio.
        
        Returns:
            dict: Un diccionario con los atributos de la instancia.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "capacidad": self.calcular_capacidad() ,
            "restaurantes": self.convertir_restaurants()
        }
