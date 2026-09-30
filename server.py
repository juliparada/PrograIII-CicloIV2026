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
        try:
            urlParse = urlparse(self.path)
            longitud = int(self.headers.get('Content-Length', 0))
            cuerpo = self.rfile.read(longitud).decode("utf-8")
            
            try:
                datos_json = json.loads(cuerpo)
            except Exception:
                try:
                    cuerpo_unquoted = parse.unquote(cuerpo)
                    datos_json = json.loads(cuerpo_unquoted)
                except Exception:
                    datos_json = {}

            if urlParse.path in ["/tarifa", "/tarifas"]:
                msg = crudTarifas.administrar(datos_json)
            elif urlParse.path in ["/balance", "/balances"]:
                msg = crudBalances.administrar(datos_json)
            else:
                msg = crudClientes.administrar(datos_json)

            respuesta = {'msg': msg}
            resp_bytes = json.dumps(respuesta, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        except Exception as e:
            print(f"Error en do_POST: {e}")
            respuesta = {'msg': f"Error en servidor: {e}"}
            resp_bytes = json.dumps(respuesta).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
       
        if urlParse.path == "/clientes":
            datos = crudClientes.consultar(qs.get("buscar", [""])[0])
            respuesta = {"array": datos if datos is not None else []}
            resp_bytes = json.dumps(respuesta, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        if urlParse.path == "/tarifas":
            datos = crudTarifas.consultar(qs.get("buscar", [""])[0])
            respuesta = {"array": datos if datos is not None else []}
            resp_bytes = json.dumps(respuesta, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        if urlParse.path == "/balances":
            codigo = qs.get("codigo", [""])[0]
            datos = crudBalances.consultar(codigo)
            respuesta = {"array": datos if datos is not None else []}
            resp_bytes = json.dumps(respuesta, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        if urlParse.path == "/calcular_tarifa":
            balance_val = qs.get("balance", ["0"])[0]
            precio = crudBalances.calcular_precio(balance_val)
            respuesta = {"precio": precio}
            resp_bytes = json.dumps(respuesta, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        if self.path == "/":
            self.path = "/index.html"
            
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    print(f"Servidor corriendo en el puerto {port} -> http://localhost:{port}")
    server = HTTPServer(("localhost", port), miServidor)
    server.serve_forever()
