from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()

class crud_productos:
    def consultar(self, buscar):
        sql = "SELECT * FROM productos WHERE codigo LIKE %s OR descripcion LIKE %s ORDER BY descripcion"
        termino = f"%{buscar}%"
        return db.consultar(sql, (termino, termino))

    def administrar(self, datos):
        try:
            accion = datos.get('accion')
            if accion == 'nuevo':
                sql = """
                    INSERT INTO productos(codigo,descripcion,estado)
                    VALUES(%s,%s,%s)
                """
                valores = (datos['codigo'],datos['descripcion'],datos['estado'])
            elif accion == 'modificar':
                sql = """
                    UPDATE productos SET codigo=%s,descripcion=%s,estado=%s
                    WHERE idProducto=%s
                """
                valores = (datos['codigo'],datos['descripcion'],datos['estado'],datos['idProducto'])
            elif accion == 'eliminar':
                sql = """
                    DELETE FROM productos WHERE idProducto=%s
                """
                valores = (datos['idProducto'],)
            else:
                return f"Error: Acción desconocida '{accion}'."
            return db.ejecutar(sql,valores)
        except Error as e:
            return f"Error al guardar el producto: {e}"