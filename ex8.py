import argparse
import re

PADRAO_SERVICO = re.compile(
    r"^(?P<data_hora>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*"
    r"systemd\[1\]:\s+(?P<acao>Started|Stopped)\s+(?P<servico>.+?)\.?$"
)


def listar_servicos(caminho_log: str):
    eventos = []
    with open(caminho_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            match = PADRAO_SERVICO.search(linha)
            if match:
                eventos.append(
                    (
                        match.group("data_hora"),
                        match.group("acao").upper(),
                        match.group("servico"),
                    )
                )
    return eventos


def main():
    parser = argparse.ArgumentParser(
        description="Lista serviços iniciados/parados no sistema."
    )
    parser.add_argument("--log", default="/var/log/syslog")
    args = parser.parse_args()

    eventos = listar_servicos(args.log)

    if not eventos:
        print("Nenhuma alteração de status de serviço encontrada no log.")
        return

    print(f"{'Data/Hora':<18} {'Ação':<10} {'Serviço'}")
    print("-" * 60)
    for data_hora, acao, servico in eventos:
        print(f"{data_hora:<18} {acao:<10} {servico}")


if __name__ == "__main__":
    main()