import mysql.connector

# Configuración de conexión
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        db="negocioimportaciones"
    )

# AVANCE 1 ******************************************************************************************************************************************************************************************


'''
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

'''


# AVANCE 2 ******************************************************************************************************************************************************************************************


# REALIZACIÓN DEL CRUD = CREATE (AÑADIR o CREAR) - READ (CONSULTAR) - UPADATE (EDITAR) - DELETE (ELIMINAR REGISTRO)

# ================================ CLIENTE ================================
def menu_clientes():
    while True:
        print("\n--- Menú CRUD Clientes ---")
        print("1. Crear Cliente")
        print("2. Consultar Clientes")
        print("3. Editar Cliente")
        print("4. Eliminar Cliente")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            consultar_clientes()
        elif opcion == "3":
            editar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ---------------- 
def crear_cliente():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Cliente ---")
        id_cliente = input("Ingrese el ID del cliente: ")
        nombre = input("Ingrese el nombre completo del cliente: ")
        cedula = input("Ingrese la cédula del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")

        sql = "INSERT INTO cliente (idCliente, nombreCompleto, cedula, dirreccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_cliente, nombre, cedula, direccion))
        db.commit()
        print("¡Cliente creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear cliente: {e}")
    finally:
        cursor.close()
        db.close()

# ---------------- Consultar ---------------- 
def consultar_clientes():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Clientes ---")
        print("1. Ver todos los clientes")
        print("2. Buscar un cliente específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los clientes
            cursor.execute("SELECT * FROM cliente")
            resultados = cursor.fetchall()
            if resultados:
                for cliente in resultados:
                    print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Cédula: {cliente[2]}, Dirección: {cliente[3]}")
            else:
                print("No se encontraron clientes registrados.")
        
        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Cliente Específico ---")
            print("1. Buscar por ID")
            print("2. Buscar por Cédula")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                id_cliente = input("Ingrese el ID del cliente: ")
                cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (id_cliente,))
            elif sub_opcion == "2":
                cedula = input("Ingrese la cédula del cliente: ")
                cursor.execute("SELECT * FROM cliente WHERE cedula = %s", (cedula,))
            else:
                print("Opción inválida.")
                return

            cliente = cursor.fetchone()
            if cliente:
                print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Cédula: {cliente[2]}, Dirección: {cliente[3]}")
            else:
                print("No se encontró el cliente con los datos proporcionados.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar clientes: {e}")
    finally:
        cursor.close()
        db.close()

