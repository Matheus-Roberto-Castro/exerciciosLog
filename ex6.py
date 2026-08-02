import re
import argparse
import subprocess


def data_boot_via_who():
    try:
        saida = subprocess.check_output(["who", "-b"], text=True, errors="ignore")
        # saída típica: "         system boot  2026-09-01 08:12"
        m = re.search(r"system boot\s+(?P<data>.+)", saida)
        if m:
            return m.group("data").strip()
    except Exception:
        pass
    return None


def data_boot_via_syslog(caminho_log):
    padrao = re.compile(r"^(?P<data>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*kernel: \[\s*0\.")
    try:
        with open(caminho_log, "r", errors="ignore") as f:
            for linha in f:
                m = padrao.search(linha)
                if m:
                    return m.group("data")
    except FileNotFoundError:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Mostra a data/hora do último boot")
    parser.add_argument("--log", default="/var/log/syslog")
    args = parser.parse_args()

    resultado = data_boot_via_who()
    fonte = "who -b"

    if not resultado:
        resultado = data_boot_via_syslog(args.log)
        fonte = args.log

    if resultado:
        print(f"Último boot: {resultado} (fonte: {fonte})")
    else:
        print("Não foi possível determinar a data do último boot.")


if __name__ == "__main__":
    main()