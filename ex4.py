import re
import argparse

PADROES = [
    (
        "Usuário inexistente",
        re.compile(r"Invalid user (?P<usuario>\S+) from (?P<ip>\S+)"),
    ),
    (
        "Falta de permissão (sudoers)",
        re.compile(r"user (?P<usuario>\S+) is not in the sudoers file"),
    ),
    (
        "Falha de autenticação genérica (PAM)",
        re.compile(r"authentication failure;.*user=(?P<usuario>\S+)"),
    ),
    (
        "Conta bloqueada/expirada",
        re.compile(r"account (?P<usuario>\S+) has expired"),
    ),
]


def analisar(caminho_log):
    resultados = []
    with open(caminho_log, "r", errors="ignore") as f:
        for linha in f:
            for motivo, padrao in PADROES:
                m = padrao.search(linha)
                if m:
                    usuario = m.groupdict().get("usuario", "desconhecido")
                    resultados.append((motivo, usuario, linha.strip()))
                    break  # já classificou a linha, não precisa testar os demais padrões
    return resultados


def main():
    parser = argparse.ArgumentParser(
        description="Logins rejeitados por motivos diferentes de senha incorreta"
    )
    parser.add_argument("--log", default="/var/log/auth.log")
    args = parser.parse_args()

    resultados = analisar(args.log)

    print(f"{'MOTIVO':<32}{'USUÁRIO':<15}")
    print("-" * 60)
    for motivo, usuario, _linha in resultados:
        print(f"{motivo:<32}{usuario:<15}")


if __name__ == "__main__":
    main()