import argparse
import re
from datetime import datetime, timedelta

PADRAO_INSTALL = re.compile(
    r"^(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2}) install (?P<pacote>\S+)"
)


def listar_instalados_ultima_semana(caminho_log: str, dias: int = 7):
    limite = datetime.now() - timedelta(days=dias)
    instalados = []
    with open(caminho_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            match = PADRAO_INSTALL.match(linha)
            if not match:
                continue
            data_hora = datetime.strptime(
                f"{match.group('data')} {match.group('hora')}", "%Y-%m-%d %H:%M:%S"
            )
            if data_hora >= limite:
                # remove a arquitetura (ex: ":amd64") do nome do pacote
                pacote = match.group("pacote").split(":")[0]
                instalados.append((data_hora, pacote))
    return instalados


def main():
    parser = argparse.ArgumentParser(
        description="Lista pacotes instalados nos últimos N dias (padrão 7)."
    )
    parser.add_argument("--log", default="/var/log/dpkg.log")
    parser.add_argument("--dias", type=int, default=7)
    args = parser.parse_args()

    instalados = listar_instalados_ultima_semana(args.log, args.dias)

    if not instalados:
        print(f"Nenhum pacote instalado nos últimos {args.dias} dias.")
        return

    print(f"{'Data/Hora':<20} {'Pacote'}")
    print("-" * 45)
    for data_hora, pacote in sorted(instalados):
        print(f"{data_hora:%Y-%m-%d %H:%M:%S}   {pacote}")


if __name__ == "__main__":
    main()