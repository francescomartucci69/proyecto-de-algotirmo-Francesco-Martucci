from Producto import Producto

class Alimento(Producto):
    """
    Clase que representa un alimento, heredando de la clase Producto.
    
    Atributos:
        nombre (str): El nombre del alimento.
        cantidad (int): La cantidad del alimento.
        precio (float): El precio del alimento.
        stock (int): La cantidad de stock disponible del alimento.
        plato (bool): Indica si el alimento es un plato preparado o un paquete.
    """
    def __init__(self, nombre, cantidad, precio, stock, plato):
        """
        Inicializa una instancia de la clase Alimento.
        
        Args:
            nombre (str): El nombre del alimento.
            cantidad (int): La cantidad del alimento.
            precio (float): El precio del alimento.
            stock (int): La cantidad de stock disponible del alimento.
            plato (bool): Indica si el alimento es un plato preparado o un paquete.
        """
        super().__init__(nombre, cantidad, precio, stock)
        self.plato = plato
    
    def mostrar_atributos(self):
        """
        Muestra los atributos del alimento, incluyendo si es un plato preparado o un paquete.
        
        Returns:
            str: Una cadena con el nombre, el stock, el precio y si es un plato preparado o un paquete.
        """
        if self.plato:
            return super().mostrar_atributos() + f"\n-Adicional: Plato\n"
        else:
            return super().mostrar_atributos() + f"\n-Adicional: Paquete\n"
        
    def verificar_stock(self):
        """
        Verifica si hay stock disponible del alimento.
        
        Returns:
            bool: True si hay stock disponible, False de lo contrario.
        """
        return super().verificar_stock()
    
    def diccionario(self):
        """
        Crea un diccionario con los atributos del alimento.
        
        Returns:
            dict: Un diccionario con los atributos del alimento.
        """

        if self.plato:
            return {
                'nombre': self.nombre,
                'cantidad': self.cantidad,
                'stock': self.stock,
                'precio': self.precio,
                'adicional': "plate",
            }
        else:
            return {
                'nombre': self.nombre,
                'cantidad': self.cantidad,
                'stock': self.stock,
                'precio': self.precio,
                'adicional': "package",
            }
        
