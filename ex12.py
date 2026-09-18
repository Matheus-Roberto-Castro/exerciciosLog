import argparse
import re

PADRAO_REMOCAO = re.compile(
    r"^(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2}) "
    r"(?P<acao>remove|purge) (?P<pacote>\S+)"
)


def listar_removidos(caminho_log: str):
    removidos = []
    with open(caminho_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            match = PADRAO_REMOCAO.match(linha)
            if match:
                pacote = match.group("pacote").split(":")[0]
                removidos.append(
                    (
                        f"{match.group('data')} {match.group('hora')}",
                        match.group("acao"),
                        pacote,
                    )
                )
    return removidos


def main():
    parser = argparse.ArgumentParser(
        description="Lista pacotes removidos (remove/purge) do sistema."
    )
    parser.add_argument("--log", default="/var/log/dpkg.log")
    args = parser.parse_args()

    removidos = listar_removidos(args.log)

    if not removidos:
        print("Nenhum pacote removido encontrado no log.")
        return

    print(f"{'Data/Hora':<20} {'Ação':<8} {'Pacote'}")
    print("-" * 50)
    for data_hora, acao, pacote in removidos:
        print(f"{data_hora:<20} {acao:<8} {pacote}")


if __name__ == "__main__":
    main()