class Cliente:
    """
    Clase que representa un cliente con su información personal.
    
    Atributos:
        nombre (str): El nombre del cliente.
        cedula (str): La cédula de identidad del cliente.
        edad (int): La edad del cliente.
    """
    def __init__(self, nombre, cedula, edad):
        """
        Inicializa una instancia de la clase Cliente.
        
        Args:
            nombre (str): El nombre del cliente.
            cedula (str): La cédula de identidad del cliente.
            edad (int): La edad del cliente.
        """
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

    def mostrar_atributos(self):
        """
        Muestra los atributos del cliente.
        
        Returns:
            str: Una cadena con el nombre, la cédula y la edad del cliente.
        """
        return f"-Nombre: {self.nombre}\n-Cedula: {self.cedula}\n-Edad: {self.edad}\n"
    
    def diccionario(self):
        """
        Crea un diccionario con los atributos del cliente.
        
        Returns:
            dict: Un diccionario con los atributos del cliente.
        """
        return {"nombre": self.nombre, "cedula": self.cedula, "edad": self.edad}
