
import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


# CONFIGURAÇÕES DO SISTEMA

TAXA_CONTRATUAL = Decimal("2000.00")
DESCONTO_APARTAMENTO = Decimal("0.05")
CENTAVOS = Decimal("0.01")


def formatar_moeda(valor):
    """Formata valores no padrão brasileiro."""
    valor = Decimal(valor).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def validar_opcao(mensagem, opcoes):
    """Solicita uma opção até que o usuário informe uma válida."""
    while True:
        opcao = input(mensagem).strip()

        if opcao in opcoes:
            return opcao

        print("Opção inválida. Tente novamente.")


def validar_inteiro(mensagem, minimo, maximo=None):
    """Valida números inteiros dentro de um intervalo."""
    while True:
        try:
            numero = int(input(mensagem))

            if numero < minimo:
                print(f"Informe um número maior ou igual a {minimo}.")
                continue

            if maximo is not None and numero > maximo:
                print(f"Informe um número menor ou igual a {maximo}.")
                continue

            return numero

        except ValueError:
            print("Digite apenas números inteiros.")


# CLASSE BASE: IMÓVEL


class Imovel:
    def __init__(self, nome, aluguel_base):
        self.nome = nome
        self.aluguel_base = Decimal(aluguel_base)
        self.adicionais = {}

    def adicionar_custo(self, descricao, valor):
        """Registra um adicional no orçamento."""
        self.adicionais[descricao] = Decimal(valor)

    def calcular_adicionais(self):
        """Soma todos os adicionais."""
        return sum(self.adicionais.values(), Decimal("0.00"))

    def calcular_aluguel(self):
        """Calcula o aluguel antes de descontos."""
        return self.aluguel_base + self.calcular_adicionais()

    def calcular_desconto(self):
        """Por padrão, não existe desconto."""
        return Decimal("0.00")


# CLASSE: APARTAMENTO


