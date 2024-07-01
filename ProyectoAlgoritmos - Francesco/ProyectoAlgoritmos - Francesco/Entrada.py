class Entrada:
    """
    Clase que representa una entrada para un partido de fútbol.
    
    Atributos:
        id (int): El identificador de la entrada.
        cliente (Cliente): El cliente que compró la entrada.
        partido (Partido): El partido para el cual es la entrada.
        tipo_entrada (str): El tipo de entrada (por ejemplo, General o VIP).
        asiento (tuple): La ubicación del asiento en el estadio.
        descuento (float): El porcentaje de descuento aplicado a la entrada.
        total_descuento (float): El monto total de descuento aplicado.
        iva (float): El monto del IVA aplicado.
        total (float): El total a pagar por la entrada después de descuentos e IVA.
        asistencia (bool): Indica si el cliente asistió al partido o no.
    """
    def __init__(self, id, cliente, partido, tipo_entrada, asiento, subtotal, descuento, total_descuento, iva, total, asistencia):
        """
        Inicializa una instancia de la clase Entrada.
        
        Args:
            id (int): El identificador de la entrada.
            cliente (Cliente): El cliente que compró la entrada.
            partido (Partido): El partido para el cual es la entrada.
            tipo_entrada (str): El tipo de entrada (por ejemplo, General o VIP).
            asiento (tuple): La ubicación del asiento en el estadio.
            descuento (float): El porcentaje de descuento aplicado a la entrada.
            total_descuento (float): El monto total de descuento aplicado.
            iva (float): El monto del IVA aplicado.
            total (float): El total a pagar por la entrada después de descuentos e IVA.
            asistencia (bool): Indica si el cliente asistió al partido o no.
        """
        self.id = id
        self.cliente = cliente
        self.partido = partido
        self.tipo_entrada = tipo_entrada
        self.asiento = asiento
        self.subtotal = subtotal 
        self.descuento = descuento
        self.total_descuento = total_descuento
        self.iva = iva
        self.total = total
        self.asistencia = asistencia
    
    def mostrar(self):
        """
        Muestra un resumen de la entrada, incluyendo el cliente, el partido y la ubicación del asiento.
        
        Returns:
            str: Una cadena con los detalles de la entrada.
        """
        return f"\n-Id: {self.id}\n-Cliente: {self.cliente.nombre}\n-Partido: {self.partido.equipoLocal.nombre} vs {self.partido.equipoVisitante.nombre}\n-Asiento: {self.asiento[0]}, {self.asiento[1]}\n"

    def diccionario(self):
        """
        Construye un diccionario con los detalles de la entrada, incluyendo el cliente, el partido y la ubicación del asiento.
        
        Returns:
            dict: Un diccionario con los detalles de la entrada.
        """
        return {
            'id': self.id,
            'cliente': self.cliente.cedula,
            'partido': f"{self.partido.id}",
            'asiento': f"{self.asiento[0]}, {self.asiento[1]}",
            'tipo_entrada': self.tipo_entrada,
            'subtotal': self.subtotal,
            'descuento': self.descuento,
            'total_descuento': self.total_descuento,
            'iva': self.iva,
            'total': self.total,
            'asistencia': self.asistencia
        }