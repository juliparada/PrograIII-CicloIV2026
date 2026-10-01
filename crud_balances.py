from mysql.connector.errors import Error
from datetime import datetime   
# pyrefly: ignore [missing-import]
import conexion

class crud_balances:
    def __init__(self):
        self.db = conexion.Conexion()
        self.verificar_y_crear_tabla()

    def _ping(self):
        """Reconecta si la conexion MySQL se perdio por inactividad."""
        try:
            self.db.conexion.ping(reconnect=True, attempts=3, delay=1)
        except Exception:
            self.db = conexion.Conexion()

    def verificar_y_crear_tabla(self):
        try:
            sql_crear = """
                CREATE TABLE IF NOT EXISTS balances (
                    idBalance int(10) NOT NULL AUTO_INCREMENT,
                    codigo char(10) NOT NULL,
                    desde date NOT NULL,
                    hasta date NOT NULL,
                    balance decimal(12,2) NOT NULL,
                    precio decimal(10,2) NOT NULL,
                    estado varchar(50) NOT NULL DEFAULT 'Histórico',
                    PRIMARY KEY (idBalance)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
            """
            self._ping()
            cursor = self.db.conexion.cursor()
            cursor.execute(sql_crear)
            self.db.conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Nota en verificar_y_crear_tabla balances: {e}")

    def calcular_precio(self, monto_balance):
        try:
            monto = float(monto_balance)
            sql = "SELECT precio_base, adicional, porcentaje FROM tabla_tarifaria WHERE %s BETWEEN desde AND hasta LIMIT 1"
            self._ping()
            cursor = self.db.conexion.cursor(dictionary=True)
            cursor.execute(sql, (monto,))
            fila = cursor.fetchone()
            cursor.close()
            if fila:
                base = float(fila['precio_base'])
                adicional = float(fila['adicional'])
                return round(base + adicional, 2)
            return 0.00
        except Exception as e:
            print(f"Error al calcular precio: {e}")
            return 0.00

    def consultar(self, codigo=""):
        try:
            if codigo:
                sql = f"SELECT * FROM balances WHERE codigo LIKE '%{codigo}%' ORDER BY desde ASC"
            else:
                sql = "SELECT * FROM balances ORDER BY desde ASC"

            filas = self.db.consultar(sql)
            if not filas:
                return []

            resultado = []
            hoy = datetime.now().date()
            for f in filas:
                d_str = str(f['desde'])
                h_str = str(f['hasta'])

                estado = f['estado']
                try:
                    f_desde = datetime.strptime(d_str[:10], "%Y-%m-%d").date()
                    f_hasta = datetime.strptime(h_str[:10], "%Y-%m-%d").date()
                    if f_desde <= hoy <= f_hasta:
                        estado = "Vigente según fecha"
                    else:
                        estado = "Histórico"
                except Exception:
                    pass

                resultado.append({
                    'idBalance': f['idBalance'],
                    'codigo': f['codigo'],
                    'desde': d_str[:10],
                    'hasta': h_str[:10],
                    'balance': float(f['balance']),
                    'precio': float(f['precio']),
                    'estado': estado
                })
            return resultado
        except Exception as e:
            print(f"Error al consultar balances: {e}")
            return []

    def administrar(self, datos):
        try:
            accion = datos.get('accion')

            # 1. ACCIÓN ELIMINAR
            if accion == 'eliminar':
                id_balance = datos.get('idBalance')
                if not id_balance:
                    return "Error: No se proporcionó el idBalance para eliminar."
                sql = "DELETE FROM balances WHERE idBalance = %s"
                return self.db.ejecutar(sql, (id_balance,))

            # 2. VALIDACIÓN: EL CLIENTE DEBE EXISTIR Y NO SER PARTICULAR (DEBE SER EMPRESA)
            codigo = str(datos.get('codigo', '')).strip()
            if not codigo:
                return "Error: El código de empresa es obligatorio."

            self._ping()
            cursor = self.db.conexion.cursor(dictionary=True)
            cursor.execute("SELECT nombre, tipo FROM clientes WHERE codigo = %s LIMIT 1", (codigo,))
            cliente = cursor.fetchone()
            cursor.close()

            if not cliente:
                return f"Error: No existe ningún cliente registrado con el código '{codigo}'."

            if str(cliente['tipo']).strip().lower() != 'empresa':
                return f"Error: El cliente '{cliente['nombre']}' es de tipo '{cliente['tipo']}'. Solo los clientes de tipo Empresa pueden registrar balances."

            # Después de validar el cliente
            id_cliente = cliente['idCliente']  # lo obtienes de la consulta

            if accion == 'nuevo':
                sql = """
                    INSERT INTO balances(idCliente, codigo, desde, hasta, balance, precio, estado)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (id_cliente, codigo, datos['desde'], datos['hasta'], datos['balance'], precio, estado)

            elif accion == 'modificar':
                sql = """
                    UPDATE balances 
                    SET idCliente=%s, codigo=%s, desde=%s, hasta=%s, balance=%s, precio=%s, estado=%s
                    WHERE idBalance=%s
                """
                valores = (id_cliente, codigo, datos['desde'], datos['hasta'], datos['balance'], precio, estado, datos['idBalance'])


            # 3. VALIDACIÓN: NO REPETIR EL BALANCE DEL MISMO AÑO PARA EL MISMO CLIENTE
            f_desde_str = str(datos.get('desde', ''))[:10]
            if not f_desde_str:
                return "Error: La fecha de inicio (Desde) es obligatoria."

            try:
                ano_desde = datetime.strptime(f_desde_str, "%Y-%m-%d").year
            except Exception:
                return "Error: Formato de fecha inválido. Debe ser YYYY-MM-DD."

            cursor2 = self.db.conexion.cursor(dictionary=True)
            if accion == 'nuevo':
                cursor2.execute(
                    "SELECT idBalance FROM balances WHERE codigo = %s AND YEAR(desde) = %s LIMIT 1",
                    (codigo, ano_desde)
                )
                if cursor2.fetchone():
                    cursor2.close()
                    return f"Error: Ya existe un balance registrado para la empresa con código '{codigo}' en el año {ano_desde}. No se puede registrar más de un balance por año para la misma empresa."
            elif accion == 'modificar':
                id_balance = datos.get('idBalance')
                cursor2.execute(
                    "SELECT idBalance FROM balances WHERE codigo = %s AND YEAR(desde) = %s AND idBalance != %s LIMIT 1",
                    (codigo, ano_desde, id_balance)
                )
                if cursor2.fetchone():
                    cursor2.close()
                    return f"Error: Ya existe otro balance registrado para la empresa con código '{codigo}' en el año {ano_desde}."
            cursor2.close()

            # 4. CALCULAR PRECIO AUTOMÁTICAMENTE SEGÚN LA TABLA TARIFARIA
            precio = float(datos.get('precio', 0))
            if precio <= 0:
                precio = self.calcular_precio(datos.get('balance', 0))

            # 5. DETERMINAR ESTADO SEGÚN FECHAS
            estado = datos.get('estado', 'Histórico')
            try:
                hoy = datetime.now().date()
                f_desde = datetime.strptime(f_desde_str, "%Y-%m-%d").date()
                f_hasta = datetime.strptime(str(datos.get('hasta', ''))[:10], "%Y-%m-%d").date()
                if f_desde <= hoy <= f_hasta:
                    estado = "Vigente según fecha"
                else:
                    estado = "Histórico"
            except Exception:
                pass

            # 6. INSERTAR O ACTUALIZAR
            if accion == 'nuevo':
                sql = """
                    INSERT INTO balances(codigo, desde, hasta, balance, precio, estado)
                    VALUES(%s, %s, %s, %s, %s, %s)
                """
                valores = (codigo, datos['desde'], datos['hasta'], datos['balance'], precio, estado)
            elif accion == 'modificar':
                sql = """
                    UPDATE balances 
                    SET codigo=%s, desde=%s, hasta=%s, balance=%s, precio=%s, estado=%s
                    WHERE idBalance=%s
                """
                valores = (codigo, datos['desde'], datos['hasta'], datos['balance'], precio, estado, datos['idBalance'])
            else:
                return f"Error: Acción desconocida '{accion}'."

            return self.db.ejecutar(sql, valores)
        except Exception as e:
            return f"Error al administrar balance: {e}"

    