# ---------------- Editar ---------------- 
def editar_cliente():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Cliente ---")
        id_cliente = input("Ingrese el ID del cliente que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        nueva_cedula = input("Ingrese la nueva cédula: ")
        nueva_direccion = input("Ingrese la nueva dirección: ")

        sql = "UPDATE cliente SET nombreCompleto = %s, cedula = %s, dirreccion = %s WHERE idCliente = %s"
        cursor.execute(sql, (nuevo_nombre, nueva_cedula, nueva_direccion, id_cliente))
        db.commit()
        print("¡Cliente editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar cliente: {e}")
    finally:
        cursor.close()
        db.close()

# ---------------- Eliminar Registro ---------------- 
def eliminar_cliente():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Cliente ---")
        id_cliente = input("Ingrese el ID del cliente que desea eliminar: ")

        sql = "DELETE FROM cliente WHERE idCliente = %s"
        cursor.execute(sql, (id_cliente,))
        db.commit()
        print("¡Cliente eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar cliente: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ GERENTE ADMINISTRATIVO ================================
def menu_gerentes_adm():
    while True:
        print("\n--- Menú CRUD Gerentes Administrativos ---")
        print("1. Crear Gerente Administrativo")
        print("2. Consultar Gerentes Administrativos")
        print("3. Editar Gerente Administrativo")
        print("4. Eliminar Gerente Administrativo")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_gerente_adm()
        elif opcion == "2":
            consultar_gerentes_adm()
        elif opcion == "3":
            editar_gerente_adm()
        elif opcion == "4":
            eliminar_gerente_adm()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_gerente_adm():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Gerente Administrativo ---")
        cedula = input("Ingrese la cédula del gerente (única): ")
        nombre = input("Ingrese el nombre completo del gerente: ")

        sql = "INSERT INTO gerenteadm (cedula, nomCompleto) VALUES (%s, %s)"
        cursor.execute(sql, (cedula, nombre))
        db.commit()
        print("¡Gerente administrativo creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear gerente administrativo: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ----------------  
def consultar_gerentes_adm():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Gerentes Administrativos ---")
        print("1. Ver todos los gerentes administrativos")
        print("2. Buscar un gerente administrativo específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los gerentes
            cursor.execute("SELECT * FROM gerenteadm")
            resultados = cursor.fetchall()
            if resultados:
                for gerente in resultados:
                    print(f"Cédula: {gerente[0]}, Nombre: {gerente[1]}")
            else:
                print("No se encontraron gerentes administrativos registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Gerente Administrativo Específico ---")
            cedula = input("Ingrese la cédula del gerente: ")
            cursor.execute("SELECT * FROM gerenteadm WHERE cedula = %s", (cedula,))
            gerente = cursor.fetchone()
            if gerente:
                print(f"Cédula: {gerente[0]}, Nombre: {gerente[1]}")
            else:
                print("No se encontró el gerente administrativo con la cédula proporcionada.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar gerentes administrativos: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_gerente_adm():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Gerente Administrativo ---")
        cedula = input("Ingrese la cédula del gerente que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre completo del gerente: ")

        sql = "UPDATE gerenteadm SET nomCompleto = %s WHERE cedula = %s"
        cursor.execute(sql, (nuevo_nombre, cedula))
        db.commit()
        print("¡Gerente administrativo editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar gerente administrativo: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_gerente_adm():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Gerente Administrativo ---")
        cedula = input("Ingrese la cédula del gerente que desea eliminar: ")

        sql = "DELETE FROM gerenteadm WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        db.commit()
        print("¡Gerente administrativo eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar gerente administrativo: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ GERENTE DE VENTA ================================
def menu_gerentes_venta():
    while True:
        print("\n--- Menú CRUD Gerentes de Ventas ---")
        print("1. Crear Gerente de Ventas")
        print("2. Consultar Gerentes de Ventas")
        print("3. Editar Gerente de Ventas")
        print("4. Eliminar Gerente de Ventas")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_gerente_venta()
        elif opcion == "2":
            consultar_gerentes_venta()
        elif opcion == "3":
            editar_gerente_venta()
        elif opcion == "4":
            eliminar_gerente_venta()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_gerente_venta():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Gerente de Ventas ---")
        cedula = input("Ingrese la cédula del gerente de ventas (única): ")
        nombre = input("Ingrese el nombre completo del gerente de ventas: ")

        sql = "INSERT INTO gerenteventa (cedula, nomCompleto) VALUES (%s, %s)"
        cursor.execute(sql, (cedula, nombre))
        db.commit()
        print("¡Gerente de ventas creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear gerente de ventas: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ----------------  
def consultar_gerentes_venta():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Gerentes de Ventas ---")
        print("1. Ver todos los gerentes de ventas")
        print("2. Buscar un gerente de ventas específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los gerentes
            cursor.execute("SELECT * FROM gerenteventa")
            resultados = cursor.fetchall()
            if resultados:
                for gerente in resultados:
                    print(f"Cédula: {gerente[0]}, Nombre: {gerente[1]}")
            else:
                print("No se encontraron gerentes de ventas registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Gerente de Ventas Específico ---")
            cedula = input("Ingrese la cédula del gerente de ventas: ")
            cursor.execute("SELECT * FROM gerenteventa WHERE cedula = %s", (cedula,))
            gerente = cursor.fetchone()
            if gerente:
                print(f"Cédula: {gerente[0]}, Nombre: {gerente[1]}")
            else:
                print("No se encontró el gerente de ventas con la cédula proporcionada.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar gerentes de ventas: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_gerente_venta():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Gerente de Ventas ---")
        cedula = input("Ingrese la cédula del gerente de ventas que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre completo del gerente de ventas: ")

        sql = "UPDATE gerenteventa SET nomCompleto = %s WHERE cedula = %s"
        cursor.execute(sql, (nuevo_nombre, cedula))
        db.commit()
        print("¡Gerente de ventas editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar gerente de ventas: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_gerente_venta():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Gerente de Ventas ---")
        cedula = input("Ingrese la cédula del gerente de ventas que desea eliminar: ")

        sql = "DELETE FROM gerenteventa WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        db.commit()
        print("¡Gerente de ventas eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar gerente de ventas: {e}")
    finally:
        cursor.close()
        db.close()


# ================================ ORDEN DE COMPRA ================================
def menu_ordenes_compra():
    while True:
        print("\n--- Menú CRUD Órdenes de Compra ---")
        print("1. Crear Orden de Compra")
        print("2. Consultar Órdenes de Compra")
        print("3. Editar Orden de Compra")
        print("4. Eliminar Orden de Compra")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_orden_compra()
        elif opcion == "2":
            consultar_ordenes_compra()
        elif opcion == "3":
            editar_orden_compra()
        elif opcion == "4":
            eliminar_orden_compra()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_orden_compra():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Orden de Compra ---")
        id_orden = input("Ingrese el ID de la orden de compra: ")
        fecha_emision = input("Ingrese la fecha de emisión (YYYY-MM-DD): ")
        fecha_llegada = input("Ingrese la fecha de llegada (YYYY-MM-DD): ")
        valor_total = float(input("Ingrese el valor total de la orden: "))
        proveedor_id = input("Ingrese el ID del proveedor: ")
        ced_adm = input("Ingrese la cédula del gerente administrativo asociado: ")

        sql = """
        INSERT INTO ordencompra (idOrden, fechaEmision, fechaLlegada, valorTotal, ProveedorId, ced_adm) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_orden, fecha_emision, fecha_llegada, valor_total, proveedor_id, ced_adm))
        db.commit()
        print("¡Orden de compra creada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear la orden de compra: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ----------------  
def consultar_ordenes_compra():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Órdenes de Compra ---")
        print("1. Ver todas las órdenes de compra")
        print("2. Buscar una orden de compra específica")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todas las órdenes de compra
            cursor.execute("SELECT * FROM ordencompra")
            resultados = cursor.fetchall()
            if resultados:
                for orden in resultados:
                    print(f"ID: {orden[0]}, Fecha Emisión: {orden[1]}, Fecha Llegada: {orden[2]}, Valor Total: ${orden[3]:.2f}, "
                          f"Proveedor ID: {orden[4]}, Gerente Administrativo: {orden[5]}")
            else:
                print("No se encontraron órdenes de compra registradas.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Orden de Compra Específica ---")
            id_orden = input("Ingrese el ID de la orden de compra: ")
            cursor.execute("SELECT * FROM ordencompra WHERE idOrden = %s", (id_orden,))
            orden = cursor.fetchone()
            if orden:
                print(f"ID: {orden[0]}, Fecha Emisión: {orden[1]}, Fecha Llegada: {orden[2]}, Valor Total: ${orden[3]:.2f}, "
                      f"Proveedor ID: {orden[4]}, Gerente Administrativo: {orden[5]}")
            else:
                print("No se encontró la orden de compra con el ID proporcionado.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar órdenes de compra: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_orden_compra():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Orden de Compra ---")
        id_orden = input("Ingrese el ID de la orden de compra que desea editar: ")
        nueva_fecha_emision = input("Ingrese la nueva fecha de emisión (YYYY-MM-DD): ")
        nueva_fecha_llegada = input("Ingrese la nueva fecha de llegada (YYYY-MM-DD): ")
        nuevo_valor_total = float(input("Ingrese el nuevo valor total: "))
        nuevo_proveedor_id = input("Ingrese el nuevo ID del proveedor: ")
        nuevo_ced_adm = input("Ingrese la nueva cédula del gerente administrativo asociado: ")

        sql = """
        UPDATE ordencompra 
        SET fechaEmision = %s, fechaLlegada = %s, valorTotal = %s, ProveedorId = %s, ced_adm = %s 
        WHERE idOrden = %s
        """
        cursor.execute(sql, (nueva_fecha_emision, nueva_fecha_llegada, nuevo_valor_total, nuevo_proveedor_id, nuevo_ced_adm, id_orden))
        db.commit()
        print("¡Orden de compra editada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar la orden de compra: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_orden_compra():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Orden de Compra ---")
        id_orden = input("Ingrese el ID de la orden de compra que desea eliminar: ")

        sql = "DELETE FROM ordencompra WHERE idOrden = %s"
        cursor.execute(sql, (id_orden,))
        db.commit()
        print("¡Orden de compra eliminada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar la orden de compra: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ PEDIDO ================================
def menu_pedidos():
    while True:
        print("\n--- Menú CRUD Pedidos ---")
        print("1. Crear Pedido")
        print("2. Consultar Pedidos")
        print("3. Editar Pedido")
        print("4. Eliminar Pedido")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_pedido()
        elif opcion == "2":
            consultar_pedidos()
        elif opcion == "3":
            editar_pedido()
        elif opcion == "4":
            eliminar_pedido()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_pedido():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Pedido ---")
        id_pedido = input("Ingrese el ID del pedido: ")
        fecha_entrega = input("Ingrese la fecha de entrega (YYYY-MM-DD): ")
        valor_total = float(input("Ingrese el valor total del pedido: "))
        cliente_id = input("Ingrese el ID del cliente asociado: ")
        ced_venta = input("Ingrese la cédula del gerente de ventas asociado: ")

        sql = """
        INSERT INTO pedido (idPedido, fechaEntrega, valorTotal, clienteID, ced_Venta) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_pedido, fecha_entrega, valor_total, cliente_id, ced_venta))
        db.commit()
        print("¡Pedido creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear el pedido: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ---------------- 
def consultar_pedidos():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Pedidos ---")
        print("1. Ver todos los pedidos")
        print("2. Buscar un pedido específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los pedidos
            cursor.execute("SELECT * FROM pedido")
            resultados = cursor.fetchall()
            if resultados:
                for pedido in resultados:
                    print(f"ID: {pedido[0]}, Fecha Entrega: {pedido[1]}, Valor Total: ${pedido[2]:.2f}, "
                          f"Cliente ID: {pedido[3]}, Gerente de Ventas: {pedido[4]}")
            else:
                print("No se encontraron pedidos registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Pedido Específico ---")
            id_pedido = input("Ingrese el ID del pedido: ")
            cursor.execute("SELECT * FROM pedido WHERE idPedido = %s", (id_pedido,))
            pedido = cursor.fetchone()
            if pedido:
                print(f"ID: {pedido[0]}, Fecha Entrega: {pedido[1]}, Valor Total: ${pedido[2]:.2f}, "
                      f"Cliente ID: {pedido[3]}, Gerente de Ventas: {pedido[4]}")
            else:
                print("No se encontró el pedido con el ID proporcionado.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar pedidos: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_pedido():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Pedido ---")
        id_pedido = input("Ingrese el ID del pedido que desea editar: ")
        nueva_fecha_entrega = input("Ingrese la nueva fecha de entrega (YYYY-MM-DD): ")
        nuevo_valor_total = float(input("Ingrese el nuevo valor total: "))
        nuevo_cliente_id = input("Ingrese el nuevo ID del cliente: ")
        nueva_ced_venta = input("Ingrese la nueva cédula del gerente de ventas: ")

        sql = """
        UPDATE pedido 
        SET fechaEntrega = %s, valorTotal = %s, clienteID = %s, ced_Venta = %s 
        WHERE idPedido = %s
        """
        cursor.execute(sql, (nueva_fecha_entrega, nuevo_valor_total, nuevo_cliente_id, nueva_ced_venta, id_pedido))
        db.commit()
        print("¡Pedido editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar el pedido: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_pedido():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Pedido ---")
        id_pedido = input("Ingrese el ID del pedido que desea eliminar: ")

        sql = "DELETE FROM pedido WHERE idPedido = %s"
        cursor.execute(sql, (id_pedido,))
        db.commit()
        print("¡Pedido eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar el pedido: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ PRODUCTO ================================
def menu_productos():
    while True:
        print("\n--- Menú CRUD Productos ---")
        print("1. Crear Producto")
        print("2. Consultar Productos")
        print("3. Editar Producto")
        print("4. Eliminar Producto")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_producto()
        elif opcion == "2":
            consultar_productos()
        elif opcion == "3":
            editar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_producto():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Producto ---")
        id_producto = input("Ingrese el ID del producto: ")
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Ingrese la descripción del producto: ")
        costo = float(input("Ingrese el costo del producto: "))
        precio_venta = float(input("Ingrese el precio de venta del producto: "))
        cantidad = int(input("Ingrese la cantidad en stock: "))
        id_orden_compra = input("Ingrese el ID de la orden de compra asociada: ")
        id_pedido = input("Ingrese el ID del pedido asociado: ")

        sql = """
        INSERT INTO producto (idProducto, nombre, descripcion, costo, precioVenta, cantidad, idOrdenCompra, idPedido) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_producto, nombre, descripcion, costo, precio_venta, cantidad, id_orden_compra, id_pedido))
        db.commit()
        print("¡Producto creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear producto: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ---------------- 
def consultar_productos():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Productos ---")
        print("1. Ver todos los productos")
        print("2. Buscar un producto específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los productos
            cursor.execute("SELECT * FROM producto")
            resultados = cursor.fetchall()
            if resultados:
                for producto in resultados:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Costo: ${producto[3]:.2f}, "
                          f"Precio Venta: ${producto[4]:.2f}, Cantidad: {producto[5]}, ID Orden: {producto[6]}, ID Pedido: {producto[7]}")
            else:
                print("No se encontraron productos registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Producto Específico ---")
            print("1. Buscar por ID")
            print("2. Buscar por Nombre")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                id_producto = input("Ingrese el ID del producto: ")
                cursor.execute("SELECT * FROM producto WHERE idProducto = %s", (id_producto,))
            elif sub_opcion == "2":
                nombre_producto = input("Ingrese el nombre del producto: ")
                cursor.execute("SELECT * FROM producto WHERE nombre LIKE %s", (f"%{nombre_producto}%",))
            else:
                print("Opción inválida.")
                return

            producto = cursor.fetchone()
            if producto:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Costo: ${producto[3]:.2f}, "
                      f"Precio Venta: ${producto[4]:.2f}, Cantidad: {producto[5]}, ID Orden: {producto[6]}, ID Pedido: {producto[7]}")
            else:
                print("No se encontró el producto con los datos proporcionados.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar productos: {e}")
    finally:
        cursor.close()
        db.close() 
# ---------------- Editar ---------------- 
def editar_producto():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Producto ---")
        id_producto = input("Ingrese el ID del producto que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        nueva_descripcion = input("Ingrese la nueva descripción: ")
        nuevo_costo = float(input("Ingrese el nuevo costo: "))
        nuevo_precio_venta = float(input("Ingrese el nuevo precio de venta: "))
        nueva_cantidad = int(input("Ingrese la nueva cantidad en stock: "))

        sql = """
        UPDATE producto 
        SET nombre = %s, descripcion = %s, costo = %s, precioVenta = %s, cantidad = %s 
        WHERE idProducto = %s
        """
        cursor.execute(sql, (nuevo_nombre, nueva_descripcion, nuevo_costo, nuevo_precio_venta, nueva_cantidad, id_producto))
        db.commit()
        print("¡Producto editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar producto: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_producto():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Producto ---")
        id_producto = input("Ingrese el ID del producto que desea eliminar: ")

        sql = "DELETE FROM producto WHERE idProducto = %s"
        cursor.execute(sql, (id_producto,))
        db.commit()
        print("¡Producto eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar producto: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ PROVEEDOR ================================
def menu_proveedores():
    while True:
        print("\n--- Menú CRUD Proveedores ---")
        print("1. Crear Proveedor")
        print("2. Consultar Proveedores")
        print("3. Editar Proveedor")
        print("4. Eliminar Proveedor")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_proveedor()
        elif opcion == "2":
            consultar_proveedores()
        elif opcion == "3":
            editar_proveedor()
        elif opcion == "4":
            eliminar_proveedor()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_proveedor():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Proveedor ---")
        id_proveedor = input("Ingrese el ID del proveedor: ")
        nombre = input("Ingrese el nombre completo del proveedor: ")
        telefono = input("Ingrese el número de teléfono del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        certificacion = input("Ingrese la certificación del proveedor: ")
        ced_venta = input("Ingrese la cédula del gerente de ventas asociado: ")

        sql = """
        INSERT INTO proveedor (idProveedor, nombreCompleto, telefono, dirreccion, certificación, ced_Venta) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_proveedor, nombre, telefono, direccion, certificacion, ced_venta))
        db.commit()
        print("¡Proveedor creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear el proveedor: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ---------------- 
def consultar_proveedores():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Proveedores ---")
        print("1. Ver todos los proveedores")
        print("2. Buscar un proveedor específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los proveedores
            cursor.execute("SELECT * FROM proveedor")
            resultados = cursor.fetchall()
            if resultados:
                for proveedor in resultados:
                    print(f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Teléfono: {proveedor[2]}, Dirección: {proveedor[3]}, "
                          f"Certificación: {proveedor[4]}, Gerente de Ventas: {proveedor[5]}")
            else:
                print("No se encontraron proveedores registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Proveedor Específico ---")
            id_proveedor = input("Ingrese el ID del proveedor: ")
            cursor.execute("SELECT * FROM proveedor WHERE idProveedor = %s", (id_proveedor,))
            proveedor = cursor.fetchone()
            if proveedor:
                print(f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Teléfono: {proveedor[2]}, Dirección: {proveedor[3]}, "
                      f"Certificación: {proveedor[4]}, Gerente de Ventas: {proveedor[5]}")
            else:
                print("No se encontró el proveedor con el ID proporcionado.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar proveedores: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_proveedor():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Proveedor ---")
        id_proveedor = input("Ingrese el ID del proveedor que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre completo del proveedor: ")
        nuevo_telefono = input("Ingrese el nuevo número de teléfono: ")
        nueva_direccion = input("Ingrese la nueva dirección: ")
        nueva_certificacion = input("Ingrese la nueva certificación: ")
        nueva_ced_venta = input("Ingrese la nueva cédula del gerente de ventas asociado: ")

        sql = """
        UPDATE proveedor 
        SET nombreCompleto = %s, telefono = %s, dirreccion = %s, certificación = %s, ced_Venta = %s 
        WHERE idProveedor = %s
        """
        cursor.execute(sql, (nuevo_nombre, nuevo_telefono, nueva_direccion, nueva_certificacion, nueva_ced_venta, id_proveedor))
        db.commit()
        print("¡Proveedor editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar el proveedor: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_proveedor():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Proveedor ---")
        id_proveedor = input("Ingrese el ID del proveedor que desea eliminar: ")

        sql = "DELETE FROM proveedor WHERE idProveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        db.commit()
        print("¡Proveedor eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar el proveedor: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ RECORDATORIO ================================
def menu_recordatorios():
    while True:
        print("\n--- Menú CRUD Recordatorios ---")
        print("1. Crear Recordatorio")
        print("2. Consultar Recordatorios")
        print("3. Editar Recordatorio")
        print("4. Eliminar Recordatorio")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_recordatorio()
        elif opcion == "2":
            consultar_recordatorios()
        elif opcion == "3":
            editar_recordatorio()
        elif opcion == "4":
            eliminar_recordatorio()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_recordatorio():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Recordatorio ---")
        id_recordatorio = input("Ingrese el ID del recordatorio: ")
        titulo = input("Ingrese el título del recordatorio: ")
        descripcion = input("Ingrese la descripción del recordatorio: ")
        fecha_max = input("Ingrese la fecha máxima (YYYY-MM-DD): ")
        nivel_relevancia = int(input("Ingrese el nivel de relevancia (1 a 5): "))
        secretaria_cedula = input("Ingrese la cédula de la secretaria asociada: ")
        ced_adm = input("Ingrese la cédula del gerente administrativo asociado: ")

        sql = """
        INSERT INTO recordatorio (idRecordatorio, titulo, descripcion, fechaMax, nivelRelevancia, SecretariaCedula, ced_adm) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_recordatorio, titulo, descripcion, fecha_max, nivel_relevancia, secretaria_cedula, ced_adm))
        db.commit()
        print("¡Recordatorio creado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear el recordatorio: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ---------------- 
def consultar_recordatorios():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Recordatorios ---")
        print("1. Ver todos los recordatorios")
        print("2. Buscar un recordatorio específico")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todos los recordatorios
            cursor.execute("SELECT * FROM recordatorio")
            resultados = cursor.fetchall()
            if resultados:
                for recordatorio in resultados:
                    print(f"ID: {recordatorio[0]}, Título: {recordatorio[1]}, Descripción: {recordatorio[2]}, "
                          f"Fecha Máxima: {recordatorio[3]}, Nivel Relevancia: {recordatorio[4]}, "
                          f"Secretaria: {recordatorio[5]}, Gerente Administrativo: {recordatorio[6]}")
            else:
                print("No se encontraron recordatorios registrados.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Recordatorio Específico ---")
            id_recordatorio = input("Ingrese el ID del recordatorio: ")
            cursor.execute("SELECT * FROM recordatorio WHERE idRecordatorio = %s", (id_recordatorio,))
            recordatorio = cursor.fetchone()
            if recordatorio:
                print(f"ID: {recordatorio[0]}, Título: {recordatorio[1]}, Descripción: {recordatorio[2]}, "
                      f"Fecha Máxima: {recordatorio[3]}, Nivel Relevancia: {recordatorio[4]}, "
                      f"Secretaria: {recordatorio[5]}, Gerente Administrativo: {recordatorio[6]}")
            else:
                print("No se encontró el recordatorio con el ID proporcionado.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar recordatorios: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_recordatorio():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Recordatorio ---")
        id_recordatorio = input("Ingrese el ID del recordatorio que desea editar: ")
        nuevo_titulo = input("Ingrese el nuevo título: ")
        nueva_descripcion = input("Ingrese la nueva descripción: ")
        nueva_fecha_max = input("Ingrese la nueva fecha máxima (YYYY-MM-DD): ")
        nuevo_nivel_relevancia = int(input("Ingrese el nuevo nivel de relevancia (1 a 5): "))
        nueva_secretaria_cedula = input("Ingrese la nueva cédula de la secretaria asociada: ")
        nueva_ced_adm = input("Ingrese la nueva cédula del gerente administrativo asociado: ")

        sql = """
        UPDATE recordatorio 
        SET titulo = %s, descripcion = %s, fechaMax = %s, nivelRelevancia = %s, 
            SecretariaCedula = %s, ced_adm = %s 
        WHERE idRecordatorio = %s
        """
        cursor.execute(sql, (nuevo_titulo, nueva_descripcion, nueva_fecha_max, nuevo_nivel_relevancia, 
                             nueva_secretaria_cedula, nueva_ced_adm, id_recordatorio))
        db.commit()
        print("¡Recordatorio editado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar el recordatorio: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_recordatorio():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Recordatorio ---")
        id_recordatorio = input("Ingrese el ID del recordatorio que desea eliminar: ")

        sql = "DELETE FROM recordatorio WHERE idRecordatorio = %s"
        cursor.execute(sql, (id_recordatorio,))
        db.commit()
        print("¡Recordatorio eliminado exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar el recordatorio: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ SECRETARIA ================================
def menu_secretarias():
    while True:
        print("\n--- Menú CRUD Secretarias ---")
        print("1. Crear Secretaria")
        print("2. Consultar Secretarias")
        print("3. Editar Secretaria")
        print("4. Eliminar Secretaria")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_secretaria()
        elif opcion == "2":
            consultar_secretarias()
        elif opcion == "3":
            editar_secretaria()
        elif opcion == "4":
            eliminar_secretaria()
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
# ---------------- Crear ----------------
def crear_secretaria():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Crear Secretaria ---")
        cedula = input("Ingrese la cédula de la secretaria (única): ")
        nombre = input("Ingrese el nombre completo de la secretaria: ")

        sql = "INSERT INTO secretaria (cedula, nomCompleto) VALUES (%s, %s)"
        cursor.execute(sql, (cedula, nombre))
        db.commit()
        print("¡Secretaria creada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al crear secretaria: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Consultar ---------------- 
def consultar_secretarias():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Consultar Secretarias ---")
        print("1. Ver todas las secretarias")
        print("2. Buscar una secretaria específica")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Consulta de todas las secretarias
            cursor.execute("SELECT * FROM secretaria")
            resultados = cursor.fetchall()
            if resultados:
                for secretaria in resultados:
                    print(f"Cédula: {secretaria[0]}, Nombre: {secretaria[1]}")
            else:
                print("No se encontraron secretarias registradas.")

        elif opcion == "2":
            # Consulta individual
            print("\n--- Buscar Secretaria Específica ---")
            cedula = input("Ingrese la cédula de la secretaria: ")
            cursor.execute("SELECT * FROM secretaria WHERE cedula = %s", (cedula,))
            secretaria = cursor.fetchone()
            if secretaria:
                print(f"Cédula: {secretaria[0]}, Nombre: {secretaria[1]}")
            else:
                print("No se encontró la secretaria con la cédula proporcionada.")
        else:
            print("Opción inválida.")
    except mysql.connector.Error as e:
        print(f"Error al consultar secretarias: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Editar ---------------- 
def editar_secretaria():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Editar Secretaria ---")
        cedula = input("Ingrese la cédula de la secretaria que desea editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre completo de la secretaria: ")

        sql = "UPDATE secretaria SET nomCompleto = %s WHERE cedula = %s"
        cursor.execute(sql, (nuevo_nombre, cedula))
        db.commit()
        print("¡Secretaria editada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al editar secretaria: {e}")
    finally:
        cursor.close()
        db.close()
# ---------------- Eliminar Registro ---------------- 
def eliminar_secretaria():
    try:
        db = conectar_bd()
        cursor = db.cursor()
        print("\n--- Eliminar Secretaria ---")
        cedula = input("Ingrese la cédula de la secretaria que desea eliminar: ")

        sql = "DELETE FROM secretaria WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        db.commit()
        print("¡Secretaria eliminada exitosamente!")
    except mysql.connector.Error as e:
        print(f"Error al eliminar secretaria: {e}")
    finally:
        cursor.close()
        db.close()

# ================================ MENU DE CRUD GENERAL ================================
def menu_general():
    while True:
        print("\n--- Menú General del CRUD de las tablas Principales ---")
        print("1. Gestionar Clientes")
        print("2. Gestionar Gerentes Administrativos")
        print("3. Gestionar Gerentes de Ventas")
        print("4. Gestionar Órdenes de Compra")
        print("5. Gestionar Pedidos")
        print("6. Gestionar Productos")
        print("7. Gestionar Proveedores")
        print("8. Gestionar Recordatorios")
        print("9. Gestionar Secretarias")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_gerentes_adm()
        elif opcion == "3":
            menu_gerentes_venta()
        elif opcion == "4":
            menu_ordenes_compra()
        elif opcion == "5":
            menu_pedidos()
        elif opcion == "6":
            menu_productos()
        elif opcion == "7":
            menu_proveedores()  # Asegúrate de implementar este menú si no está hecho
        elif opcion == "8":
            menu_recordatorios()
        elif opcion == "9":
            menu_secretarias()
        elif opcion == "10":
            print("¡Saliendo del sistema!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu_general()
    
















    