class Apartamento(Imovel):
    def __init__(self, quartos, possui_criancas, garagem):
        super().__init__("Apartamento", "700.00")

        self.quartos = quartos
        self.possui_criancas = possui_criancas
        self.garagem = garagem

        if self.quartos == 2:
            self.adicionar_custo("Adicional de segundo quarto", "200.00")

        if self.garagem:
            self.adicionar_custo("Vaga de garagem", "300.00")

    def calcular_desconto(self):
        if not self.possui_criancas:
            return (
                self.calcular_aluguel()
                * DESCONTO_APARTAMENTO
            ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

        return Decimal("0.00")


# CLASSE: CASA


class Casa(Imovel):
    def __init__(self, quartos, garagem):
        super().__init__("Casa", "900.00")

        self.quartos = quartos
        self.garagem = garagem

        if self.quartos == 2:
            self.adicionar_custo("Adicional de segundo quarto", "250.00")

        if self.garagem:
            self.adicionar_custo("Vaga de garagem", "300.00")


# CLASSE: ESTÚDIO


class Estudio(Imovel):
    def __init__(self, quantidade_vagas):
        super().__init__("Estúdio", "1200.00")

        self.quantidade_vagas = quantidade_vagas

        if self.quantidade_vagas >= 2:
            self.adicionar_custo("Pacote inicial de 2 vagas", "250.00")

            vagas_adicionais = self.quantidade_vagas - 2

            if vagas_adicionais > 0:
                valor_adicional = Decimal(vagas_adicionais) * Decimal("60.00")

                self.adicionar_custo(
                    f"{vagas_adicionais} vaga(s) adicional(is)",
                    valor_adicional
                )


# CLASSE: ORÇAMENTO


class Orcamento:
    def __init__(self, imovel, parcelas_contrato):
        self.imovel = imovel
        self.parcelas_contrato = parcelas_contrato

        self.valor_bruto = imovel.calcular_aluguel()
        self.desconto = imovel.calcular_desconto()

        self.valor_mensal = (
            self.valor_bruto - self.desconto
        ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

        self.valor_taxa = TAXA_CONTRATUAL

    def calcular_valor_parcela(self):
        return (
            self.valor_taxa / self.parcelas_contrato
        ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    def calcular_parcelas(self):
        """Calcula as parcelas, ajustando os centavos na última."""
        valor_parcela = self.calcular_valor_parcela()

        parcelas = [
            valor_parcela
            for _ in range(self.parcelas_contrato)
        ]

        soma_anterior = sum(parcelas[:-1], Decimal("0.00"))

        parcelas[-1] = self.valor_taxa - soma_anterior

        return parcelas

    def exibir_resumo(self):
        print("\n" + "=" * 48)
        print("             RESUMO DO ORÇAMENTO")
        print("=" * 48)

        print(f"\nImóvel: {self.imovel.nome}")
        print(f"Aluguel base: {formatar_moeda(self.imovel.aluguel_base)}")

        print("\n--- Adicionais ---")

        if self.imovel.adicionais:
            for descricao, valor in self.imovel.adicionais.items():
                print(f"{descricao}: {formatar_moeda(valor)}")
        else:
            print("Nenhum adicional.")

        print("\n--- Cálculo do aluguel ---")

        print(f"Valor antes do desconto: {formatar_moeda(self.valor_bruto)}")
        print(f"Desconto: -{formatar_moeda(self.desconto)}")

        print("-" * 48)
        print(f"ALUGUEL MENSAL: {formatar_moeda(self.valor_mensal)}")

        print("\n--- Taxa contratual ---")

        print(f"Valor total: {formatar_moeda(self.valor_taxa)}")
        print(f"Quantidade de parcelas: {self.parcelas_contrato}")

        for numero, valor in enumerate(self.calcular_parcelas(), start=1):
            print(f"Parcela {numero}: {formatar_moeda(valor)}")

        print("=" * 48)

        print(
            "\nO valor do aluguel e a taxa contratual "
            "são cobrados separadamente."
        )


# CLASSE: GERADOR DE CSV


class GeradorCSV:
    def __init__(self, orcamento):
        self.orcamento = orcamento

    def gerar_projecao(self):
        """Gera um arquivo CSV com os 12 meses da locação."""

        parcelas = self.orcamento.calcular_parcelas()

        caminho = Path(__file__).resolve().parent.parent / "output" / "projecao_rentsmart.csv"

        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:

            escritor = csv.writer(arquivo, delimiter=";")

            escritor.writerow([
                "Mês",
                "Aluguel mensal",
                "Parcela da taxa contratual",
                "Total previsto"
            ])

            for mes in range(1, 13):

                if mes <= len(parcelas):
                    parcela_contrato = parcelas[mes - 1]
                else:
                    parcela_contrato = Decimal("0.00")

                total_mes = (
                    self.orcamento.valor_mensal
                    + parcela_contrato
                )

                escritor.writerow([
                    mes,
                    format(self.orcamento.valor_mensal, ".2f"),
                    format(parcela_contrato, ".2f"),
                    format(total_mes, ".2f")
                ])

        print("\nArquivo CSV gerado com sucesso!")
        print(f"Local: {caminho.resolve()}")



# CLASSE PRINCIPAL: SISTEMA RENTSMART


class SistemaRentSmart:

    def solicitar_imovel(self):
        print("\n" + "=" * 48)
        print("              RENTSMART")
        print("       SISTEMA DE ORÇAMENTO DE LOCAÇÃO")
        print("=" * 48)

        print("\nEscolha o tipo de imóvel:")
        print("1 - Apartamento")
        print("2 - Casa")
        print("3 - Estúdio")

        opcao = validar_opcao(
            "\nDigite sua opção: ",
            ["1", "2", "3"]
        )

        if opcao == "1":
            return self.criar_apartamento()

        elif opcao == "2":
            return self.criar_casa()

        else:
            return self.criar_estudio()

    def criar_apartamento(self):
        print("\n--- APARTAMENTO ---")

        quartos = validar_inteiro(
            "Quantidade de quartos (1 ou 2): ",
            1,
            2
        )

        criancas = validar_opcao(
            "Possui crianças? (S/N): ",
            ["S", "N", "s", "n"]
        ).upper()

        possui_criancas = criancas == "S"

        garagem = validar_opcao(
            "Deseja vaga de garagem? (S/N): ",
            ["S", "N", "s", "n"]
        ).upper() == "S"

        return Apartamento(quartos, possui_criancas, garagem)

    def criar_casa(self):
        print("\n--- CASA ---")

        quartos = validar_inteiro(
            "Quantidade de quartos (1 ou 2): ",
            1,
            2
        )

        garagem = validar_opcao(
            "Deseja vaga de garagem? (S/N): ",
            ["S", "N", "s", "n"]
        ).upper() == "S"

        return Casa(quartos, garagem)

    def criar_estudio(self):
        print("\n--- ESTÚDIO ---")

        print("O pacote inicial de estacionamento inclui 2 vagas.")
        print("Informe 0 para não contratar estacionamento.")
        print("Para contratar, informe 2 ou mais vagas.")

        vagas = validar_opcao(
            "Deseja estacionamento? (S/N): ",
            ["S", "N", "s", "n"]
        ).upper()

        if vagas == "S":
            quantidade_vagas = validar_inteiro(
                "Quantidade de vagas (mínimo 2): ",
                2
            )
        else:
            quantidade_vagas = 0

        return Estudio(quantidade_vagas)

    def executar(self):
        """Controla a execução completa do sistema."""

        imovel = self.solicitar_imovel()

        print("\n--- CONTRATO ---")

        parcelas = validar_inteiro(
            "Em quantas parcelas deseja pagar a taxa contratual (1 a 5)? ",
            1,
            5
        )

        orcamento = Orcamento(imovel, parcelas)

        orcamento.exibir_resumo()

        gerador = GeradorCSV(orcamento)
        gerador.gerar_projecao()



# EXECUÇÃO DO PROGRAMA


if __name__ == "__main__":

    sistema = SistemaRentSmart()
    sistema.executar()
