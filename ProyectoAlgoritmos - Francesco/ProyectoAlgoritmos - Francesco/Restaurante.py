class Restaurante:
    """
    Clase que representa un restaurante con una lista de productos.
    
    Atributos:
        nombre (str): El nombre del restaurante.
        productos (list): Una lista de productos disponibles en el restaurante.
    """
    def __init__(self, nombre, productos):
        """
        Inicializa una instancia de la clase Restaurante.
        
        Args:
            nombre (str): El nombre del restaurante.
            productos (list): Una lista de productos disponibles en el restaurante.
        """
        self.nombre = nombre
        self.productos = productos
    
    def mostrar_atributos(self):
        """
        Muestra los atributos del restaurante, incluyendo su nombre y los productos disponibles.
        """
        print(f"Nombre: {self.nombre}")
        print(f"Productos:\n")
        self.mostrar_productos()

    def mostrar_productos(self):
        """
        Muestra los atributos de cada producto disponible en el restaurante.
        """
        for producto in self.productos:
            producto.mostrar_atributos()

    def verificar_stock_productos(self):
        """
        Verifica si hay stock disponible de algún producto en el restaurante.
        
        Returns:
            bool: True si al menos un producto tiene stock disponible, False de lo contrario.
        """
        count = 0
        for producto in self.productos:
            if producto.verificar_stock():
                count += 1
        
        if count != 0:
            return True
        else:
            return False
        
    def convertir_productos(self):
        productos = []
        for producto in self.productos:
            productos.append(producto.diccionario())
        
        return productos

    def diccionario(self):
        return {
            "nombre": self.nombre,
            "productos": self.convertir_productos()
        }

            