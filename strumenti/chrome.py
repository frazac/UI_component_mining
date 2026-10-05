"""
Chrome headless per PDF e schermate. Chrome 154 a volte scrive il file e poi non si chiude:
qui si aspetta che il file compaia e smetta di crescere, poi si chiude Chrome.
"""
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def esegui(argomenti, uscita, attesa=180, stabile=2.0, gpu=False):
    """argomenti: opzioni e indirizzo (senza --user-data-dir); uscita: il file che Chrome deve scrivere"""
    uscita = Path(uscita)
    if uscita.exists():
        uscita.unlink()
    profilo = tempfile.mkdtemp(prefix="chrome-")
    base = [CHROME, "--headless=new", "--no-first-run", "--no-default-browser-check", f"--user-data-dir={profilo}"]
    # schermate di siti in WebGL: con la GPU (altrimenti restano vuote); PDF: senza
    base += ["--enable-gpu", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"] if gpu else ["--disable-gpu"]
    p = subprocess.Popen(base + list(argomenti),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        inizio, ultima, da = time.time(), -1, None
        while time.time() - inizio < attesa:
            if p.poll() is not None and not uscita.exists():
                raise RuntimeError("Chrome si è chiuso senza scrivere " + uscita.name)
            if uscita.exists():
                dim = uscita.stat().st_size
                if dim and dim == ultima:
                    if time.time() - da >= stabile:
                        return uscita
                else:
                    ultima, da = dim, time.time()
            time.sleep(0.5)
        raise TimeoutError(f"Chrome: {uscita.name} non scritto in {attesa} s")
    finally:
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(5)
            except subprocess.TimeoutExpired:
                p.kill()
        shutil.rmtree(profilo, ignore_errors=True)
