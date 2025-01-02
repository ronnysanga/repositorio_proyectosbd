import mysql.connector

# Configuración de conexión
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        db="negocioimportaciones"
    )


def menu_principal():
    while True:
        print("\n-------------------------- Bienvenido al sistema --------------------------")
        print("1. Iniciar sesión.")
        print("2. Crear una cuenta.")
        print("3. Salir.")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            crear_cuenta()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.")


# Función para crear una cuenta de cliente
def crear_cuenta():
    try:
        db = conectar_bd()
        cursor = db.cursor()

        print("\n------------------- Creación de cuenta -------------------")
        id_cliente = input("Ingrese un ID de cliente (único): ")
        nombre_completo = input("Ingrese su nombre completo: ")
        cedula = input("Ingrese su número de cédula: ")
        direccion = input("Ingrese su dirección: ")

        sql = "INSERT INTO Cliente (idCliente, nombreCompleto, cedula, dirreccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_cliente, nombre_completo, cedula, direccion))
        db.commit()

        print("¡Cuenta registrada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al registrar la cuenta: {e}")
    finally:
        cursor.close()
        db.close()


# Función para iniciar sesión (Cliente o Administrativo)
def iniciar_sesion():
    try:
        db = conectar_bd()
        cursor = db.cursor()

        print("\n------------------- Iniciar sesión -------------------")
        cedula = input("Ingrese su número de cédula: ")
        cursor.execute("SELECT nombreCompleto FROM Cliente WHERE cedula = %s", (cedula,))
        resultado = cursor.fetchone()

        if resultado:
            nombre = resultado[0]
            print(f"\n------------------------------ Bienvenido {nombre} ------------------------------")
            menu_cliente(cedula)  # Pasa cedula como argumento
        else:
            cursor.execute("SELECT nomCompleto FROM GerenteAdm WHERE cedula = %s", (cedula,))
            resultado = cursor.fetchone()
            if resultado:
                nombre = resultado[0]
                print(f"\n------------------------------ Bienvenido Administrador {nombre} ------------------------------")
                menu_administrador()
            else:
                print("Cédula incorrecta o usuario no registrado.")
    except mysql.connector.Error as e:
        print(f"Error al iniciar sesión: {e}")
    finally:
        cursor.close()
        db.close()



# Menú principal para el cliente
def menu_cliente(cedula_cliente):
    while True:
        print("\n1. Ver pedidos")
        print("2. Realizar un pedido")
        print("3. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_pedidos_cliente(cedula_cliente)
        elif opcion == "2":
            realizar_pedido(cedula_cliente)
        elif opcion == "3":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

# Función para realizar un pedido
def realizar_pedido(cedula_cliente):
    db = conectar_bd()
    cursor = db.cursor()

    total_pedido = 0
    continuar = 'si'

    while continuar.lower() == 'si':
        cursor.execute("SELECT idProducto, nombre, precioVenta, cantidad FROM Producto WHERE cantidad > 0")
        productos = cursor.fetchall()

        if productos:
            print("\n--- Productos disponibles ---")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: ${producto[2]:.2f}, Stock: {producto[3]}")

            id_producto = int(input("Ingrese el ID del producto que desea comprar: "))
            cantidad = int(input("Ingrese la cantidad que desea comprar: "))

            cursor.execute("SELECT cantidad, precioVenta FROM Producto WHERE idProducto = %s", (id_producto,))
            producto = cursor.fetchone()

            if producto and producto[0] >= cantidad:
                total_pedido += producto[1] * cantidad
                print(f"Producto añadido al pedido. Total parcial: ${total_pedido:.2f}")

                cursor.execute("UPDATE Producto SET cantidad = cantidad - %s WHERE idProducto = %s", (cantidad, id_producto))
                db.commit()

            else:
                print("No hay suficiente stock para este producto.")

            continuar = input("¿Desea comprar otro producto? (si/no): ")
        else:
            print("No hay productos disponibles actualmente.")
            break

    print(f"\nEl total a pagar es de: ${total_pedido:.2f}")
    cursor.execute("INSERT INTO Pedido (fechaEntrega, valorTotal, clienteID, ced_Venta) VALUES (CURDATE(), %s, (SELECT idCliente FROM Cliente WHERE cedula = %s), 0991426578)", (total_pedido, cedula_cliente))
    db.commit()

    print("¡Muchas gracias por su compra!")

    cursor.close()
    db.close()
# Función para ver pedidos de un cliente
def ver_pedidos_cliente(cedula_cliente):
    try:
        db = conectar_bd()
        cursor = db.cursor()

        cedula = input("Ingrese su número de cédula para consultar pedidos: ")
        sql = """
        SELECT Pedido.idPedido, Pedido.fechaEntrega, Pedido.valorTotal, Producto.nombre
        FROM Pedido
        JOIN Cliente ON Pedido.clienteID = Cliente.idCliente
        JOIN Producto ON Pedido.idPedido = Producto.idPedido
        WHERE Cliente.cedula = %s
        """
        cursor.execute(sql, (cedula_cliente,))
        pedidos = cursor.fetchall()

        if pedidos:
            print("\n--- Sus pedidos ---")
            for pedido in pedidos:
                print(
                    f"ID Pedido: {pedido[0]}, Fecha de entrega: {pedido[1]}, Total: ${pedido[2]:.2f}, Producto: {pedido[3]}")
        else:
            print("No tiene pedidos registrados.")
    except mysql.connector.Error as e:
        print(f"Error al consultar los pedidos: {e}")
    finally:
        cursor.close()
        db.close()


# Menú principal para administrador
def menu_administrador():
    while True:
        print("\n1. Administrar pedidos")
        print("2. Ver recordatorios")
        print("3. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            administrar_pedidos()
        elif opcion == "2":
            ver_recordatorios()
        elif opcion == "3":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")


# Función para ver recordatorios del administrador
def ver_recordatorios():
    try:
        db = conectar_bd()
        cursor = db.cursor()

        cursor.execute("SELECT titulo, descripcion, fechaMax FROM Recordatorio")
        recordatorios = cursor.fetchall()

        if recordatorios:
            print("\n--- Recordatorios ---")
            for rec in recordatorios:
                print(f"Título: {rec[0]}, Descripción: {rec[1]}, Fecha máxima: {rec[2]}")
        else:
            print("No hay recordatorios.")
    except mysql.connector.Error as e:
        print(f"Error al consultar los recordatorios: {e}")
    finally:
        cursor.close()
        db.close()


# Función para administrar pedidos
def administrar_pedidos():
    try:
        db = conectar_bd()
        cursor = db.cursor()

        print("\n--- Lista de pedidos ---")
        cursor.execute("SELECT * FROM Pedido")
        pedidos = cursor.fetchall()

        for pedido in pedidos:
            print(f"ID Pedido: {pedido[0]}, Fecha entrega: {pedido[1]}, Total: ${pedido[2]:.2f}")
    except mysql.connector.Error as e:
        print(f"Error al consultar los pedidos: {e}")
    finally:
        cursor.close()
        db.close()


# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal()