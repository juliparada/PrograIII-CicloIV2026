from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
# pyrefly: ignore[missing-import]
import crud_usuarios_usss025125

port = 3000
crudUsuarios = crud_usuarios_usss025125.crud_usuarios_usss025125()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            longitud = int(self.headers.get('Content-Length', 0))
            cuerpo = self.rfile.read(longitud)
            datos = json.loads(cuerpo.decode("utf-8")) if cuerpo else {}

            if self.path == "/usuario":
                resultado = crudUsuarios.administrar(datos)
                respuesta = {'msg': resultado}
            elif self.path == "/login":
                usuario = datos.get('usuario', '')
                clave = datos.get('clave', '')
                respuesta = crudUsuarios.login(usuario, clave)
            else:
                self.send_error(404, "Ruta no encontrada")
                return

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'msg': str(e)}).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/usuarios":
            buscar = qs.get('buscar', [''])[0]
            datos = crudUsuarios.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))

        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            form = qs.get('form', [''])[0]
            self.path = f"/modulos/{form}.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        else:
            return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    print("=====================================================")
    print(f" Servidor iniciado con éxito en: http://localhost:{port}")
    print("=====================================================")
    servidor = HTTPServer(("localhost", port), miServidor)
    servidor.serve_forever()
