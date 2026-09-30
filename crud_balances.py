from mysql.connector.errors import Error
from datetime import datetime
# pyrefly: ignore [missing-import]
import conexion

class crud_balances:
    def __init__(self):
        self.db = conexion.Conexion()
        self.verificar_y_crear_tabla()

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
            cursor = self.db.conexion.cursor()
            cursor.execute(sql_crear)
            self.db.conexion.commit()
        except Error as e:
            print(f"Nota en verificar_y_crear_tabla balances: {e}")

    def calcular_precio(self, monto_balance):
        try:
            monto = float(monto_balance)
            sql = "SELECT precio_base, adicional, porcentaje FROM tabla_tarifaria WHERE %s BETWEEN desde AND hasta LIMIT 1"
            cursor = self.db.conexion.cursor(dictionary=True)
            cursor.execute(sql, (monto,))
            fila = cursor.fetchone()
            if fila:
                base = float(fila['precio_base'])
                adicional = float(fila['adicional'])
                return round(base + adicional, 2)
            return 0.00
        except Exception as e:
            print(f"Error al calcular precio: {e}")
            return 0.00

    def consultar(self, codigo=""):
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

    def administrar(self, datos):
        try:
            precio = float(datos.get('precio', 0))
            if precio <= 0:
                precio = self.calcular_precio(datos['balance'])

            estado = datos.get('estado', 'Histórico')
            try:
                hoy = datetime.now().date()
                f_desde = datetime.strptime(datos['desde'][:10], "%Y-%m-%d").date()
                f_hasta = datetime.strptime(datos['hasta'][:10], "%Y-%m-%d").date()
                if f_desde <= hoy <= f_hasta:
                    estado = "Vigente según fecha"
                else:
                    estado = "Histórico"
            except Exception:
                pass

            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO balances(codigo, desde, hasta, balance, precio, estado)
                    VALUES(%s, %s, %s, %s, %s, %s)
                """
                valores = (datos['codigo'], datos['desde'], datos['hasta'], datos['balance'], precio, estado)
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE balances 
                    SET codigo=%s, desde=%s, hasta=%s, balance=%s, precio=%s, estado=%s
                    WHERE idBalance=%s
                """
                valores = (datos['codigo'], datos['desde'], datos['hasta'], datos['balance'], precio, estado, datos['idBalance'])
            else:
                sql = "DELETE FROM balances WHERE idBalance=%s"
                valores = (datos['idBalance'],)

            return self.db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al administrar balance: {e}"
