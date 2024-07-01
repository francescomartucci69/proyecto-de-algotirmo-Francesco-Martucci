class Partido:
    """
    Clase que representa un partido de fútbol con detalles sobre los equipos, la fecha, el grupo y el estadio.
    
    Atributos:
        id (int): El identificador del partido.
        numero (int): El número del partido.
        equipoLocal (Equipo): El equipo local del partido.
        equipoVisitante (Equipo): El equipo visitante del partido.
        fecha (str): La fecha en la que se juega el partido.
        grupo (str): El grupo al que pertenece el partido.
        estadio (Estadio): El estadio donde se juega el partido.
    """
    def __init__(self, id, numero, equipoLocal, equipoVisitante, fecha, grupo, estadio):
        """
        Inicializa una instancia de la clase Partido.
        
        Args:
            id (int): El identificador del partido.
            numero (int): El número del partido.
            equipoLocal (Equipo): El equipo local del partido.
            equipoVisitante (Equipo): El equipo visitante del partido.
            fecha (str): La fecha en la que se juega el partido.
            grupo (str): El grupo al que pertenece el partido.
            estadio (Estadio): El estadio donde se juega el partido.
        """
        self.id = id
        self.numero = numero
        self.equipoLocal = equipoLocal
        self.equipoVisitante = equipoVisitante
        self.fecha = fecha
        self.grupo = grupo
        self.estadio = estadio
    
    def mostrar_atributo(self):
        """
        Muestra los atributos del partido, incluyendo detalles de los equipos, la fecha, el grupo y el estadio.
        """
        print(f"Id: {self.id}\nNumero: {self.numero}\nEquipo Local:")
        print(self.equipoLocal.mostrar_atributo())
        print(f"Equipo Visitante:")
        print(self.equipoVisitante.mostrar_atributo())
        print(f"Fecha: {self.fecha}\nGrupo: {self.grupo}\nEstadio:\n")
        print(self.estadio.mostrar_atributo())
    
    def mostrar(self):
        """
        Muestra un resumen del partido, incluyendo los nombres de los equipos, la fecha y el estadio.
        
        Returns:
            str: Una cadena con los nombres de los equipos, la fecha y el estadio del partido.
        """
        return f"Equipo Local: {self.equipoLocal.nombre}\nEquipo Visitante: {self.equipoVisitante.nombre}\nFecha: {self.fecha}\nEstadio:\n{self.estadio.mostrar()}"
    
    def mostrar_est(self):
        return f"{self.equipoLocal.nombre} vs {self.equipoVisitante.nombre}.\nEstadio:{self.estadio.nombre}"
    
    def diccionario(self):
        """
        Construye un diccionario con los atributos del partido.
        
        Returns:
            dict: Un diccionario con los atributos del partido.
        """
        return {
            'id': self.id,
            'numero': self.numero,
            'equipo_local': self.equipoLocal.id,
            'equipo_visitante': self.equipoVisitante.id,
            'fecha': self.fecha,
            'grupo': self.grupo,
            'estadio': self.estadio.id
        }
    

