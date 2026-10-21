"""python -m engine BASE.json CASO.json — execução local de um caso."""
import argparse
import json
from pathlib import Path
from .casos import executar_caso


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base',type=Path)
    parser.add_argument('caso',type=Path)
    args=parser.parse_args(argv)
    try:
        base=json.loads(args.base.read_text(encoding='utf-8-sig'))
        caso=json.loads(args.caso.read_text(encoding='utf-8-sig'))
        resultado=executar_caso(base,caso)
    except (OSError,ValueError) as erro:
        resultado={'status':'erro','erro':str(erro)}
    print(json.dumps(resultado,ensure_ascii=True,allow_nan=False))
    return 0 if resultado['status']=='passou' else 1


if __name__=='__main__': raise SystemExit(main())
