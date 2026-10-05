#!/usr/bin/env python3
"""
PDF delle slide, uno per lingua.
  python3 strumenti/pdf.py [it en fr zh]      bozze in pdf/ui-components-<VERSION>.<lingua>.pdf
  python3 strumenti/pdf.py --pubblica          numero di versione +1, PDF in pdf/ e copia diretta nella cartella
                                               indicata in pdf.locale.json (es. OneDrive del semestre);
                                               le versioni precedenti lasciano la cartella e vanno in pdf/archivio/
pdf.locale.json (solo locale, fuori da git):
  {"cartella": "~/Library/CloudStorage/…", "nome": "COMPONENTS . ID2627 . SEM1", "versione": 0}
Le slide caricano gli esempi in iframe: serve un server http, che lo script avvia da sé se non c'è.
"""
import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import chrome
import schede

R = schede.RADICE
PORTA = 8771
NOME_LINGUA = {'it': 'IT', 'en': 'EN', 'fr': 'FR', 'zh': 'ZH'}
LOCALE = R / 'pdf.locale.json'


def server():
    with socket.socket() as s:
        if s.connect_ex(('127.0.0.1', PORTA)) == 0:
            return None
    p = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORTA), '--bind', '127.0.0.1', '--directory', str(R)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    return p


def stampa(lingua, uscita):
    for _ in range(3):  # a volte Chrome stampa la pagina ancora vuota: si riprova
        chrome.esegui(['--no-pdf-header-footer', '--virtual-time-budget=15000', '--run-all-compositor-stages-before-draw',
                       f'--print-to-pdf={uscita}', f'http://127.0.0.1:{PORTA}/slide.html?lingua={lingua}'], uscita, attesa=600)
        if uscita.stat().st_size > 200_000:
            return
    sys.exit(f'{uscita.name}: resta vuoto dopo 3 tentativi')


def onedrive_acceso():
    return subprocess.run(['pgrep', '-x', 'OneDrive'], capture_output=True).returncode == 0


def main():
    pubblica = '--pubblica' in sys.argv
    lingue = [a for a in sys.argv[1:] if not a.startswith('--')] or list(schede.LINGUE)
    cartella = R / 'pdf'
    cartella.mkdir(exist_ok=True)
    if pubblica:
        if not LOCALE.exists():
            sys.exit('manca pdf.locale.json (cartella di destinazione e nome dei PDF)')
        conf = json.loads(LOCALE.read_text())
        dest = Path(conf['cartella']).expanduser()
        if not dest.is_dir():
            sys.exit(f'cartella non trovata: {dest}')
        if 'OneDrive' in str(dest) and not onedrive_acceso():
            print('ATTENZIONE: OneDrive non è acceso: i PDF si caricano solo quando lo riapri')
        conf['versione'] += 1
    srv = server()
    try:
        for l in lingue:
            if pubblica:
                nome = f'{conf["nome"]} . v{conf["versione"]:02d} . {NOME_LINGUA[l]}.pdf'
            else:
                nome = f'ui-components-{(R / "VERSION").read_text().strip()}.{l}.pdf'
            uscita = cartella / nome
            stampa(l, uscita)
            print(f'pdf/{nome}  {uscita.stat().st_size / 1e6:.1f} MB')
            if pubblica:
                for vecchio in dest.glob(f'{conf["nome"]} . v* . {NOME_LINGUA[l]}.pdf'):
                    if vecchio.name != nome:
                        (cartella / 'archivio').mkdir(exist_ok=True)
                        shutil.move(str(vecchio), cartella / 'archivio' / vecchio.name)
                        print(f'  {vecchio.name}: dalla cartella a pdf/archivio/')
                shutil.copy2(uscita, dest / nome)
                print(f'  copiato in {dest.name}/{nome}')
        if pubblica:
            LOCALE.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + '\n')
    finally:
        if srv:
            srv.terminate()


if __name__ == '__main__':
    main()
