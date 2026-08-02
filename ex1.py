import re
import argparse
from collections import Counter

PADRAO_FALHA = re.compile(
    r"Failed password for (?:invalid user )?(?P<usuario>\S+) from (?P<ip>\S+)"
)


def analisar(caminho_log):
    contagem = Counter()

    with open(caminho_log, "r", errors="ignore") as f:
        for linha in f:
            m = PADRAO_FALHA.search(linha)
            if m:
                usuario = m.group("usuario")
                contagem[usuario] += 1

    return contagem


def main():
    parser = argparse.ArgumentParser(
        description="Lista usuários com tentativas de login com senha incorreta"
    )
    parser.add_argument(
        "--log", default="/var/log/auth.log", help="Caminho do arquivo de log"
    )
    args = parser.parse_args()

    contagem = analisar(args.log)

    print(f"{'USUÁRIO':<25}{'TENTATIVAS FALHAS'}")
    print("-" * 45)
    for usuario, total in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
        print(f"{usuario:<25}{total}")


if __name__ == "__main__":
    main()