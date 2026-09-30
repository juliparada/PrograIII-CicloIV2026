from mysql.connector.errors import Error
# pyrefly: ignore [missing-import]
import conexion

TARIFAS_INICIALES = [
    (1, 0.01, 500.00, 1.50, 0.00, 0.00),
    (2, 500.01, 1000.00, 1.50, 3.00, 0.00),
    (3, 1000.01, 2000.00, 3.00, 3.00, 0.00),
    (4, 2000.01, 3000.00, 6.00, 3.00, 0.00),
    (5, 3000.01, 6000.00, 9.00, 2.00, 0.00),
    (6, 8000.01, 18000.00, 15.00, 2.00, 0.00),
    (7, 18000.01, 30000.00, 39.00, 2.00, 0.00),
    (8, 30000.01, 60000.00, 63.00, 1.00, 0.00),
    (9, 60000.01, 100000.00, 93.00, 0.80, 0.00),
    (10, 100000.01, 200000.00, 125.00, 0.70, 0.00),
    (11, 200000.01, 300000.00, 195.00, 0.60, 0.00),
    (12, 300000.01, 400000.00, 255.00, 0.45, 0.00),
    (13, 400000.01, 500000.00, 300.00, 0.40, 0.00),
    (14, 500000.01, 1000000.00, 340.00, 0.30, 0.00),
    (15, 1000000.01, 99999999.99, 490.00, 0.18, 0.00)
]

class crud_tarifas:
    def __init__(self):
        self.db = conexion.Conexion()
        self.verificar_y_crear_tabla()

    def verificar_y_crear_tabla(self):
        try:
            sql_crear = """
                CREATE TABLE IF NOT EXISTS tabla_tarifaria (
                    idTarifa int(10) NOT NULL AUTO_INCREMENT,
                    desde decimal(12,2) NOT NULL,
                    hasta decimal(12,2) NOT NULL,
                    precio_base decimal(10,2) NOT NULL,
                    adicional decimal(10,2) NOT NULL,
                    porcentaje decimal(5,2) NOT NULL DEFAULT 0.00,
                    PRIMARY KEY (idTarifa)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
            """
            cursor = self.db.conexion.cursor()
            cursor.execute(sql_crear)
            self.db.conexion.commit()

            # Verificar si ya tiene datos
            cursor.execute("SELECT COUNT(*) FROM tabla_tarifaria")
            total = cursor.fetchone()[0]
            if total == 0:
                sql_insert = """
                    INSERT INTO tabla_tarifaria (idTarifa, desde, hasta, precio_base, adicional, porcentaje)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(sql_insert, TARIFAS_INICIALES)
                self.db.conexion.commit()
                print("Tabla tarifaria inicializada con los 15 rangos.")
        except Error as e:
            print(f"Nota en verificar_y_crear_tabla: {e}")

    def consultar(self, buscar=""):
        filas = self.db.consultar("SELECT * FROM tabla_tarifaria ORDER BY desde ASC")
        if not filas:
            return []
        
        # Convertir Decimal a float para que json.dumps no falle
        resultado = []
        for f in filas:
            resultado.append({
                'idTarifa': f['idTarifa'],
                'desde': float(f['desde']),
                'hasta': float(f['hasta']),
                'precio_base': float(f['precio_base']),
                'adicional': float(f['adicional']),
                'porcentaje': float(f['porcentaje'])
            })
        return resultado

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO tabla_tarifaria(desde, hasta, precio_base, adicional, porcentaje)
                    VALUES(%s, %s, %s, %s, %s)
                """
                valores = (datos['desde'], datos['hasta'], datos['precio_base'], datos['adicional'], datos['porcentaje'])
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE tabla_tarifaria 
                    SET desde=%s, hasta=%s, precio_base=%s, adicional=%s, porcentaje=%s
                    WHERE idTarifa=%s
                """
                valores = (datos['desde'], datos['hasta'], datos['precio_base'], datos['adicional'], datos['porcentaje'], datos['idTarifa'])
            else:
                sql = "DELETE FROM tabla_tarifaria WHERE idTarifa=%s"
                valores = (datos['idTarifa'],)
            return self.db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al administrar tarifa: {e}"
