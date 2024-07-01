class Equipo:
    def __init__(self, id, codigo, nombre, grupo):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.grupo = grupo
    
    def mostrar_atributos(self):
        return f"-id: {self.id}\n-Codigo: {self.codigo}\n-Nombre: {self.nombre}\n-Grupo: {self.grupo}\n"
    
    def mostrar(self):
        return f"-Nombre: {self.nombre}\n-Codigo: {self.codigo}\n-Grupo: {self.grupo}\n"
    
    def diccionario(self):
        return {"id": self.id, "codigo": self.codigo, "nombre": self.nombre, "grupo": self.grupo}
    
    
    