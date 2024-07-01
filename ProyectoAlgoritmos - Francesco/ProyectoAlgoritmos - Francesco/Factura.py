class Factura:
    """
    Clase que representa una factura para un cliente por un partido y productos de un restaurante.
    
    Atributos:
        cliente (Cliente): El cliente al que se le emite la factura.
        partido (Partido): El partido relacionado con la factura.
        restaurant (Restaurante): El restaurante del cual se compraron los productos.
        detalles_productos (list): Una lista de detalles de los productos comprados.
        subtotal (float): El subtotal de la factura antes de descuentos.
        descuento (float): El descuento aplicado a la factura.
        total (float): El total a pagar después del descuento.
    """
    def __init__(self, cliente, partido, restaurant, detalles_productos, subtotal, descuento, total):
        """
        Inicializa una instancia de la clase Factura.
        
        Args:
            cliente (Cliente): El cliente al que se le emite la factura.
            partido (Partido): El partido relacionado con la factura.
            restaurant (Restaurante): El restaurante del cual se compraron los productos.
            detalles_productos (list): Una lista de detalles de los productos comprados.
            subtotal (float): El subtotal de la factura antes de descuentos.
            descuento (float): El descuento aplicado a la factura.
            total (float): El total a pagar después del descuento.
        """
        self.cliente = cliente
        self.partido = partido
        self.restaurant = restaurant
        self.detalles_productos = detalles_productos
        self.subtotal = subtotal
        self.descuento = descuento
        self.total = total

    def producto_en_factura(self, producto):
        cantidad = 0
        for detalle in self.detalles_productos:
            if detalle[0].nombre == producto.nombre:
                cantidad += detalle[1]
        
        return cantidad
    
    
    def convertir_detalles_producto(self):
        detalles_productos = []

        for detalle in self.detalles_productos:
            detalles_productos.append((detalle[0].nombre, detalle[1]))

        return detalles_productos

    def diccionario(self):
        return {
            'cliente': self.cliente.cedula,
            'partido': self.partido.id,
            'restaurant': self.restaurant.nombre,
            'detalles_productos': self.convertir_detalles_producto(),
            'subtotal': self.subtotal,
            'descuento': self.descuento,
            'total': self.total,
        }