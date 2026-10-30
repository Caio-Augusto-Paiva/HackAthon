/**
 * Modo navegador (site publicado na Cloudflare): a mesma API FastAPI roda dentro do navegador com o Pyodide.
 * Nenhuma requisição sai para um servidor de aplicação; o histórico fica no IndexedDB deste navegador.
 * Só é usado quando o build é feito com ``VITE_MODO_NAVEGADOR=1`` (ver ``npm run build:navegador``).
 */
const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/';

const INICIAR = `
import os, sys, json, zipfile, io
import anyio.to_thread

async def _direto(func, *args, **_):
    return func(*args)

anyio.to_thread.run_sync = _direto  # o Pyodide não tem threads: endpoints síncronos rodam direto

zipfile.ZipFile(io.BytesIO(bytes(_zip.to_py()))).extractall('/app')
os.chdir('/app'); sys.path.insert(0, '/app')
os.environ['ANAMNESE_DB'] = '/dados/anamnese.db'
from api.main import criar_app
from api.db.conexao import inicializar
app = criar_app()
inicializar(app.state.config.db_path)

async def chamar(metodo, caminho, corpo=None):
    corpo_b = b'' if corpo is None else corpo.encode()
    lido = False
    async def receive():
        nonlocal lido
        if lido:
            return {'type': 'http.disconnect'}
        lido = True
        return {'type': 'http.request', 'body': corpo_b, 'more_body': False}
    resposta = {'status': 500, 'corpo': b''}
    async def send(m):
        if m['type'] == 'http.response.start':
            resposta['status'] = m['status']
        elif m['type'] == 'http.response.body':
            resposta['corpo'] += m.get('body', b'')
    rota, _, consulta = caminho.partition('?')
    escopo = {'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1', 'method': metodo, 'scheme': 'http',
              'path': rota, 'raw_path': rota.encode(), 'query_string': consulta.encode(), 'root_path': '',
              'headers': [(b'host', b'localhost'), (b'content-type', b'application/json'), (b'accept', b'application/json')],
              'client': ('127.0.0.1', 0), 'server': ('localhost', 80)}
    await app(escopo, receive, send)
    return json.dumps([resposta['status'], resposta['corpo'].decode()])
`;

type Pyodide = {
  FS: { mkdirTree(c: string): void; mount(t: unknown, o: object, c: string): void; filesystems: { IDBFS: unknown };
    syncfs(popular: boolean, cb: (e: unknown) => void): void };
  loadPackage(p: string[]): Promise<void>;
  pyimport(n: string): { install(u: string): Promise<void> };
  globals: { set(n: string, v: unknown): void; get(n: string): (m: string, c: string, b?: string) => Promise<string> };
  runPythonAsync(c: string): Promise<unknown>;
};

let pronto: Promise<(m: string, c: string, b?: string) => Promise<string>> | null = null;

function sincronizar(py: Pyodide, popular: boolean) {
  return new Promise<void>((ok) => py.FS.syncfs(popular, () => ok()));
}

async function carregar() {
  const { loadPyodide } = await import(/* @vite-ignore */ `${PYODIDE}pyodide.mjs`) as {
    loadPyodide(o: { indexURL: string }): Promise<Pyodide> };
  const py = await loadPyodide({ indexURL: PYODIDE });
  py.FS.mkdirTree('/dados');
  py.FS.mount(py.FS.filesystems.IDBFS, {}, '/dados');
  await sincronizar(py, true);
  await py.loadPackage(['fastapi', 'pydantic', 'starlette', 'micropip']);
  await py.pyimport('micropip').install(new URL('/py/python_multipart-0.0.32-py3-none-any.whl', location.href).href);
  const zip = await fetch('/py/app.zip').then((r) => r.arrayBuffer());
  py.globals.set('_zip', new Uint8Array(zip));
  await py.runPythonAsync(INICIAR);
  const chamar = py.globals.get('chamar');
  return async (metodo: string, caminho: string, corpo?: string) => {
    const r = await chamar(metodo, caminho, corpo);
    if (metodo !== 'GET') await sincronizar(py, false);
    return r;
  };
}

/** Executa ``metodo /api{caminho}`` na API dentro do navegador e devolve uma ``Response`` como o ``fetch``. */
export async function chamarNoNavegador(metodo: string, caminho: string, corpo?: string): Promise<Response> {
  pronto ??= carregar();
  const [status, texto] = JSON.parse(await (await pronto)(metodo, `/api${caminho}`, corpo)) as [number, string];
  return new Response(texto, { status, headers: { 'Content-Type': 'application/json' } });
}
