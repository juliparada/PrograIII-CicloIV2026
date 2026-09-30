from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
# pyrefly: ignore [missing-import]
import crud_clientes
# pyrefly: ignore [missing-import]
import crud_tarifas
# pyrefly: ignore [missing-import]
import crud_balances
import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudTarifas = crud_tarifas.crud_tarifas()
crudBalances = crud_balances.crud_balances()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        urlParse = urlparse(self.path)
        longitud = int(self.headers.get('Content-Length', 0))
        datos = self.rfile.read(longitud).decode("utf-8")
        datos = parse.unquote(datos)
        try:
            datos_json = json.loads(datos)
        except Exception:
            datos_json = {}

        if urlParse.path in ["/tarifa", "/tarifas"]:
            msg = crudTarifas.administrar(datos_json)
        elif urlParse.path in ["/balance", "/balances"]:
            msg = crudBalances.administrar(datos_json)
        else:
            msg = crudClientes.administrar(datos_json)

        respuesta = {'msg': msg}
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta, default=str).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
       
        if urlParse.path == "/clientes":
            datos = crudClientes.consultar(qs.get("buscar", [""])[0])
            respuesta = {"array": datos if datos is not None else []}
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, default=str).encode("utf-8"))
            return

        if urlParse.path == "/tarifas":
            datos = crudTarifas.consultar(qs.get("buscar", [""])[0])
            respuesta = {"array": datos if datos is not None else []}
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, default=str).encode("utf-8"))
            return

        if urlParse.path == "/balances":
            codigo = qs.get("codigo", [""])[0]
            datos = crudBalances.consultar(codigo)
            respuesta = {"array": datos if datos is not None else []}
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, default=str).encode("utf-8"))
            return

        if urlParse.path == "/calcular_tarifa":
            balance_val = qs.get("balance", ["0"])[0]
            precio = crudBalances.calcular_precio(balance_val)
            respuesta = {"precio": precio}
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, default=str).encode("utf-8"))
            return

        if self.path == "/":
            self.path = "/index.html"
            
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    print(f"Servidor corriendo en el puerto {port} -> http://localhost:{port}")
    server = HTTPServer(("localhost", port), miServidor)
    server.serve_forever()
