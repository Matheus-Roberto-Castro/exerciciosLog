import argparse
import re

PADRAO_DATA_HORA = re.compile(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}")

PALAVRAS_CHAVE = [
    ("REBOOT", re.compile(r"rebooting|reached target reboot", re.IGNORECASE)),
    (
        "SHUTDOWN",
        re.compile(
            r"powering down|shutting down|reached target shutdown|system halt",
            re.IGNORECASE,
        ),
    ),
]


def listar_eventos(caminho_log: str):
    eventos = []
    with open(caminho_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            for tipo, padrao in PALAVRAS_CHAVE:
                if padrao.search(linha):
                    data_hora_match = PADRAO_DATA_HORA.match(linha)
                    data_hora = data_hora_match.group(0) if data_hora_match else "?"
                    eventos.append((data_hora, tipo, linha.strip()))
                    break
    return eventos


def main():
    parser = argparse.ArgumentParser(
        description="Lista eventos de shutdown/reboot do sistema."
    )
    parser.add_argument("--log", default="/var/log/syslog")
    args = parser.parse_args()

    eventos = listar_eventos(args.log)

    if not eventos:
        print("Nenhum evento de shutdown/reboot encontrado no log.")
        return

    print(f"{'Data/Hora':<18} {'Tipo':<10} {'Linha original'}")
    print("-" * 80)
    for data_hora, tipo, linha in eventos:
        print(f"{data_hora:<18} {tipo:<10} {linha}")


if __name__ == "__main__":
    main()