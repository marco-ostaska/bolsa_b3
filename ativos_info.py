from matplotlib.pyplot import tick_params
import bancoCentral
import fundamentusData
import investidor10
from tabulate import tabulate

def taxa_livre_risco():
    selic = bancoCentral.SELIC(5)
    ipca = bancoCentral.IPCA(5)

    if ipca.media_ganho_real() > selic.media_anual():
        return ipca.media_ganho_real()

    return selic.media_anual()


def get_tickers():
    tickers = input("Entre os tickers separados por virgula: ")
    return [t.upper().strip() for t in tickers.split(",")]


def get_tipo():
    tipo=None
    while tipo not in ["1","2","3"]:
        print("--------------------------------------------")
        print("1 - Ações")
        print("2 - FII")
        print("3 FI-INFRA")
        print("--------------------------------------------")
        tipo = input("Selecione uma opção:")

    return tipo

def process_acoes(ticker, free_risk):
    ativo = fundamentusData.Acao(ticker)
    df = [
        ["Cotação",f"R$ {ativo.cotacao}"],
        ["P/L", f"{ativo.pl}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Ghaham", f"R$ {ativo.graham}"],
        ["Bazin", f"R$ {ativo.bazin(free_risk)}"]

        ]

    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    desconto = round(((ativo.cotacao-ativo.graham)/ativo.graham)*100,2) if ativo.graham < 0 else round(((ativo.graham-ativo.cotacao)/ativo.graham)*100,2)

    return {
            'ticker': ativo.ticker,
            'desconto': desconto
        }


def process_fii(ticker, free_risk):
    ativo = fundamentusData.FII(ticker)
    df = [
        ["Cotação", f"R$ {ativo.cotacao}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Ghaham", f"R$ {ativo.graham}"],
        ["Bazin", f"R$ {ativo.bazin(free_risk)}"]

    ]
    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    return {
            'ticker': ativo.ticker,
            'desconto': round(1-ativo.pvp,2)
        }

def process_fi_infra(ticker, free_risk):
    ativo = investidor10.FI_INFRA(ticker)
    df = [
        ["Cotação", f"R$ {ativo.cotacao}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Ghaham", f"R$ {ativo.graham}"],
        ["Bazin", f"R$ {ativo.bazin(free_risk)}"]

    ]
    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    return {
            'ticker': ativo.ticker,
            'desconto': round(1-ativo.pvp,2)
        }


def main():
    tipo=get_tipo()
    tickers = get_tickers()
    risk_free = taxa_livre_risco()

    results = []
    for t in tickers:
        if tipo == "1":
            results.append(process_acoes(t, risk_free))
        elif tipo == "2":
            results.append(process_fii(t, risk_free))
        else:
            results.append(process_fi_infra(t, risk_free))


    print()
    print("----------------------------------------")
    print("Ordenados por desconto")
    print("----------------------------------------")
    
#   # Ordena os resultados pelo desconto Bazin
    sorted_results = sorted(results, key=lambda x: x['desconto'],reverse=True)

#     # Agora imprime os ativos ordenados
    for result in sorted_results:
        print(f"Ticker: {result['ticker']} | {result['desconto']}%")




if __name__ == "__main__":
    main()
