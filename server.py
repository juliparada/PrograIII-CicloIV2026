from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_productos

import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudProductos = crud_productos.crud_productos()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = json.loads(datos.decode("utf-8"))
        if self.path == "/cliente":
            resultado = crudClientes.administrar(datos)
        elif self.path == "/producto":
            resultado = crudProductos.administrar(datos)
        else:
            self.send_error(404, "Ruta no encontrada")
            return

        respuesta = {'msg': resultado}
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
    
        if urlParse.path in ("/clientes", "/productos"):
            buscar = qs.get('buscar', [''])[0]
            if urlParse.path == "/clientes":
                datos = crudClientes.consultar(buscar)
            else:
                datos = crudProductos.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))
        
        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            self.path = f"/modulos/{qs.get('form', [''])[0]}.html"
            return SimpleHTTPRequestHandler.do_GET(self)

print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost",port),miServidor)
server.serve_forever()