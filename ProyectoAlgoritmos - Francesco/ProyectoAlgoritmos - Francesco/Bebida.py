from Producto import Producto

class Bebida(Producto):
    """
    Clase que representa una bebida, heredando de la clase Producto.
    
    Atributos:
        nombre (str): El nombre de la bebida.
        cantidad (int): La cantidad de la bebida.
        precio (float): El precio de la bebida.
        stock (int): La cantidad de stock disponible de la bebida.
        alcoholica (bool): Indica si la bebida es alcohólica o no.
    """
    def __init__(self, nombre, cantidad, precio, stock, alcoholica):
        """
        Inicializa una instancia de la clase Bebida.
        
        Args:
            nombre (str): El nombre de la bebida.
            cantidad (int): La cantidad de la bebida.
            precio (float): El precio de la bebida.
            stock (int): La cantidad de stock disponible de la bebida.
            alcoholica (bool): Indica si la bebida es alcohólica o no.
        """
        super().__init__(nombre, cantidad, precio, stock)
        self.alcoholica = alcoholica
    
    def mostrar_atributos(self):
        """
        Muestra los atributos de la bebida, incluyendo si es alcohólica o no.
        
        Returns:
            str: Una cadena con el nombre, el stock, el precio y si es alcohólica o no.
        """
        if self.alcoholica:
            return super().mostrar_atributos() + f"\n-Adicional: Alcoholica\n"
        else:
            return super().mostrar_atributos() + f"\n-Adicional: No alcoholica\n"
        
    def verificar_stock(self):
        """
        Verifica si hay stock disponible de la bebida.
        
        Returns:
            bool: True si hay stock disponible, False de lo contrario.
        """
        return super().verificar_stock()
    
    def diccionario(self):
        """
        Crea un diccionario con los atributos de la bebida.
        
        Returns:
            dict: Un diccionario con los atributos de la bebida.
        """
        if self.alcoholica:
            return {
                "nombre": self.nombre,
                "stock": self.stock,
                "cantidad": self.cantidad,
                "precio": self.precio,
                "adicional": "alcoholic"
            }
        else:
            return {
                "nombre": self.nombre,
                "stock": self.stock,
                "cantidad": self.cantidad,
                "precio": self.precio,
                "adicional": "non-alcoholic"
            }
