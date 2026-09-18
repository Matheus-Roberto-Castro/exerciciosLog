import argparse
import re

PADRAO_SUDO_PACOTES = re.compile(
    r"^(?P<data_hora>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*"
    r"sudo:\s+(?P<usuario>\S+)\s*:.*COMMAND=(?P<comando>.*(?:apt-get|apt|dpkg).*)$"
)

PADRAO_ACAO_DPKG = re.compile(
    r"^(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2}) "
    r"(?P<acao>install|remove|purge|upgrade) (?P<pacote>\S+)"
)


def quem_executou(caminho_auth_log: str):
    eventos = []
    with open(caminho_auth_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            match = PADRAO_SUDO_PACOTES.search(linha)
            if match:
                eventos.append(
                    (
                        match.group("data_hora"),
                        match.group("usuario"),
                        match.group("comando").strip(),
                    )
                )
    return eventos


def o_que_foi_feito(caminho_dpkg_log: str):
    eventos = []
    with open(caminho_dpkg_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            match = PADRAO_ACAO_DPKG.match(linha)
            if match:
                eventos.append(
                    (
                        f"{match.group('data')} {match.group('hora')}",
                        match.group("acao"),
                        match.group("pacote").split(":")[0],
                    )
                )
    return eventos


def main():
    parser = argparse.ArgumentParser(
        description="Rastreia uso de apt/apt-get/dpkg (usuário + ação realizada)."
    )
    parser.add_argument("--auth-log", default="/var/log/auth.log")
    parser.add_argument("--dpkg-log", default="/var/log/dpkg.log")
    args = parser.parse_args()

    print("== Quem executou comandos de gerenciamento de pacotes (auth.log) ==")
    execucoes = quem_executou(args.auth_log)
    if execucoes:
        print(f"{'Data/Hora':<18} {'Usuário':<12} {'Comando'}")
        print("-" * 60)
        for data_hora, usuario, comando in execucoes:
            print(f"{data_hora:<18} {usuario:<12} {comando}")
    else:
        print("Nenhuma execução de sudo com apt/apt-get/dpkg encontrada.")

    print()
    print("== Ações registradas pelo dpkg (dpkg.log) ==")
    acoes = o_que_foi_feito(args.dpkg_log)
    if acoes:
        print(f"{'Data/Hora':<20} {'Ação':<10} {'Pacote'}")
        print("-" * 55)
        for data_hora, acao, pacote in acoes:
            print(f"{data_hora:<20} {acao:<10} {pacote}")
    else:
        print("Nenhuma ação de pacote encontrada no dpkg.log.")


if __name__ == "__main__":
    main()