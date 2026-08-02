import re
import argparse

PADRAO_SUCESSO = re.compile(
    r"^(?P<data>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*"
    r"Accepted (?P<metodo>\w+) for (?P<usuario>\S+) from (?P<ip>\S+)"
)


def analisar(caminho_log):
    resultados = []
    with open(caminho_log, "r", errors="ignore") as f:
        for linha in f:
            m = PADRAO_SUCESSO.search(linha)
            if m:
                resultados.append(
                    (m.group("data"), m.group("usuario"), m.group("metodo"), m.group("ip"))
                )
    return resultados


def main():
    parser = argparse.ArgumentParser(description="Relatório de logins bem-sucedidos")
    parser.add_argument("--log", default="/var/log/auth.log")
    args = parser.parse_args()

    resultados = analisar(args.log)

    print(f"{'DATA/HORA':<18}{'USUÁRIO':<15}{'MÉTODO':<12}{'IP ORIGEM'}")
    print("-" * 60)
    for data, usuario, metodo, ip in resultados:
        print(f"{data:<18}{usuario:<15}{metodo:<12}{ip}")


if __name__ == "__main__":
    main()