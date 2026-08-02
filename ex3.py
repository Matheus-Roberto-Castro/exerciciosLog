import re
import argparse

PADRAO_SUDO = re.compile(
    r"^(?P<data>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*sudo:\s*"
    r"(?P<usuario>\S+)\s*:.*COMMAND=(?P<comando>.+)$"
)


def analisar(caminho_log):
    eventos = []
    with open(caminho_log, "r", errors="ignore") as f:
        for linha in f:
            m = PADRAO_SUDO.search(linha)
            if m:
                eventos.append((m.group("data"), m.group("usuario"), m.group("comando")))
    return eventos


def main():
    parser = argparse.ArgumentParser(description="Auditoria de uso do sudo")
    parser.add_argument("--log", default="/var/log/auth.log")
    args = parser.parse_args()

    eventos = analisar(args.log)

    print(f"{'DATA/HORA':<18}{'USUÁRIO':<12}{'COMANDO'}")
    print("-" * 60)
    for data, usuario, comando in eventos:
        print(f"{data:<18}{usuario:<12}{comando}")


if __name__ == "__main__":
    main()