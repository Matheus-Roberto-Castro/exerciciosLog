import argparse
import re
from datetime import datetime

PADRAO_BOOT = re.compile(
    r"^(?P<data_hora>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*kernel:\s*\[\s*0\.000000\]"
)
PADRAO_SHUTDOWN = re.compile(
    r"^(?P<data_hora>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*"
    r"(powering down|shutting down)",
    re.IGNORECASE,
)


def _para_datetime(data_hora_str: str) -> datetime:
    ano_atual = datetime.now().year
    return datetime.strptime(f"{ano_atual} {data_hora_str}", "%Y %b %d %H:%M:%S")


def calcular_periodos_atividade(caminho_log: str):
    boots = []
    shutdowns = []
    with open(caminho_log, "r", errors="ignore") as arquivo:
        for linha in arquivo:
            m_boot = PADRAO_BOOT.search(linha)
            if m_boot:
                boots.append(_para_datetime(m_boot.group("data_hora")))
                continue
            m_shutdown = PADRAO_SHUTDOWN.search(linha)
            if m_shutdown:
                shutdowns.append(_para_datetime(m_shutdown.group("data_hora")))

    periodos = []
    for boot in boots:
        # pega o primeiro shutdown que ocorreu depois deste boot
        candidatos = [s for s in shutdowns if s > boot]
        if candidatos:
            fim = min(candidatos)
            periodos.append((boot, fim, fim - boot))
    return periodos


def main():
    parser = argparse.ArgumentParser(
        description="Calcula o tempo de atividade entre boot e shutdown."
    )
    parser.add_argument("--log", default="/var/log/syslog")
    args = parser.parse_args()

    periodos = calcular_periodos_atividade(args.log)

    if not periodos:
        print("Não foi possível calcular o uptime: faltam pares boot/shutdown no log.")
        return

    print(f"{'Boot':<20} {'Shutdown':<20} {'Tempo ativo'}")
    print("-" * 60)
    for boot, fim, duracao in periodos:
        print(f"{boot:%Y-%m-%d %H:%M:%S}   {fim:%Y-%m-%d %H:%M:%S}   {duracao}")


if __name__ == "__main__":
    main()