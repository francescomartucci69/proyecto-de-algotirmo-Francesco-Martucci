class Producto:
    """
    Clase que representa un producto con sus atributos principales.
    
    Atributos:
        nombre (str): El nombre del producto.
        cantidad (int): La cantidad del producto.
        precio (float): El precio del producto.
        stock (int): La cantidad de stock disponible del producto.
    """
    def __init__(self, nombre, cantidad, precio, stock):
        """
        Inicializa una instancia de la clase Producto.
        
        Args:
            nombre (str): El nombre del producto.
            cantidad (int): La cantidad del producto.
            precio (float): El precio del producto.
            stock (int): La cantidad de stock disponible del producto.
        """
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.stock = stock
    
    def mostrar_atributos(self):
        """
        Muestra los atributos del producto.
        
        Returns:
            str: Una cadena con el nombre, el stock y el precio del producto.
        """
        return f"-Nombre: {self.nombre}\n-Stock: {self.stock}\n-Precio: {self.precio}"
    
    def verificar_stock(self):
        """
        Verifica si hay stock disponible del producto.
        
        Returns:
            bool: True si hay stock disponible, False de lo contrario.
        """
        if self.stock > 0:
            return True
        else:
            return False
        
    def diccionario(self):
        """
        Crea un diccionario con los atributos del producto.
        
        Returns:
            dict: Un diccionario con los atributos del producto.
        """
        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "stock": self.stock
        }


        