from Alimento import Alimento
from Bebida import Bebida
from Cliente import Cliente
from Entrada import Entrada
from Equipo import Equipo
from Estadio import Estadio
from Factura import Factura
from Partido import Partido
from Producto import Producto
from Restaurante import Restaurante
import requests
import json
import os

class App:
    """
    Clase principal que representa la aplicación que maneja equipos, estadios, restaurantes, productos, partidos, entradas, facturas y clientes.
    
    Atributos:
        equipos (list): Lista de equipos.
        estadios (list): Lista de estadios.
        restaurantes (list): Lista de restaurantes.
        productos (list): Lista de productos.
        partidos (list): Lista de partidos.
        entradas (list): Lista de entradas.
        facturas (list): Lista de facturas.
        clientes (list): Lista de clientes.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase App con listas vacías para cada tipo de entidad.
        """
        self.equipos = []
        self.estadios = []
        self.restaurantes = []
        self.productos = []
        self.partidos = []
        self.entradas = []
        self.facturas = []
        self.clientes = []

    
    def cargar_Equipos(self):
        """
        Carga los equipos desde una API y los añade a la lista de equipos de la aplicación.
        
        Obtiene los datos de los equipos desde una API, crea instancias de la clase Equipo con los datos recibidos
        y las añade a la lista de equipos de la aplicación.
        """
        # Realiza una solicitud GET a la URL de la API que contiene los datos de los equipos
        api = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json")
        
        # Convierte la respuesta de la API a formato JSON
        datos = api.json()

        # Itera sobre la lista de datos obtenidos de la API
        for info in datos:
            # Extrae la información de cada equipo
            id = info["id"]
            codigo = info["code"]
            nombre = info["name"]
            grupo = info["group"]

            # Crea una instancia de la clase Equipo con la información extraída
            equipo = Equipo(id, codigo, nombre, grupo)
            
            # Añade el equipo a la lista de equipos de la aplicación
            self.equipos.append(equipo)


    def llenar_mapa(self, capacidad):
        """
        Llena un mapa de asientos para un estadio basado en la capacidad dada.

        Args:
            capacidad (int): La capacidad del mapa de asientos.

        Returns:
            list: Una lista de listas que representa el mapa de asientos.
        """
        mapa = []
        count = 1

        # Rellena el mapa de asientos hasta alcanzar la capacidad dada
        while count <= capacidad:
            lista = []
            sub_count = 0
            
            # Añade hasta 10 asientos por fila, o hasta que se alcance la capacidad
            while sub_count < 10 and count <= capacidad:
                lista.append(str(sub_count + 1))
                count += 1
                sub_count += 1
            
            mapa.append(lista)
        
        return mapa

    def cargar_Estadios(self):
        """
        Carga los estadios desde una API y los añade a la lista de estadios de la aplicación.
        
        Obtiene los datos de los estadios desde una API, crea instancias de la clase Estadio con los datos recibidos
        y las añade a la lista de estadios de la aplicación.
        """
        # Realiza una solicitud GET a la URL de la API que contiene los datos de los estadios
        api = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
        
        # Convierte la respuesta de la API a formato JSON
        datos = api.json()

        # Itera sobre la lista de datos obtenidos de la API
        for info in datos:
            # Extrae la información de cada estadio
            id = info["id"]
            nombre = info["name"]
            ciudad = info["city"]
            mapaGnral = self.llenar_mapa(info["capacity"][0])  # Llenar mapa de asientos general
            mapaVip = self.llenar_mapa(info["capacity"][1])  # Llenar mapa de asientos VIP

            lista_restaurantes = []

            # Itera sobre la lista de restaurantes dentro del estadio
            for info_rest in info["restaurants"]:
                nombreRest = info_rest["name"]
                lista_productos = []

                # Itera sobre la lista de productos dentro de cada restaurante
                for info_prod in info_rest["products"]:
                    nombreProd = info_prod["name"]
                    cantidad = info_prod["quantity"]
                    precio = float(info_prod["price"]) + (float(info_prod["price"]) * 0.16)  # Añadir IVA al precio
                    stock = int(info_prod["stock"])

                    # Verifica si el producto es un alimento
                    if info_prod["adicional"] == "plate" or info_prod["adicional"] == "package":
                        plato = False

                        if info_prod["adicional"] == "plate":
                            plato = True
                        
                        alimento = Alimento(nombreProd, cantidad, precio, stock, plato)
                        lista_productos.append(alimento)
                        self.productos.append(alimento)
                    else:  # El producto es una bebida
                        alcoholica = False

                        if info_prod["adicional"] == "alcoholic":
                            alcoholica = True
                        
                        bebida = Bebida(nombreProd, cantidad, precio, stock, alcoholica)
                        lista_productos.append(bebida)
                        self.productos.append(bebida)
                
                # Crear una instancia de Restaurante con los productos y añadirla a la lista
                restaurante = Restaurante(nombreRest, lista_productos)
                lista_restaurantes.append(restaurante)
                self.restaurantes.append(restaurante)
            
            # Crear una instancia de Estadio con los datos obtenidos y añadirla a la lista
            estadio = Estadio(id, nombre, ciudad, mapaGnral, mapaVip, lista_restaurantes)
            self.estadios.append(estadio)

    
    def buscar_equipo_id(self, id):
        """
        Busca un equipo por su ID en la lista de equipos.

        Args:
            id (str): El identificador del equipo a buscar.

        Returns:
            Equipo: El equipo con el ID especificado, o None si no se encuentra.
        """
        # Itera sobre la lista de equipos para encontrar el equipo con el ID dado
        for equipo in self.equipos:
            if equipo.id == id:
                return equipo
        return None

    def buscar_estadio_id(self, id):
        """
        Busca un estadio por su ID en la lista de estadios.

        Args:
            id (int): El identificador del estadio a buscar.

        Returns:
            Estadio: El estadio con el ID especificado, o None si no se encuentra.
        """
        # Itera sobre la lista de estadios para encontrar el estadio con el ID dado
        for estadio in self.estadios:
            if estadio.id == id:
                return estadio
        return None

    def cargar_Partidos(self):
        """
        Carga los partidos desde una API y los añade a la lista de partidos de la aplicación.
        
        Obtiene los datos de los partidos desde una API, crea instancias de la clase Partido con los datos recibidos
        y las añade a la lista de partidos de la aplicación.
        """
        # Realiza una solicitud GET a la URL de la API que contiene los datos de los partidos
        api = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json")
        
        # Convierte la respuesta de la API a formato JSON
        datos = api.json()

        # Itera sobre la lista de datos obtenidos de la API
        for info in datos:
            # Extrae la información de cada partido
            id = info["id"]
            numero = info["number"]
            fecha = info["date"]
            grupo = info["group"]
            
            # Busca los equipos local y visitante por su ID
            equipo_local = self.buscar_equipo_id(info["home"]["id"])
            equipo_visitante = self.buscar_equipo_id(info["away"]["id"])
            
            # Busca el estadio por su ID
            estadio = self.buscar_estadio_id(info["stadium_id"])

            # Crea una instancia de la clase Partido con la información extraída
            partido = Partido(id, numero, equipo_local, equipo_visitante, fecha, grupo, estadio)
            
            # Añade el partido a la lista de partidos de la aplicación
            self.partidos.append(partido)

    def ver_equipos(self):
        """
        Muestra la lista de equipos disponibles en la aplicación.
        
        Imprime los detalles de cada equipo en la lista de equipos.
        """
        print("\n")
        # Itera sobre la lista de equipos y muestra los detalles de cada uno
        for equipo in self.equipos:
            print(equipo.mostrar())

    def ver_estadios(self):
        """
        Muestra la lista de estadios disponibles en la aplicación.
        
        Imprime los detalles de cada estadio en la lista de estadios.
        """
        print("\n")
        # Itera sobre la lista de estadios y muestra los detalles de cada uno
        for estadio in self.estadios:
            print(estadio.mostrar())

    def ver_partidos(self):
        """
        Muestra la lista de partidos disponibles en la aplicación.
        
        Imprime los detalles de cada partido en la lista de partidos.
        """
        print("\n")
        # Itera sobre la lista de partidos y muestra los detalles de cada uno
        for partido in self.partidos:
            print(partido.mostrar())


    def bascar_partido_pais(self):
        """
        Busca partidos en la aplicación basados en el nombre de un país ingresado por el usuario.
        
        Solicita al usuario el nombre de un país y muestra los partidos en los que participa dicho país, ya sea
        como equipo local o visitante.
        """
        # Solicita al usuario que ingrese el nombre del país
        nombre = input("\nIngrese el nombre del pais del cual quiere ver los partidos: ").lower()
        
        # Valida que el nombre ingresado sea una cadena alfabética y tenga al menos un carácter
        while (not nombre.isalpha()) and (not len(nombre) >= 1):
            print("\nIngrese un nombre valido")
            nombre = input("Ingrese el nombre del pais del cual quiere ver los partidos: ")

        resultado_busqueda = []

        # Busca partidos en los que el nombre del país coincida con el equipo local o visitante
        for partido in self.partidos:
            if nombre in partido.equipoLocal.nombre.lower() or nombre in partido.equipoVisitante.nombre.lower():
                resultado_busqueda.append(partido)
        
        # Muestra el resultado de la búsqueda
        if len(resultado_busqueda) == 0:
            print("\nNo se encontraron partidos para el pais ingresado.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for partido in resultado_busqueda:
                print(f"{count}.\n{partido.mostrar()}")
                count += 1

    def buscar_partido_estadio(self):
        """
        Busca partidos en la aplicación basados en el nombre de un estadio ingresado por el usuario.
        
        Solicita al usuario el nombre de un estadio y muestra los partidos que se juegan en dicho estadio.
        """
        # Solicita al usuario que ingrese el nombre del estadio
        nombre_estadio = input("Ingresa el nombre del estadio para mostrar los partidos asociados: ")
        
        # Valida que el nombre ingresado sea una cadena alfabética y tenga al menos un carácter
        while (not nombre_estadio.isalpha()) and (not len(nombre_estadio) >= 1):
            print("\nIngrese un nombre valido")
            nombre_estadio = input("Ingresa el nombre del estadio para mostrar los partidos asociados: ")
        
        resultado_busqueda = []

        # Busca partidos en los que el nombre del estadio coincida
        for partido in self.partidos:
            if nombre_estadio.lower() in partido.estadio.nombre.lower():
                resultado_busqueda.append(partido)
        
        # Muestra el resultado de la búsqueda
        if len(resultado_busqueda) == 0:
            print("\nNo se encontraron partidos para el estadio ingresado.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for partido in resultado_busqueda:
                print(f"{count}.\n{partido.mostrar()}")
                count += 1

    def buscar_partido_fecha(self):
        """
        Busca partidos en la aplicación basados en la fecha ingresada por el usuario.
        
        Solicita al usuario el día de un partido y muestra los partidos que se juegan en dicha fecha.
        """
        # Solicita al usuario que ingrese el día del partido
        fecha = input("\nIngrese la fecha del partido (solo el dia): ")
        
        # Valida que la fecha ingresada sea un número y esté dentro del rango permitido
        while (not fecha.isnumeric()) or (not int(fecha) in range(14, 27)):
            print("Ingrese una fecha valida (solo el dia)")
            fecha = input("Ingrese la fecha del partido (solo el dia): ")
        
        resultado_busqueda = []

        # Busca partidos que coincidan con el día ingresado
        for partido in self.partidos:
            fecha_separada = partido.fecha.split("-")
            if fecha_separada[2] == fecha:
                resultado_busqueda.append(partido)
        
        # Muestra el resultado de la búsqueda
        if len(resultado_busqueda) == 0:
            print("\nNo se encontraron partidos para la fecha ingresada.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for partido in resultado_busqueda:
                print(f"{count}.\n{partido.mostrar()}")
                count += 1


    def buscador_partidos(self):
        """
        Muestra un menú para buscar partidos por país, estadio o fecha.
        
        Permite al usuario elegir una opción para buscar partidos en la aplicación según el país, estadio o fecha.
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n====================")
            print("BUSQUEDA DE PARTIDOS")
            print("====================")

            # Muestra las opciones del menú de búsqueda
            print("1. Buscar Partidos por País\n2. Buscar Partidos según el Estadio\n3. Buscar Partidos según la Fecha\n4. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 5)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")
            
            # Ejecuta la búsqueda correspondiente según la opción seleccionada
            if int(opcion) == 1:
                self.bascar_partido_pais()
            elif int(opcion) == 2:
                self.buscar_partido_estadio()
            elif int(opcion) == 3:
                self.buscar_partido_fecha()
            else:
                # Sale del bucle y termina el menú de búsqueda
                break


    def gestion_partidos(self):
        """
        Muestra un menú para gestionar partidos y estadios.
        
        Permite al usuario elegir una opción para ver equipos, ver estadios, ver partidos o buscar partidos.
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n========================================")
            print("MODULO DE GESTION DE PARTIDOS Y ESTADIOS")
            print("========================================")

            # Muestra las opciones del menú de gestión
            print("1. Ver Equipos\n2. Ver Estadios\n3. Ver Partidos\n4. Buscador de Partidos\n5. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 6)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")
            
            # Ejecuta la acción correspondiente según la opción seleccionada
            if int(opcion) == 1:
                self.ver_equipos()
            elif int(opcion) == 2:
                self.ver_estadios()
            elif int(opcion) == 3:
                self.ver_partidos()
            elif int(opcion) == 4:
                self.buscador_partidos()
            else:
                # Sale del bucle y termina el menú de gestión
                break


    def seleccionar_asiento(self, tipo_entrada, estadio):
        """
        Permite al usuario seleccionar un asiento en el estadio para un tipo de entrada específico.
        
        Args:
            tipo_entrada (str): El tipo de entrada, puede ser "General" o "VIP".
            estadio (Estadio): El estadio en el que se desea seleccionar el asiento.

        Returns:
            list: Una lista con el número de fila y el número de asiento seleccionados.
        """
        if tipo_entrada == "General":
            # Muestra el mapa de asientos de la zona general
            print(estadio.mostrar_mapa_gnral())

            # Solicita al usuario que ingrese la fila deseada
            opcion_fila = input("Ingrese la fila en la que desea sentarse: ")
            
            # Valida que la fila ingresada sea un número y esté dentro del rango permitido, y que la fila no esté llena
            while (not opcion_fila.isnumeric()) or (not int(opcion_fila) in range(1, len(estadio.mapaGnral)+1)) or(estadio.verificar_fila_llena(int(opcion_fila)-1, tipo_entrada)):
                print("\nDato invalida")
                opcion_fila = input("Ingrese la fila en la que desea sentarse: ")

            index_fila = int(opcion_fila) - 1

            # Solicita al usuario que ingrese el número del asiento deseado
            opcion_asiento = input("Ingrese el numero del asiento donde desea sentarse: ")
            
            # Valida que el número del asiento ingresado sea un número y esté dentro del rango permitido, y que el asiento no esté ocupado
            while (not opcion_asiento.isnumeric()) or (not int(opcion_asiento) in range(1, len(estadio.mapaGnral[index_fila])+1)) or (estadio.asiento_ocupado(index_fila, int(opcion_asiento)-1, tipo_entrada)):
                print("\nDato invalida")
                opcion_asiento = input("Ingrese el numero del asiento donde desea sentarse: ")

            index_asiento = int(opcion_asiento) -  1

            # Marca el asiento como ocupado
            estadio.ocupar_asiento(index_fila, index_asiento, tipo_entrada)

            # Devuelve la fila y el asiento seleccionados
            asiento_elegido = [int(opcion_fila), int(opcion_asiento)]

            return asiento_elegido

        else:
            # Muestra el mapa de asientos de la zona VIP
            print(estadio.mostrar_mapa_vip())
            
            # Solicita al usuario que ingrese la fila deseada
            opcion_fila = input("Ingrese la fila en la que desea sentarse: ")
            
            # Valida que la fila ingresada sea un número y esté dentro del rango permitido, y que la fila no esté llena
            while (not opcion_fila.isnumeric()) or (not int(opcion_fila) in range(1, len(estadio.mapaVip)+1)) or(estadio.verificar_fila_llena(int(opcion_fila)-1, tipo_entrada)):
                print("\nDato invalida")
                opcion_fila = input("Ingrese la fila en la que desea sentarse: ")

            index_fila = int(opcion_fila) - 1

            # Solicita al usuario que ingrese el número del asiento deseado
            opcion_asiento = input("Ingrese el numero del asiento donde desea sentarse: ")
            
            # Valida que el número del asiento ingresado sea un número y esté dentro del rango permitido, y que el asiento no esté ocupado
            while (not opcion_asiento.isnumeric()) or (not int(opcion_asiento) in range(1, len(estadio.mapaVip[index_fila])+1)) or (estadio.asiento_ocupado(index_fila, int(opcion_asiento)-1, tipo_entrada)):
                print("\nDato invalida")
                opcion_asiento = input("Ingrese el numero del asiento donde desea sentarse: ")

            index_asiento = int(opcion_asiento) -  1

            # Marca el asiento como ocupado
            estadio.ocupar_asiento(index_fila, index_asiento, tipo_entrada)

            # Devuelve la fila y el asiento seleccionados
            asiento_elegido = [int(opcion_fila), int(opcion_asiento)]

            return asiento_elegido

        
    def es_vampiro(self, numero_str):
        """
        Verifica si un número dado en formato de cadena es un número vampiro.

        Un número vampiro es un número compuesto cuyos factores (colmillos) contienen
        los mismos dígitos que el número original y, al multiplicarse, producen el número original.
        Los colmillos no deben tener ceros finales a menos que el número original también los tenga.

        Args:
        numero_str (str): El número en formato de cadena.

        Returns:
        bool: True si el número es vampiro, False en caso contrario.
        """
        # Verifica que el número tenga una longitud par
        if len(numero_str) % 2 != 0:
            return False

        # Convierte el número de cadena a entero
        numero = int(numero_str)
        
        # Calcula la longitud de los colmillos
        len_colmillos = len(numero_str) // 2

        # Genera los límites para los colmillos
        min_colmillo = 10**(len_colmillos - 1)
        max_colmillo = 10**len_colmillos

        # Itera sobre los posibles colmillos
        for colmillo1 in range(min_colmillo, max_colmillo):
            for colmillo2 in range(colmillo1, max_colmillo):
                # Evita colmillos con ceros finales
                if (colmillo1 % 10 == 0 and colmillo2 % 10 == 0):
                    continue

                # Verifica si el producto de los colmillos es igual al número original
                if colmillo1 * colmillo2 == numero:
                    # Verifica que los dígitos de los colmillos coincidan con los del número original
                    if sorted(str(colmillo1) + str(colmillo2)) == sorted(numero_str):
                        return True

        return False
    

    def descuento_entrada(self, cliente, subtotal):
        """
        Calcula el descuento en el precio de la entrada para un cliente específico.

        Args:
            cliente (Cliente): El cliente que está comprando la entrada.
            subtotal (float): El precio subtotal de la entrada.

        Returns:
            float: El monto del descuento aplicado. Si el cliente es un vampiro, el descuento es del 50% del subtotal.
        """
        # Verifica si el cliente es un vampiro basado en su cédula
        if self.es_vampiro(cliente.cedula):
            # Calcula el 50% de descuento si el cliente es un vampiro
            descuento = 0.50 * subtotal
            return descuento
        else:
            # No se aplica descuento si el cliente no es un vampiro
            return 0

    def buscar_ci(self, cedula):
        """
        Busca un cliente por su cédula en la lista de clientes.

        Args:
            cedula (str): La cédula del cliente a buscar.

        Returns:
            Cliente: El cliente con la cédula especificada, o None si no se encuentra.
        """
        # Itera sobre la lista de clientes para encontrar el cliente con la cédula dada
        for cliente in self.clientes:
            if cliente.cedula == cedula:
                return cliente
        return None

    

    def registrar_cliente(self):
        """
        Registra un nuevo cliente en la lista de clientes de la aplicación.

        Solicita al usuario que ingrese el nombre, la cédula y la edad del cliente, valida los datos ingresados y crea una instancia de Cliente.
        Añade el nuevo cliente a la lista de clientes.

        Returns:
            Cliente: La instancia del cliente registrado.
        """
        # Solicita al usuario que ingrese el nombre del cliente
        nombre = input("\nIngrese el nombre del cliente: ")
        
        # Valida que el nombre ingresado sea alfabético y tenga al menos 2 caracteres
        while (not nombre.isalpha()) or (not len(nombre) >= 2):
            print("Ingrese un nombre valido")
            nombre = input("Ingrese el nombre del cliente: ")
            
        # Solicita al usuario que ingrese la cédula del cliente
        cedula = input("Ingrese la cedula del cliente: ")
        
        # Valida que la cédula ingresada sea numérica, tenga al menos 6 caracteres y que no esté ya registrada
        while (not cedula.isnumeric()) or (not len(cedula) >= 6) or (self.buscar_ci(cedula) != None):
            print("Ingrese una cedula invalida")
            cedula = input("Ingrese la cedula del cliente: ")

        # Solicita al usuario que ingrese la edad del cliente
        edad = input("Ingrese la edad del cliente: ")
        
        # Valida que la edad ingresada sea numérica y esté en el rango permitido (1 a 119 años)
        while (not edad.isnumeric()) or (not int(edad) in range(1, 120)):
            print("Ingrese una edad valida (entre 1 y 119)")
            edad = input("Ingrese la edad del cliente: ")
        
        # Crea una instancia de la clase Cliente con los datos ingresados
        cliente = Cliente(nombre, cedula, int(edad))
        
        # Añade el nuevo cliente a la lista de clientes de la aplicación
        self.clientes.append(cliente)
        
        # Devuelve la instancia del cliente registrado
        return cliente

    def gestion_entradas(self):
        """
        Módulo de gestión de entradas que permite registrar clientes, verificar clientes registrados y comprar entradas para partidos.
        """
        while True:
            print("\n==============================")
            print("MODULO DE GESTION DE ENTRADAS")
            print("==============================")

            # Muestra las opciones del menú de gestión de entradas
            print("1. Registrar Cliente\n2. Cliente ya Registrado\n3. Salir")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion_cliente = input("Ingrese la opcion que desea: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion_cliente.isnumeric()) or (not int(opcion_cliente) in range(1, 4)):
                print("\nError. Opcion Invalida.")
                opcion_cliente = input("Ingrese la opcion que desea: ")

            if opcion_cliente == "1":
                # Registra un nuevo cliente
                cliente = self.registrar_cliente()
                print("\nCliente Registrado con Exito\n")
            elif opcion_cliente == "2":
                # Verifica si el cliente ya está registrado
                cedula = input("\nIngrese la cedula del cliente: ")
                
                # Valida que la cédula ingresada sea numérica y tenga al menos 6 caracteres
                while (not cedula.isnumeric()) or (not len(cedula) >= 6):
                    print("Ingrese una cedula valida")
                    cedula = input("Ingrese la cedula del cliente: ")
                
                # Si el cliente no está registrado, ofrece la opción de registrarlo
                if self.buscar_ci(cedula) == None:
                    print("\nCliente no registrado.")
                    print("\n1. Deseas registrar al cliente.\n2. Salir")

                    opcion_registro = input("Ingrese la opcion deseada: ")
                    
                    # Valida que la opción de registro ingresada sea un número y esté dentro del rango permitido
                    while (not opcion_registro.isnumeric()) or (not int(opcion_registro) in range(1, 3)):
                        print("\nError. Opcion Invalida.")
                        opcion_registro = input("Ingrese la opcion deseada: ")
                    
                    if opcion_registro == "1":
                        self.registrar_cliente()
                        print("\nCliente Registrado con Exito\n")
                        break
                    else:
                        print("\nHaz Salido del Modulo Gestion de Entradas")
                        break
                else:
                    cliente = self.buscar_ci(cedula)
            else:
                print("\nHaz Salido del Modulo Gestion de Entradas")
                break

            print(f"\nDatos del Cliente:\n{cliente.mostrar_atributos()}")

            print("\n==========================================\n")
            # Muestra la lista de partidos disponibles
            for i in range(len(self.partidos)):
                print(f"{i+1}.\n{self.partidos[i].mostrar()}")
            
            # Solicita al usuario que seleccione un partido
            opcion_partido = input("Ingresa el numero de partido al que quieres asistir: ")
            
            # Valida que la opción de partido ingresada sea un número y esté dentro del rango permitido
            while (not opcion_partido.isnumeric()) or (not int(opcion_partido) in range(1, len(self.partidos)+1)):
                print("\nError. Opcion Invalida.")
                opcion_partido = input("Ingresa el numero de partido al que quieres asistir: ")

            index_partido = int(opcion_partido) - 1
            partido_elegido = self.partidos[index_partido]

            print("1. General\n2. Vip\n")

            # Solicita al usuario que seleccione el tipo de entrada
            opcion_tipo_entrada = input("Ingrese el tipo de entrada que desea comprar: ")
            
            # Valida que la opción de tipo de entrada ingresada sea un número y esté dentro del rango permitido
            while (not opcion_tipo_entrada.isnumeric()) or (not int(opcion_tipo_entrada) in range(1, 3)):
                print("\nError. Opcion Invalida.")
                opcion_tipo_entrada = input("Ingrese el tipo de entrada que desea comprar: ")
            
            if opcion_tipo_entrada == "1":
                tipo_entrada = "General"
                subtotal = 35
                
                # Selecciona un asiento en la zona general
                asiento_elegido = self.seleccionar_asiento(tipo_entrada, partido_elegido.estadio)
                
                # Calcula el descuento para la entrada
                descuento = self.descuento_entrada(cliente, subtotal)
                
                if descuento == 0:
                    print("\nSu cedula no es un numero vampiro por ende, no se aplica descuento.")
                else:
                    print("\nComo su cedula es un numero vampiro se ha aplicado un descuento del 50%.\n")
                
                total_descuento = subtotal - descuento
                iva = total_descuento * 0.16
                total_pagar = total_descuento + iva
                
                # Muestra el resumen de pago
                print("\n=============================================")
                print("              RESUMEN DE PAGO")
                print("=============================================")
                print(f"Nombre: {cliente.nombre}")
                print(f"Cedula: {cliente.cedula}")
                print(f"Fila: {asiento_elegido[0]}, Asiento: {asiento_elegido[1]}")
                print(f"Subtotal: ${subtotal}")
                print(f"Descuento: -${descuento}")
                print(f"Total con Descuento: +${total_descuento}")
                print(f"Iva: +${iva}")
                print(f"Total a Pagar: ${total_pagar}")
                
                # Solicita al usuario que confirme la compra
                print("\n1. Desea completar la comprar? \n2. Salir")
                opcion_pago = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                
                # Valida que la opción de pago ingresada sea un número y esté dentro del rango permitido
                while (not opcion_pago.isnumeric()) or (not int(opcion_pago) in range(1, 3)):
                    print("\nError. Opcion Invalida.")
                    opcion_pago = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                
                if opcion_pago == "1":
                    asistencia = False
                    id = len(self.entradas) + 1
                    entrada = Entrada(id, cliente, partido_elegido, tipo_entrada, asiento_elegido, subtotal,descuento, total_descuento, iva, total_pagar, asistencia)
                    self.entradas.append(entrada)
                    print("\nEntrada Comprada con Exito.\n")
                    break
                else:
                    fila = asiento_elegido[0] - 1
                    asiento = asiento_elegido[1] - 1
                    partido_elegido.estadio.mapaGnral[fila][asiento] = str(asiento + 1)
                    print("\nUsted ha abandonado la compra de la entrada.")
            else:
                tipo_entrada = "VIP"
                subtotal = 75  
                
                # Selecciona un asiento en la zona VIP
                asiento_elegido = self.seleccionar_asiento(tipo_entrada, partido_elegido.estadio)
                descuento = self.descuento_entrada(cliente, subtotal)
                
                if descuento == 0:
                    print("\nSu cedula no es un numero vampiro por ende, no se aplica descuento.")
                else:
                    print("\nComo su cedula es un numero vampiro se ha aplicado un descuento del 50%.\n")
                
                total_descuento = subtotal - descuento
                iva = total_descuento * 0.16
                total_pagar = total_descuento + iva
                
                # Muestra el resumen de pago
                print("\n=============================================")
                print("              RESUMEN DE PAGO")
                print("=============================================")
                print(f"Nombre: {cliente.nombre}")
                print(f"Cedula: {cliente.cedula}")
                print(f"Fila: {asiento_elegido[0]}, Asiento: {asiento_elegido[1]}")
                print(f"Subtotal: ${subtotal}")
                print(f"Descuento: -${descuento}")
                print(f"Total con Descuento: +${total_descuento}")
                print(f"Iva: +${iva}")
                print(f"Total a Pagar: ${total_pagar}")
                
                # Solicita al usuario que confirme la compra
                print("\n1. Desea completar la comprar? \n2. Salir")
                opcion_pago = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                
                # Valida que la opción de pago ingresada sea un número y esté dentro del rango permitido
                while (not opcion_pago.isnumeric()) or (not int(opcion_pago) in range(1, 3)):
                    print("\nError. Opcion Invalida.")
                    opcion_pago = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                
                if opcion_pago == "1":
                    asistencia = False
                    id = len(self.entradas) + 1
                    entrada = Entrada(id, cliente, partido_elegido, tipo_entrada, asiento_elegido, subtotal, descuento, total_descuento, iva, total_pagar, asistencia)
                    self.entradas.append(entrada)
                    print("\nEntrada Comprada con Exito.\n")
                    break
                else:
                    fila = asiento_elegido[0] - 1
                    asiento = asiento_elegido[1] - 1
                    partido_elegido.estadio.mapaVip[fila][asiento] = str(asiento + 1)
                    print("\nUsted ha abandonado la compra de la entrada.") 


    def buscar_entradas_cliente(self, cliente):
        """
        Busca todas las entradas no usadas (sin asistencia) de un cliente específico.

        Args:
            cliente (Cliente): El cliente para el cual se buscan las entradas.

        Returns:
            list: Una lista de entradas no usadas del cliente.
        """
        entradas_cliente = []
        
        # Itera sobre la lista de entradas para encontrar las entradas del cliente que no han sido usadas
        for entrada in self.entradas:
            if entrada.cliente.cedula == cliente.cedula and not entrada.asistencia:
                entradas_cliente.append(entrada)
        
        return entradas_cliente

    def existe_entrada(self, id):
        """
        Verifica si existe una entrada con un ID específico en la lista de entradas.

        Args:
            id (int): El identificador de la entrada a buscar.

        Returns:
            bool: True si la entrada existe, False de lo contrario.
        """
        # Itera sobre la lista de entradas para encontrar la entrada con el ID dado
        for entrada in self.entradas:
            if entrada.id == id:
                return True
        
        return False

    def asistir_partido(self, id):
        """
        Marca una entrada como usada (asistencia confirmada) para un partido específico.

        Args:
            id (int): El identificador de la entrada a marcar como usada.
        """
        # Itera sobre la lista de entradas para encontrar la entrada con el ID dado
        for entrada in self.entradas:
            if entrada.id == id:
                entrada.asistencia = True
                print("\nLa entrada ha sido confirmada.\n")

    def confirmar_asistencia(self):
        """
        Permite confirmar la asistencia de un cliente a un partido usando la entrada comprada.

        Solicita la cédula del cliente, verifica si el cliente tiene entradas no usadas, muestra las entradas disponibles y permite confirmar una de ellas.
        """
        # Solicita al usuario que ingrese la cédula del cliente
        cedula = input("Ingrese la cedula del cliente: ")
        
        # Valida que la cédula ingresada sea numérica y tenga al menos 6 caracteres
        while (not cedula.isnumeric()) or (not len(cedula) >= 6):
            print("Ingrese una cedula valida")
            cedula = input("Ingrese la cedula del cliente: ")

        # Verifica si el cliente está registrado en el sistema
        if self.buscar_ci(cedula) != None:
            cliente = self.buscar_ci(cedula)

            # Verifica si el cliente tiene entradas no usadas
            if len(self.buscar_entradas_cliente(cliente)) != 0:
                entradas = self.buscar_entradas_cliente(cliente)
                
                # Muestra las entradas no usadas del cliente
                for entrada in entradas:
                    print(entrada.mostrar())

                # Solicita al usuario que ingrese el ID de la entrada a confirmar
                opcion_id = input("Ingresa el id de la entrada que quiere confirmar: ")
                
                # Valida que el ID ingresado sea numérico, esté dentro del rango permitido y exista en el sistema
                while (not opcion_id.isnumeric()) or (not int(opcion_id) in range(1, len(self.entradas)+1)) or (not self.existe_entrada(int(opcion_id))):
                    print("\nError. Opcion Invalida.")
                    opcion_id = input("Ingresa el id de la entrada que quiere confirmar: ")
                
                # Marca la entrada como usada
                self.asistir_partido(int(opcion_id))

            else:
                print("\nEl cliente no ha comprado ninguna entrada o no tiene entradas por confirmar.\n")
        else:
            print("\nNo se ha encontrado el cliente en la base de datos.\n")
            print("\n1. Desea registrar al cliente.\n2. Salir")
            
            # Solicita al usuario que seleccione una opción para registrar al cliente o salir
            opcion_cliente = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            # Valida que la opción ingresada sea "1" o "2"
            while opcion_cliente not in ["1", "2"]:
                print("\nError. Opcion Invalida.")
                opcion_cliente = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            if opcion_cliente == "1":
                # Registra al cliente en el sistema
                self.registrar_cliente()

                        

    def gestion_asistencia(self):
        """
        Módulo de gestión de asistencias que permite confirmar la asistencia de los clientes a los partidos.
        """
        while True:
            print("\n================================")
            print("MODULO DE GESTION DE ASISTENCIAS")
            print("=================================")
            print("\n1. Confirmar Asistencia\n2. Salir")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion_asistencia = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion_asistencia.isnumeric()) or (not int(opcion_asistencia) in range(1, 3)):
                print("\nError. Opcion Invalida.")
                opcion_asistencia = input("Ingrese el numero correspondiente a la accion que desea realizar: ")

            if int(opcion_asistencia) == 1:
                # Llama a la función para confirmar la asistencia del cliente
                self.confirmar_asistencia()
            else:
                print("\nUsted ha salido del Modulo de Gestion de Asistencias.\n")
                break

    def ver_productos(self):
        """
        Muestra la lista de productos disponibles en la aplicación.

        Itera sobre la lista de productos y muestra los atributos de cada producto.
        """
        # Itera sobre la lista de productos y muestra los atributos de cada uno
        for producto in self.productos:
            print("\n")
            print(producto.mostrar_atributos())

    def bascar_producto_nombre(self):
        """
        Busca productos en la aplicación basados en el nombre ingresado por el usuario.

        Solicita al usuario el nombre de un producto y muestra los productos que coinciden con dicho nombre.
        """
        # Solicita al usuario que ingrese el nombre del producto
        nombre_producto = input("Ingresa el nombre del producto que desea buscar: ")
        
        # Valida que el nombre ingresado sea alfabético y tenga al menos un carácter
        while (not nombre_producto.isalpha()) or (not len(nombre_producto) >= 1):
            print("\nIngrese un nombre valido")
            nombre_producto = input("Ingresa el nombre del producto que desea buscar: ")
        
        resultado_busqueda = []

        # Busca productos que coincidan con el nombre ingresado
        for producto in self.productos:
            if nombre_producto.lower() in producto.nombre.lower():
                resultado_busqueda.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado_busqueda) == 0:
            print("\nNo se encontraron productos para el nombre ingresado.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado_busqueda:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")

    def buscar_alimentos_platos(self):
        """
        Busca alimentos que se sirvan en platos en la lista de productos de la aplicación.

        Itera sobre la lista de productos y añade los alimentos que se sirven en platos a la lista de resultados.
        Muestra los resultados encontrados.
        """
        resultado = []
        
        # Itera sobre la lista de productos para encontrar alimentos que se sirvan en platos
        for producto in self.productos:
            if isinstance(producto, Alimento) and producto.plato:
                resultado.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado) == 0:
            print("\nNo se encontraron alimentos en platos.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")
    
    def buscar_alimentos_paquete(self):
        """
        Busca alimentos que se sirvan en paquetes en la lista de productos de la aplicación.

        Itera sobre la lista de productos y añade los alimentos que se sirven en paquetes a la lista de resultados.
        Muestra los resultados encontrados.
        """
        resultado = []
        
        # Itera sobre la lista de productos para encontrar alimentos que se sirvan en paquetes
        for producto in self.productos:
            if isinstance(producto, Alimento) and not producto.plato:
                resultado.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado) == 0:
            print("\nNo se encontraron alimentos en paquetes.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")

    def buscar_bebida_alcoholica(self):
        """
        Busca bebidas alcohólicas en la lista de productos de la aplicación.

        Itera sobre la lista de productos y añade las bebidas alcohólicas a la lista de resultados.
        Muestra los resultados encontrados.
        """
        resultado = []
        
        # Itera sobre la lista de productos para encontrar bebidas alcohólicas
        for producto in self.productos:
            if isinstance(producto, Bebida) and producto.alcoholica:
                resultado.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado) == 0:
            print("\nNo se encontraron bebidas alcoholicas.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")

    
    def buscar_bebida_no_alcoholica(self):
        """
        Busca bebidas no alcohólicas en la lista de productos de la aplicación.

        Itera sobre la lista de productos y añade las bebidas no alcohólicas a la lista de resultados.
        Muestra los resultados encontrados.
        """
        resultado = []
        
        # Itera sobre la lista de productos para encontrar bebidas no alcohólicas
        for producto in self.productos:
            if isinstance(producto, Bebida) and not producto.alcoholica:
                resultado.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado) == 0:
            print("\nNo se encontraron bebidas no alcoholicas.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")

    def buscar_producto_tipo(self):
        """
        Permite buscar productos en la aplicación por tipo de alimento o bebida.

        Muestra un menú para buscar productos por tipo de alimento (platos o paquetes) o bebida (alcohólicas o no alcohólicas).
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n1. Buscar Tipos de Alimentos\n2. Buscar Tipos de Bebidas\n3. Salir")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion_tipo = input("\nIngrese la opcion que desee: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion_tipo.isnumeric()) or (not int(opcion_tipo) in range(1, 4)):
                print("Ingrese una opcion valida")
                opcion_tipo = input("Ingrese la opcion que desee: ")

            if int(opcion_tipo) == 1:
                # Muestra las opciones de tipos de alimentos
                print("\nTipos de Alimentos:\n1. En platos\n2. En paquete\n3. Salir")
                
                # Solicita al usuario que ingrese el tipo de alimento a buscar
                tipo_alimento = input("\nIngrese el tipo de alimento que desea buscar: ")
                
                # Valida que el tipo de alimento ingresado sea un número y esté dentro del rango permitido
                while (not tipo_alimento.isnumeric()) or (not int(tipo_alimento) in range(1, 4)):
                    print("\nIngrese un nombre valido")
                    tipo_alimento = input("Ingrese el tipo de alimento que desea buscar: ")
                
                if int(tipo_alimento) == 1:
                    # Busca alimentos en platos
                    self.buscar_alimentos_platos()
                elif int(tipo_alimento) == 2:
                    # Busca alimentos en paquetes
                    self.buscar_alimentos_paquete()
                else:
                    break
            elif int(opcion_tipo) == 2:
                # Muestra las opciones de tipos de bebidas
                print("\nTipos de Bebidas:\n1. Alcoholicas\n2. No Alcoholicas\n3. Salir")

                # Solicita al usuario que ingrese el tipo de bebida a buscar
                tipo_bebida = input("\nIngrese el tipo de bebida que desea buscar: ")
                
                # Valida que el tipo de bebida ingresado sea un número y esté dentro del rango permitido
                while (not tipo_bebida.isnumeric()) or (not int(tipo_bebida) in range(1, 4)):
                    print("\nIngrese un nombre valido")
                    tipo_bebida = input("Ingrese el tipo de bebida que desea buscar: ")

                if int(tipo_bebida) == 1:
                    # Busca bebidas alcohólicas
                    self.buscar_bebida_alcoholica()
                elif int(tipo_bebida) == 2:
                    # Busca bebidas no alcohólicas
                    self.buscar_bebida_no_alcoholica()
                else:
                    break     
            else:
                break

    def buscar_rango_precio(self):
        """
        Busca productos en la aplicación dentro de un rango de precios especificado por el usuario.

        Solicita al usuario que ingrese un precio mínimo y un precio máximo, valida los datos ingresados y muestra los productos que se encuentran dentro de ese rango de precios.
        """
        # Solicita al usuario que ingrese el precio mínimo del producto
        precio_minimo = input("Ingrese el precio minimo del producto: ")
        
        # Valida que el precio mínimo ingresado sea un número y mayor que 0
        while (not precio_minimo.isnumeric()) or (not float(precio_minimo) > 0):
            print("\nIngrese un precio invalido")
            precio_minimo = input("Ingrese el precio minimo del producto: ")
        
        # Solicita al usuario que ingrese el precio máximo del producto
        precio_maximo = input("Ingrese el precio maximo del producto: ")
        
        # Valida que el precio máximo ingresado sea un número y mayor o igual al precio mínimo
        while (not precio_maximo.isnumeric()) or (not float(precio_maximo) >= float(precio_minimo)):
            print("\nIngrese un precio invalido")
            precio_maximo = input("Ingrese el precio maximo del producto: ")
        
        resultado = []

        # Busca productos que se encuentren dentro del rango de precios especificado
        for producto in self.productos:
            if float(precio_minimo) <= producto.precio <= float(precio_maximo):
                resultado.append(producto)
        
        # Muestra el resultado de la búsqueda
        if len(resultado) == 0:
            print("\nNo se encontraron productos con precios dentro del rango ingresado.\n")
        else:
            print("\nResultados de la busqueda:\n")
            count = 1
            for producto in resultado:
                print(f"{count}.\n")
                print(producto.mostrar_atributos())
                count += 1
                print("\n")


    def buscador_restaurant(self):
        """
        Muestra un menú para buscar productos en la aplicación por nombre, tipo o rango de precio.
        
        Permite al usuario elegir una opción para buscar productos por nombre, tipo o rango de precio.
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n====================")
            print("BUSQUEDA DE PRODUCTOS")
            print("====================")

            # Muestra las opciones del menú de búsqueda de productos
            print("1. Buscar Productos por Nombre\n2. Buscar Productos por Tipo\n3. Buscar Productos por Rango de Precio\n4. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 5)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")
            
            # Ejecuta la búsqueda correspondiente según la opción seleccionada
            if int(opcion) == 1:
                self.bascar_producto_nombre()
            elif int(opcion) == 2:
                self.buscar_producto_tipo()
            elif int(opcion) == 3:
                self.buscar_rango_precio()
            else:
                break

    def gestion_restaurante(self):
        """
        Módulo de gestión de restaurante que permite ver productos y buscar productos en la aplicación.
        
        Muestra un menú para ver productos, buscar productos o salir del módulo.
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n===============================")
            print("MODULO DE GESTION DE RESTAURANTE")
            print("================================")

            # Muestra las opciones del menú de gestión de restaurante
            print("1. Ver Productos\n2. Busqueda de productos\n3. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 4)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")
            
            # Ejecuta la acción correspondiente según la opción seleccionada
            if int(opcion) == 1:
                self.ver_productos()
            elif int(opcion) == 2:
                self.buscador_restaurant()
            else:
                break

    
    def buscar_entrada_id(self, id):
        """
        Busca una entrada por su ID en la lista de entradas.

        Args:
            id (int): El identificador de la entrada a buscar.

        Returns:
            Entrada: La entrada con el ID especificado, o None si no se encuentra.
        """
        # Itera sobre la lista de entradas para encontrar la entrada con el ID dado
        for entrada in self.entradas:
            if entrada.id == id:
                return entrada
        return None

    def partidos_asistidos(self, cliente):
        """
        Busca todas las entradas asistidas de un cliente específico.

        Args:
            cliente (Cliente): El cliente para el cual se buscan las entradas asistidas.

        Returns:
            list: Una lista de entradas asistidas del cliente.
        """
        entradas_asistidas = []
        
        # Itera sobre la lista de entradas para encontrar las entradas asistidas del cliente
        for entrada in self.entradas:
            if cliente.cedula == entrada.cliente.cedula and entrada.asistencia:
                entradas_asistidas.append(entrada)
        
        return entradas_asistidas

    def numero_perfecto(self, cliente):
        """
        Verifica si la cédula del cliente es un número perfecto.

        Un número perfecto es un número entero positivo que es igual a la suma de sus divisores propios positivos, excluyendo el propio número.

        Args:
            cliente (Cliente): El cliente cuya cédula se va a verificar.

        Returns:
            bool: True si la cédula del cliente es un número perfecto, False de lo contrario.
        """
        divisores = []
        
        # Encuentra todos los divisores de la cédula del cliente
        for i in range(1, int(cliente.cedula)):
            if int(cliente.cedula) % i == 0:
                divisores.append(i)
        
        suma_divisores = sum(divisores)

        # Verifica si la suma de los divisores es igual a la cédula
        if suma_divisores == int(cliente.cedula):
            return True
        else:
            return False

    
    def descuento_compra_restaurant(self, cliente, subtotal):
        """
        Calcula el descuento en el subtotal de una compra en el restaurante para un cliente específico.

        Args:
            cliente (Cliente): El cliente que está realizando la compra.
            subtotal (float): El subtotal de la compra.

        Returns:
            float: El monto del descuento aplicado. Si la cédula del cliente es un número perfecto, el descuento es del 15% del subtotal.
        """
        # Verifica si la cédula del cliente es un número perfecto
        if self.numero_perfecto(cliente):
            # Calcula el 15% de descuento si la cédula es un número perfecto
            descuento = subtotal * 0.15
            return descuento
        else:
            # No se aplica descuento si la cédula no es un número perfecto
            return 0

    def restar_stock(self, factura):
        """
        Resta el stock de los productos comprados según los detalles de la factura.

        Args:
            factura (Factura): La factura que contiene los detalles de los productos comprados.
        """
        # Itera sobre los detalles de productos en la factura
        for detalle in factura.detalles_productos:
            # Busca el producto correspondiente en la lista de productos
            for producto in self.productos:
                if producto.nombre == detalle[0].nombre:
                    # Resta la cantidad comprada del stock del producto
                    producto.stock -= detalle[1]

    def buscar_detalle_producto(self, detalle_productos, producto):
        count = 0
        for detalle in detalle_productos:
            if detalle[0].nombre == producto.nombre:
                return count
            count += 1
        
        return -1


    def comprar_restaurant(self):
        """
        Permite a un cliente realizar una compra en un restaurante dentro de un estadio.

        Solicita la cédula del cliente, verifica si el cliente tiene entradas asistidas, muestra los restaurantes disponibles y permite al cliente comprar productos.
        """
        # Solicita al usuario que ingrese la cédula del cliente
        cedula = input("Ingrese la cedula del cliente: ")
        
        # Valida que la cédula ingresada sea numérica y tenga al menos 6 caracteres
        while (not cedula.isnumeric()) or (not len(cedula) >= 6):
            print("Ingrese una cedula valida")
            cedula = input("Ingrese la cedula del cliente: ")

        # Verifica si el cliente está registrado en el sistema
        if self.buscar_ci(cedula) != None:
            cliente = self.buscar_ci(cedula)

            # Verifica si el cliente tiene entradas asistidas
            if len(self.partidos_asistidos(cliente)) != 0:
                entradas = self.partidos_asistidos(cliente)

                # Muestra las entradas asistidas del cliente
                for entrada in entradas:
                    print(entrada.mostrar())

                # Solicita al usuario que ingrese el ID de una de sus entradas para realizar la compra
                opcion_id = input("Ingresa el id de una de sus entradas para realizar la compra: ")
                
                # Valida que el ID ingresado sea numérico, esté dentro del rango permitido y exista en el sistema
                while (not opcion_id.isnumeric()) or (not int(opcion_id) in range(1, len(self.entradas)+1)) or (not self.existe_entrada(int(opcion_id))):
                    print("\nError. Opcion Invalida.")
                    opcion_id = input("Ingresa el id de una de sus entradas para realizar la compra: ")
                
                entrada_elegida = self.buscar_entrada_id(int(opcion_id))
                partido_elegido = entrada_elegida.partido
                
                # Verifica si hay disponibilidad de stock en los restaurantes del estadio
                if partido_elegido.estadio.disponibilidad_restaurant():
                    count = 1
                    
                    # Muestra los restaurantes con stock disponible
                    for restaurant in partido_elegido.estadio.restaurantes:
                        if restaurant.verificar_stock_productos():
                            print(f"{count}. {restaurant.nombre}")
                            count += 1
                    
                    # Solicita al usuario que seleccione un restaurante para realizar la compra
                    opcion_restaurant = input("\nIngrese el numero del restaurant en el que desea realizar la compra: ")
                    
                    # Valida que la opción ingresada sea numérica y esté dentro del rango permitido
                    while (not opcion_restaurant.isnumeric()) or (not int(opcion_restaurant) in range(1, len(partido_elegido.estadio.restaurantes)+1)):
                        print("\nError. Opcion Invalida.")
                        opcion_restaurant = input("Ingrese el numero del restaurant en el que desea realizar la compra: ")
                    
                    restaurant_elegido = partido_elegido.estadio.restaurantes[int(opcion_restaurant) - 1]

                    print("\n=====================================================")
                    print(f"    PRODUCTOS DE {restaurant_elegido.nombre}")
                    print("=====================================================")

                    count = 1
                    # Muestra los productos con stock disponible en el restaurante seleccionado
                    for producto in restaurant_elegido.productos:
                        if producto.verificar_stock():
                            print(f"{count}.\n{producto.mostrar_atributos()}")
                            count += 1

                    subtotal = 0
                    detalle_productos = []
                    
                    # Permite al cliente seleccionar productos para comprar
                    while True:
                        print("1. Comprar Producto\n2. Salir")
                        opcion_compra = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                        
                        # Valida que la opción ingresada sea numérica y esté dentro del rango permitido
                        while (not opcion_compra.isnumeric()) or (not int(opcion_compra) in range(1, 3)):
                            print("\nError. Opcion Invalida.")
                            opcion_compra = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
                        
                        if int(opcion_compra) == 1:
                            # Solicita al usuario que seleccione un producto para comprar
                            opcion_producto = input("\nIngrese el numero correspondiente al producto que desea comprar: ")
                            
                            # Valida que la opción ingresada sea numérica y esté dentro del rango permitido
                            while (not opcion_producto.isnumeric()) or (not int(opcion_producto) in range(1, len(restaurant_elegido.productos)+1)):
                                print("\nError. Opcion Invalida.")
                                opcion_producto = input("Ingrese el numero correspondiente al producto que desea comprar: ")
                            
                            producto_elegido = restaurant_elegido.productos[int(opcion_producto) - 1]
                            
                            # Solicita al usuario que ingrese la cantidad de productos a comprar
                            cantidad = input("Ingrese la cantidad de productos que desea comprar: ")
                            
                            # Valida que la cantidad ingresada sea numérica y mayor que 0
                            while (not cantidad.isnumeric()) or (int(cantidad) <= 0):
                                print("\nError. Ingrese una cantidad valida.")
                                cantidad = input("Ingrese la cantidad de productos que desea comprar: ")
                            
                            # Calcula el subtotal de la compra y añade el producto a los detalles de la compra
                            subtotal += float(producto_elegido.precio) * int(cantidad)

                            if self.buscar_detalle_producto(detalle_productos, producto_elegido) == -1:
                                detalle_productos.append([producto_elegido, int(cantidad)])
                            else:
                                detalle_productos[self.buscar_detalle_producto(detalle_productos, producto_elegido)][1] += int(cantidad)
                            
                            print(f"\nProducto agregado al carrito.\nSubtotal: ${subtotal}\n")
                        else:
                            if subtotal == 0:
                                print("\nNo ha seleccionado ningun producto para realizar la compra.\n")
                            else:
                                break

                    # Calcula el descuento para la compra
                    descuento = self.descuento_compra_restaurant(cliente, subtotal)
                    if descuento == 0:
                        print("\nEl cliente no cumple con las condiciones para aplicar el descuento.\n")
                    else:
                        print(f"\nDescuento aplicado: ${descuento}")
                    
                    total = subtotal - descuento
                    
                    # Muestra el resumen de la factura
                    print("\n==========================================")
                    print("           RESUMEN DE FACTURA")
                    print("==========================================")
                    for detalle in detalle_productos:
                        print(f"{detalle[0].nombre}: {detalle[1]} unidades x ${detalle[0].precio} = ${float(detalle[0].precio) * int(detalle[1])}")
                    
                    print(f"\nSubtotal: ${subtotal}")
                    print(f"Descuento: ${descuento}")
                    print(f"Total: ${total}")

                    print("\n==========================================")
                    print("             Realizar pago")
                    print("==========================================")

                    print("\n1. Pagar.\n2. Salir")

                    # Solicita al usuario que confirme la compra
                    opcion_pago = input("Ingrese la opcion deseada: ")
                    
                    # Valida que la opción ingresada sea numérica y esté dentro del rango permitido
                    while (not opcion_pago.isnumeric()) or (not int(opcion_pago) in range(1, 3)):
                        print("\nError. Opcion Invalida.")
                        opcion_pago = input("Ingrese la opcion deseada: ")
                    
                    if int(opcion_pago) == 1:
                        # Crea una instancia de Factura con los detalles de la compra
                        factura = Factura(cliente, partido_elegido, restaurant_elegido, detalle_productos, subtotal, descuento, total)
                        
                        # Resta el stock de los productos comprados
                        self.restar_stock(factura)
                        
                        # Añade la factura a la lista de facturas
                        self.facturas.append(factura)
                        print("\nGracias por su compra.\n")
                    else:
                        print("\nLa compra ha sido cancelada.\n")
                        print("\nUsted ha salido del Modulo de Gestion de Ventas.\n")
                else:
                    print("\nNo hay stock disponible en el estadio para realizar la compra.\n")
            else:
                print("\nEl cliente no ha comprado ninguna entrada o no tiene entradas confirmadas.\n")
        else:
            print("\nNo se ha encontrado el cliente en la base de datos.\n")
            print("\n1. Desea registrar al cliente.\n2. Salir")
            
            # Solicita al usuario que seleccione una opción para registrar al cliente o salir
            opcion_cliente = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            # Valida que la opción ingresada sea "1" o "2"
            while opcion_cliente not in ["1", "2"]:
                print("\nError. Opcion Invalida.")
                opcion_cliente = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            if opcion_cliente == "1":
                # Registra al cliente en el sistema
                self.registrar_cliente()     

    def gestion_ventas_restaurante(self):
        """
        Módulo de gestión de ventas de restaurante que permite realizar compras en un restaurante dentro de un estadio.

        Muestra un menú para comprar en un restaurante o salir del módulo.
        El menú se repite hasta que el usuario elige la opción de salir.
        """
        while True:
            print("\n==========================================")
            print("MODULO DE GESTION DE VENTAS DE RESTAURANT")
            print("=========================================")
            print("\n1. Comprar en un Restaurant\n2. Salir")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion_compra = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion_compra.isnumeric()) or (not int(opcion_compra) in range(1, 3)):
                print("\nError. Opcion Invalida.")
                opcion_compra = input("Ingrese el numero correspondiente a la accion que desea realizar: ")

            if int(opcion_compra) == 1:
                # Llama a la función para realizar una compra en el restaurante
                self.comprar_restaurant()
            else:
                print("\nUsted ha salido del Modulo de Gestion de Ventas de Restaurant.\n")
                break

    def gastos_cliente(self, cliente):
        """
        Calcula el total de gastos de un cliente específico en entradas VIP y compras en restaurantes.

        Args:
            cliente (Cliente): El cliente para el cual se calculan los gastos.

        Returns:
            float: El total de los gastos del cliente.
        """
        total_gastos = 0

        # Itera sobre la lista de entradas para sumar los gastos en entradas VIP del cliente
        for entrada in self.entradas:
            if entrada.cliente.cedula == cliente.cedula and entrada.tipo_entrada == "VIP":
                total_gastos += entrada.total
        
        # Itera sobre la lista de facturas para sumar los gastos en restaurantes del cliente
        for factura in self.facturas:
            if factura.cliente.cedula == cliente.cedula:
                total_gastos += factura.total
        
        return total_gastos



    def promedio_cliente_vip(self):
        """
        Calcula el promedio de gasto de todos los clientes VIP.

        Itera sobre la lista de clientes y calcula el total de gastos de cada cliente en entradas VIP y compras en restaurantes.
        Calcula el promedio de los gastos y lo imprime.
        """
        gastos_clientes = []

        # Itera sobre la lista de clientes para calcular los gastos de cada cliente
        for cliente in self.clientes:
            gastos_clientes.append(self.gastos_cliente(cliente))

        # Calcula e imprime el promedio de los gastos si hay datos disponibles
        if len(gastos_clientes) != 0:
            promedio = sum(gastos_clientes) / len(gastos_clientes)
            print(f"\nEl promedio de gasto de clientes VIP es: ${promedio:.2f}\n")
        else:
            print("\nNo hay datos de gastos disponibles para los clientes VIP.\n")


    def entradas_partido(self, partido):
        """
        Calcula el número total de entradas vendidas para un partido específico.

        Args:
            partido (Partido): El partido para el cual se cuentan las entradas vendidas.

        Returns:
            int: El número total de entradas vendidas para el partido.
        """
        entradas_partido = 0

        # Itera sobre la lista de entradas para contar las entradas vendidas para el partido especificado
        for entrada in self.entradas:
            if entrada.partido.id == partido.id:
                entradas_partido += 1
        
        return entradas_partido

    def asistencia_partido(self, partido):
        """
        Calcula el número total de asistencias confirmadas para un partido específico.

        Args:
            partido (Partido): El partido para el cual se cuentan las asistencias confirmadas.

        Returns:
            int: El número total de asistencias confirmadas para el partido.
        """
        asistencia_partido = 0

        # Itera sobre la lista de entradas para contar las asistencias confirmadas para el partido especificado
        for entrada in self.entradas:
            if entrada.partido.id == partido.id and entrada.asistencia:
                asistencia_partido += 1
        
        return asistencia_partido


    def tabla_asistencia(self):
        """
        Muestra una tabla con la asistencia a los partidos, incluyendo el número de entradas vendidas y el número de asistencias confirmadas.

        Itera sobre la lista de partidos y calcula el número de entradas vendidas y asistencias confirmadas para cada partido.
        Imprime una tabla con los resultados, incluyendo la relación entre las ventas de entradas y las asistencias.
        """
        resultado = []

        # Itera sobre la lista de partidos para calcular las entradas vendidas y asistencias confirmadas
        for partido in self.partidos:
            entradas_partido = self.entradas_partido(partido)
            asistencias_partido = self.asistencia_partido(partido)
            resultado.append([partido, entradas_partido, asistencias_partido])
        
        # Imprime la tabla de asistencia si hay datos disponibles
        if len(resultado) != 0:
            print("\n==========================================")
            print("           TABLA DE ASISTENCIA")
            print("==========================================")
            for detalle in resultado:
                print(f"{detalle[0].mostrar_est()}\nEntradas vendidas: {detalle[1]}\nCantidad de asistencias: {detalle[2]}\n")
                
                if detalle[1] != 0:
                    relacion_venta_asistencia = (detalle[2] * 100) / detalle[1]
                    print(f"Asistio el {relacion_venta_asistencia:.2f}% de las personas que compraron entradas.\n")
                else:
                    print("No asistio ningun cliente.\n")
            print("----------------------------------------")
        else:
            print("\nNo hay datos de asistencia disponibles para los partidos.\n")


    def partido_mayor_asistencia(self):
        """
        Muestra el partido con la mayor asistencia confirmada.

        Itera sobre la lista de partidos y calcula el número de asistencias confirmadas para cada partido.
        Encuentra el partido con la mayor asistencia y lo muestra.
        """
        partidos_asistencias = []

        # Itera sobre la lista de partidos para calcular las asistencias confirmadas
        for partido in self.partidos:
            asistencias_partido = self.asistencia_partido(partido)
            if asistencias_partido > 0:
                partidos_asistencias.append([partido, asistencias_partido])
        
        # Encuentra y muestra el partido con la mayor asistencia si hay datos disponibles
        if len(partidos_asistencias) != 0:
            partido_mayor_asistencia = max(partidos_asistencias, key=lambda x: x[1])
            print(f"\nEl partido con mayor asistencia es:\n{partido_mayor_asistencia[0].mostrar()}\n")
        else:
            print("\nNo hay datos de asistencia disponibles para los partidos.\n")

    def partido_mas_vendido(self):
        """
        Muestra el partido con el mayor número de entradas vendidas.

        Itera sobre la lista de partidos y calcula el número de entradas vendidas para cada partido.
        Encuentra el partido con el mayor número de entradas vendidas y lo muestra.
        """
        partidos_ventas = []

        # Itera sobre la lista de partidos para calcular las entradas vendidas
        for partido in self.partidos:
            entradas_partido = self.entradas_partido(partido)
            if entradas_partido > 0:
                partidos_ventas.append([partido, entradas_partido])
        
        # Encuentra y muestra el partido con el mayor número de entradas vendidas si hay datos disponibles
        if len(partidos_ventas) != 0:
            partido_mas_vendido = max(partidos_ventas, key=lambda x: x[1])
            print(f"\nEl partido con mayor venta de entradas es:\n{partido_mas_vendido[0].mostrar()}\n")
        else:
            print("\nNo hay datos de venta de entradas disponibles para los partidos.\n")


    
    def total_venta_producto(self, producto):
        resultado = 0
        for factura in self.facturas:
            cantidad_producto = factura.producto_en_factura(producto)
            resultado += cantidad_producto
            
        return resultado


    def top_productos_vendidos(self):
        resultado = []
        for producto in self.productos:
            venta_total = self.total_venta_producto(producto)
            if venta_total > 0:
                resultado.append([producto, venta_total])
        
        if len(resultado) != 0:
            print("\n==========================================")
            print("           TOP 3 PRODUCTOS VENDIDOS")
            print("==========================================")
            for detalle in sorted(resultado, key=lambda x: x[1], reverse=True)[:3]:
                print(f"{detalle[0].mostrar_atributos()}\nCantidad vendida: {detalle[1]}\n")

        else:
            print("\nNo hay datos de venta de productos disponibles.\n")


    def cantidad_entradas_cliente(self, cliente):
        """
        Calcula la cantidad total de entradas compradas por un cliente específico.

        Args:
            cliente (Cliente): El cliente para el cual se cuentan las entradas.

        Returns:
            int: La cantidad total de entradas compradas por el cliente.
        """
        count = 0

        # Itera sobre la lista de entradas para contar las entradas compradas por el cliente especificado
        for entrada in self.entradas:
            if entrada.cliente.cedula == cliente.cedula:
                count += 1

        return count

    def top_clientes(self):
        """
        Muestra los clientes con más entradas compradas, ordenados de mayor a menor.

        Itera sobre la lista de clientes y calcula la cantidad de entradas compradas por cada cliente.
        Muestra el top 3 de clientes con más entradas compradas. Si hay menos de 3 clientes con entradas, muestra todos los que hayan comprado entradas.
        """
        clientes_entradas = []

        # Itera sobre la lista de clientes para contar las entradas compradas por cada cliente
        for cliente in self.clientes:
            entradas_cliente = self.cantidad_entradas_cliente(cliente)
            if entradas_cliente > 0:  # Ignora clientes que no compraron entradas
                clientes_entradas.append([cliente, entradas_cliente])

        # Si hay datos de clientes con entradas, muestra el top de clientes
        if len(clientes_entradas) != 0:
            # Si hay 3 o más clientes con entradas, muestra el top 3
            if len(clientes_entradas) >= 3:
                top_clientes = sorted(clientes_entradas, key=lambda x: x[1], reverse=True)[:3]
                print("\nTop 3 Clientes con mas Entradas Compradas:")
                for cliente, entradas in top_clientes:
                    print(f"{cliente.nombre}, Cedula: {cliente.cedula}, Entradas Compradas: {entradas}")
            # Si hay 2 clientes con entradas, muestra el top 2
            elif len(clientes_entradas) == 2:
                top_clientes = sorted(clientes_entradas, key=lambda x: x[1], reverse=True)[:2]
                print("\nTop 2 Clientes con mas Entradas Compradas:")
                for cliente, entradas in top_clientes:
                    print(f"{cliente.nombre}, Cedula: {cliente.cedula}, Entradas Compradas: {entradas}")
            # Si hay solo 1 cliente con entradas, muestra ese cliente
            else:
                print("\nSolo hay 1 Cliente con mas Entradas Compradas:")
                print(f"{clientes_entradas[0][0].nombre}, Cedula: {clientes_entradas[0][0].cedula}, Entradas Compradas: {clientes_entradas[0][1]}")
        else:
            print("\nNo hay datos de clientes con entradas disponibles.\n")


    def graficas(self):
        pass

    def indicadores(self):
        while True:
            print("\n==========================================")
            print("    MODULO DE INDICADORES DE GESTION")
            print("=========================================")
            print("\n1. Promedio de Gasto de Clientes VIP\n2. Tabla de Asistencia\n3. Partido con Mayor Asitencia\n4. Partido con Mayor Venta de Entradas\n5. Top 3 Productos mas Vendidos\n6. Top 3 Clientes con mas Entradas Compradas\n7. Graficas\n8. Salir")

            # Solicita al usuario que ingrese una opción del menú
            opcion_indicador = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion_indicador.isnumeric()) or (not int(opcion_indicador) in range(1, 9)):
                print("\nError. Opcion Invalida.")
                opcion_indicador = input("Ingrese el numero correspondiente a la accion que desea realizar: ")
            
            if int(opcion_indicador) == 1:
                self.promedio_cliente_vip()
            elif int(opcion_indicador) == 2:
                self.tabla_asistencia()
            elif int(opcion_indicador) == 3:
                self.partido_mayor_asistencia()
            elif int(opcion_indicador) == 4:
                self.partido_mas_vendido()
            elif int(opcion_indicador) == 5:
                self.top_productos_vendidos()
            elif int(opcion_indicador) == 6:
                self.top_clientes()
            elif int(opcion_indicador) == 7:
                self.graficas()
            elif int(opcion_indicador) == 8:
                print("\nUsted ha salido del Modulo de Indicadores de Gestion.\n")
                break
            
    def eliminar(self):
        """
        Elimina todos los datos de la aplicación.

        Reinicia las listas de equipos, estadios, restaurantes, productos, partidos, entradas, facturas y clientes, dejándolas vacías.
        """
        self.equipos = []         # Vacía la lista de equipos
        self.estadios = []        # Vacía la lista de estadios
        self.restaurantes = []    # Vacía la lista de restaurantes
        self.productos = []       # Vacía la lista de productos
        self.partidos = []        # Vacía la lista de partidos
        self.entradas = []        # Vacía la lista de entradas
        self.facturas = []        # Vacía la lista de facturas
        self.clientes = []        # Vacía la lista de clientes

    def menu_principal(self):
        """
        Muestra el menú principal de la aplicación y permite navegar a diferentes módulos de gestión.

        Muestra las opciones del menú principal y permite al usuario elegir una opción para gestionar partidos y estadios, venta de entradas,
        asistencia a partidos, restaurantes, ventas de restaurantes, indicadores de gestión o salir de la aplicación.
        Antes de salir, guarda los datos en un archivo de texto y elimina todos los datos de la aplicación.
        """
        while True:
            print("\n================================")
            print("BIENVENIDOS AL PROYECTO EURO 2024")
            print("=================================")

            # Muestra las opciones del menú principal
            print("1. Gestion de Partidos y Estadios\n2. Gestion de Venta de Entradas\n3. Gestion de Asistencia de Partidos\n4. Gestion de Restaurantes\n5. Gestion de Ventas de Restaurantes\n6. Indicadores de Gestion\n7. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 8)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")
            
            # Ejecuta la acción correspondiente según la opción seleccionada
            if int(opcion) == 1:
                self.gestion_partidos()
            elif int(opcion) == 2:
                self.gestion_entradas()
            elif int(opcion) == 3:
                self.gestion_asistencia()
            elif int(opcion) == 4:
                self.gestion_restaurante()
            elif int(opcion) == 5:
                self.gestion_ventas_restaurante()
            elif int(opcion) == 6:
                self.indicadores()
            else:
                self.guardar_json()  # Guarda los datos en un archivo de texto antes de salir
                self.eliminar()  # Elimina todos los datos antes de salir
                break

    def guardar_equipos(self):
        """
        Guarda la lista de equipos en un archivo JSON.

        Convierte cada equipo en un diccionario y guarda la lista resultante en 'equipos.json'.
        """
        equipos = []
        for equipo in self.equipos:
            equipos.append(equipo.diccionario())

        with open('equipos.json', 'w', encoding="utf-8") as archivo:
            json.dump(equipos, archivo, indent=4, ensure_ascii= False)

    def guardar_estadios(self):
        """
        Guarda la lista de estadios en un archivo JSON.

        Convierte cada estadio en un diccionario y guarda la lista resultante en 'estadios.json'.
        """
        estadios = []
        for estadio in self.estadios:
            estadios.append(estadio.diccionario())
        
        with open('estadios.json', 'w', encoding="utf-8") as archivo:
            json.dump(estadios, archivo, indent=4, ensure_ascii= False)

    def guardar_partidos(self):
        """
        Guarda la lista de partidos en un archivo JSON.

        Convierte cada partido en un diccionario y guarda la lista resultante en 'partidos.json'.
        """
        partidos = []
        for partido in self.partidos:
            partidos.append(partido.diccionario())
        
        with open('partidos.json', 'w', encoding="utf-8") as archivo:
            json.dump(partidos, archivo, indent=4, ensure_ascii= False)

    def guardar_clientes(self):
        """
        Guarda la lista de clientes en un archivo JSON.

        Convierte cada cliente en un diccionario y guarda la lista resultante en 'clientes.json'.
        """
        clientes = []
        for cliente in self.clientes:
            clientes.append(cliente.diccionario())
        
        with open('clientes.json', 'w', encoding="utf-8") as archivo:
            json.dump(clientes, archivo, indent=4, ensure_ascii= False)

    def guardar_entradas(self):
        """
        Guarda la lista de entradas en un archivo JSON.

        Convierte cada entrada en un diccionario y guarda la lista resultante en 'entradas.json'.
        """
        entradas = []
        for entrada in self.entradas:
            entradas.append(entrada.diccionario())
        
        with open('entradas.json', 'w', encoding="utf-8") as archivo:
            json.dump(entradas, archivo, indent=4, ensure_ascii= False)

    def guardar_facturas(self):
        """
        Guarda la lista de facturas en un archivo JSON.

        Convierte cada factura en un diccionario y guarda la lista resultante en 'facturas.json'.
        """
        facturas = []
        for factura in self.facturas:
            facturas.append(factura.diccionario())
        
        with open('facturas.json', 'w', encoding="utf-8") as archivo:
            json.dump(facturas, archivo, indent=4, ensure_ascii= False)

    def guardar_json(self):
        """
        Guarda todas las listas de datos en archivos JSON.

        Llama a las funciones para guardar equipos, estadios, partidos, clientes, entradas y facturas.
        """
        self.guardar_equipos()
        self.guardar_estadios()
        self.guardar_partidos()
        self.guardar_clientes()
        self.guardar_entradas()
        self.guardar_facturas()

        print("\nDatos guardados exitosamente\n")



    def cargar_equipos_json(self):
        """
        Carga la lista de equipos desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'equipos.json', convierte cada diccionario en una instancia de Equipo y la añade a la lista de equipos.
        """
        archivo_path = 'equipos.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                equipos = json.load(archivo)
                self.equipos = []
                for equipo_data in equipos:
                    id = equipo_data["id"]
                    codigo = equipo_data["codigo"]
                    nombre = equipo_data["nombre"]
                    grupo = equipo_data["grupo"]
                    equipo = Equipo(id, codigo, nombre, grupo)
                    self.equipos.append(equipo)
            print("\nEquipos cargados exitosamente desde equipos.json\n")
        else:
            print("\nError: El archivo equipos.json no se encontró.\n")

    def cargar_estadios_json(self):
        """
        Carga la lista de estadios desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'estadios.json', convierte cada diccionario en una instancia de Estadio y la añade a la lista de estadios.
        """
        archivo_path = 'estadios.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                estadios = json.load(archivo)
                self.estadios = []
                for estadio_data in estadios:
                    id = estadio_data["id"]
                    nombre = estadio_data["nombre"]
                    ciudad = estadio_data["ciudad"]
                    mapaGnral = self.llenar_mapa(estadio_data["capacidad"][0])
                    mapaVip = self.llenar_mapa(estadio_data["capacidad"][1])

                    # Cargar restaurantes
                    lista_restaurantes = []
                    for rest_data in estadio_data["restaurantes"]:
                        nombreRest = rest_data["nombre"]
                        lista_productos = []

                        for prod_data in rest_data["productos"]:
                            nombreProd = prod_data["nombre"]
                            cantidad = prod_data["cantidad"]
                            precio = prod_data["precio"]
                            stock = prod_data["stock"]

                            if prod_data["adicional"] == "plate" or prod_data["adicional"] == "package":
                                plato = False
                                if prod_data["adicional"] == "plate":
                                     plato = True
                                producto = Alimento(nombreProd, cantidad, precio, stock, plato)
                            else:
                                alcoholica = False
                                if prod_data["adicional"] == "alcoholic":
                                     alcoholica = True
                                producto = Bebida(nombreProd, cantidad, precio, stock, alcoholica)

                            lista_productos.append(producto)

                        restaurante = Restaurante(nombreRest, lista_productos)
                        lista_restaurantes.append(restaurante)

                    estadio = Estadio(id, nombre, ciudad, mapaGnral, mapaVip, lista_restaurantes)
                    self.estadios.append(estadio)
            print("\nEstadios cargados exitosamente desde estadios.json\n")
        else:
            print("\nError: El archivo estadios.json no se encontró.\n")

    def cargar_partidos_json(self):
        """
        Carga la lista de partidos desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'partidos.json', convierte cada diccionario en una instancia de Partido y la añade a la lista de partidos.
        """
        archivo_path = 'partidos.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                partidos = json.load(archivo)
                self.partidos = []
                for partido_data in partidos:
                    id = partido_data["id"]
                    numero = partido_data["numero"]
                    fecha = partido_data["fecha"]
                    grupo = partido_data["grupo"]
                    equipo_local = self.buscar_equipo_id(partido_data["equipo_local"])
                    equipo_visitante = self.buscar_equipo_id(partido_data["equipo_visitante"])
                    estadio = self.buscar_estadio_id(partido_data["estadio"])

                    partido = Partido(id, numero, equipo_local, equipo_visitante, fecha, grupo, estadio)
                    self.partidos.append(partido)
            print("\nPartidos cargados exitosamente desde partidos.json\n")
        else:
            print("\nError: El archivo partidos.json no se encontró.\n")

    def cargar_clientes_json(self):
        """
        Carga la lista de clientes desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'clientes.json', convierte cada diccionario en una instancia de Cliente y la añade a la lista de clientes.
        """
        archivo_path = 'clientes.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                clientes = json.load(archivo)
                self.clientes = []
                for cliente_data in clientes:
                    nombre = cliente_data["nombre"]
                    cedula = cliente_data["cedula"]
                    edad = cliente_data["edad"]
                    cliente = Cliente(nombre, cedula, edad)
                    self.clientes.append(cliente)
            print("\nClientes cargados exitosamente desde clientes.json\n")
        else:
            print("\nError: El archivo clientes.json no se encontró.\n")

    def cargar_entradas_json(self):
        """
        Carga la lista de entradas desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'entradas.json', convierte cada diccionario en una instancia de Entrada y la añade a la lista de entradas.
        """
        archivo_path = 'entradas.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                entradas = json.load(archivo)
                self.entradas = []
                for entrada_data in entradas:
                    id = entrada_data["id"]
                    cliente = self.buscar_ci(entrada_data["cliente"])
                    partido = self.buscar_partido_id(entrada_data["partido"])
                    asiento = [int(x) for x in entrada_data["asiento"].split(', ')]
                    tipo_entrada = entrada_data["tipo_entrada"]
                    subtotal = entrada_data["subtotal"]
                    descuento = entrada_data["descuento"]
                    total_descuento = entrada_data["total_descuento"]
                    iva = entrada_data["iva"]
                    total = entrada_data["total"]
                    asistencia = entrada_data["asistencia"]
                    entrada = Entrada(id, cliente, partido, tipo_entrada, asiento, subtotal, descuento, total_descuento, iva, total, asistencia)
                    self.entradas.append(entrada)
            print("\nEntradas cargadas exitosamente desde entradas.json\n")
        else:
            print("\nError: El archivo entradas.json no se encontró.\n")

    def cargar_facturas_json(self):
        """
        Carga la lista de facturas desde un archivo JSON y la almacena en la aplicación.

        Lee el archivo 'facturas.json', convierte cada diccionario en una instancia de Factura y la añade a la lista de facturas.
        """
        archivo_path = 'facturas.json'
        if os.path.exists(archivo_path):
            with open(archivo_path, 'r') as archivo:
                facturas = json.load(archivo)
                self.facturas = []
                for factura_data in facturas:
                    cliente = self.buscar_ci(factura_data["cliente"])
                    partido = self.buscar_partido_id(factura_data["partido"])
                    restaurant = self.buscar_restaurante_nombre(factura_data["restaurant"])
                    detalles_productos = self.convertir_detalles_producto(factura_data["detalles_productos"])
                    subtotal = factura_data["subtotal"]
                    descuento = factura_data["descuento"]
                    total = factura_data["total"]
                    factura = Factura(cliente, partido, restaurant, detalles_productos, subtotal, descuento, total)
                    self.facturas.append(factura)
            print("\nFacturas cargadas exitosamente desde facturas.json\n")
        else:
            print("\nError: El archivo facturas.json no se encontró.\n")


    def buscar_partido_id(self, id):
        """
        Busca un partido por su ID en la lista de partidos.

        Args:
            id (int): El identificador del partido a buscar.

        Returns:
            Partido: El partido con el ID especificado, o None si no se encuentra.
        """
        for partido in self.partidos:
            if partido.id == id:
                return partido
        return None

    def buscar_restaurante_nombre(self, nombre):
        """
        Busca un restaurante por su nombre en la lista de restaurantes.

        Args:
            nombre (str): El nombre del restaurante a buscar.

        Returns:
            Restaurante: El restaurante con el nombre especificado, o None si no se encuentra.
        """
        for restaurante in self.restaurantes:
            if restaurante.nombre == nombre:
                return restaurante
        return None

    def convertir_detalles_producto(self, detalles_productos):
        """
        Convierte los detalles de productos desde un diccionario a una lista de productos.

        Args:
            detalles_productos (list): Lista de diccionarios con detalles de productos.

        Returns:
            list: Lista de productos convertidos.
        """
        productos = []
        for detalle in detalles_productos:
            nombre_producto = detalle[0]
            cantidad = detalle[1]
            producto = self.buscar_producto_nombre(nombre_producto)
            productos.append([producto, cantidad])
        return productos
    
    def buscar_producto_nombre(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                return producto
        return None


    def cargar_json(self):
        self.cargar_equipos_json()
        self.cargar_estadios_json()
        self.cargar_partidos_json()
        self.cargar_clientes_json()
        self.cargar_entradas_json()
        self.cargar_facturas_json()

        print("\nArchivos cargados exitosamente")
        

    def inicializar(self):
        """
        Muestra el menú de inicialización de la aplicación y permite cargar datos desde una API o un archivo de texto.

        Muestra las opciones del menú de inicialización y permite al usuario elegir una opción para cargar datos desde una API, cargar datos desde un archivo de texto o salir de la aplicación.
        Después de cargar los datos, navega al menú principal de la aplicación.
        """
        while True:
            print("\n===========================")
            print("        BIENVENIDOS")
            print("===========================")

            # Muestra las opciones del menú de inicialización
            print("1. Cargar API\n2. Cargar TXT\n3. Salir\n")
            
            # Solicita al usuario que ingrese una opción del menú
            opcion = input("Ingrese una opcion: ")
            
            # Valida que la opción ingresada sea un número y esté dentro del rango permitido
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 4)):
                print("Ingrese una opcion valida")
                opcion = input("Ingrese una opcion: ")

            if int(opcion) == 1:
                print("Espere...")
                # Carga los datos desde la API
                self.cargar_Equipos()
                self.cargar_Estadios()
                self.cargar_Partidos()
                print("\n...Carga Exitosa!")
                # Navega al menú principal de la aplicación
                self.menu_principal()
            elif int(opcion) == 2:
                # Carga los datos desde un archivo de texto
                self.cargar_json()
                # Navega al menú principal de la aplicación
                self.menu_principal()
            else:
                print("Gracias por usar la aplicacion")
                break