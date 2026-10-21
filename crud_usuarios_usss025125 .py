from mysql.connector.errors import Error
# pyrefly: ignore[missing-import] 
import conexion

db = conexion.Conexion()

class crud_usuarios_usss025125:
    def consultar(self, buscar=""):
        if buscar:
            sql = f"SELECT * FROM usuarios_usss025125 WHERE usuario LIKE '%{buscar}%' OR nombre LIKE '%{buscar}%' OR direccion LIKE '%{buscar}%' OR telefono LIKE '%{buscar}%'"
        else:
            sql = "SELECT * FROM usuarios_usss025125"
        return db.consultar(sql)

    def administrar(self, datos):
        try:
            if datos.get('accion') == 'nuevo':
                sql = """
                    INSERT INTO usuarios_usss025125(usuario, clave, nombre, direccion, telefono)
                    VALUES(%s, %s, %s, %s, %s)
                """
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'])
            elif datos.get('accion') == 'modificar':
                sql = """
                    UPDATE usuarios_usss025125 
                    SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s
                    WHERE idUsuario=%s
                """
                valores = (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], datos['idUsuario'])
            elif datos.get('accion') == 'eliminar':
                sql = """
                    DELETE FROM usuarios_usss025125 WHERE idUsuario=%s
                """
                valores = (datos['idUsuario'],)
            else:
                return "Accion no valida"

            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al procesar el usuario: {e}"

    def login(self, usuario, clave):
        try:
            sql = "SELECT idUsuario, usuario, nombre FROM usuarios_usss025125 WHERE usuario=%s AND clave=%s"
            filas = db.consultar(sql, (usuario, clave))
            if filas and len(filas) > 0:
                return {'status': 'ok', 'msg': 'ok', 'usuario': filas[0]}
            else:
                return {'status': 'error', 'msg': 'Acceso denegado: Usuario o clave incorrectos'}
        except Error as e:
            return {'status': 'error', 'msg': f"Error en login: {e}"}
