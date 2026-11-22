# RentSmart — Sistema de Orçamento de Locação

## Sobre o projeto

O RentSmart nasceu com a ideia de facilitar o cálculo de aluguel para quem está procurando um imóvel. Muitas vezes, ao escolher uma casa, apartamento ou estúdio, não pensamos apenas no valor do aluguel, mas também nos custos extras que podem aparecer durante a contratação.

Pensando nisso, desenvolvi este sistema em Python para ajudar a organizar esses valores e apresentar um orçamento mais claro, mostrando quanto será pago por mês e como ficará o planejamento financeiro ao longo de um ano.

## O que o RentSmart faz?

Com o programa, é possível escolher entre três tipos de imóveis:

- **Apartamento:** permite adicionar um segundo quarto e garagem, além de aplicar um desconto de acordo com a regra sobre crianças.
- **Casa:** permite escolher a quantidade de quartos e adicionar garagem.
- **Estúdio:** permite incluir vagas de estacionamento e calcular os valores adicionais.

Depois de escolher o imóvel, o sistema calcula o aluguel, os adicionais, os possíveis descontos e a taxa contratual de R$ 2.000,00, que pode ser dividida em até cinco parcelas.

No final, o usuário recebe um resumo do orçamento e o sistema gera um arquivo CSV com a previsão dos pagamentos durante 12 meses.

## Como o projeto foi desenvolvido?

O projeto foi desenvolvido utilizando Python e os conceitos de Programação Orientada a Objetos (POO).

Durante o desenvolvimento, foram criadas classes para representar os imóveis e organizar as responsabilidades de cada parte do sistema.

As principais classes são:

- **Imovel:** representa a estrutura básica de um imóvel.
- **Apartamento, Casa e Estudio:** possuem suas próprias características e regras de cálculo.
- **Orcamento:** organiza os valores e realiza os cálculos do orçamento.
- **GeradorCSV:** cria o arquivo com a previsão dos pagamentos.
- **SistemaRentSmart:** controla o funcionamento do programa e a interação com o usuário.

## Organização dos arquivos

```text
RentSmart/
│
├── src/
│   └── rentsmart.py
│
├── output/
│   └── projecao_rentsmart.csv
│
├── documentacao/
│   ├── fluxograma.png
│   └── RentSmart_Teoria.pdf
│
├── README.md
└── .gitignore
```

## Como executar?

Para utilizar o RentSmart, é necessário ter o Python instalado no computador.

1. Abra a pasta do projeto no Visual Studio Code.
2. Abra o terminal.
3. Execute o comando:

```bash
py src/rentsmart.py
```

4. Escolha o tipo de imóvel.
5. Responda às perguntas apresentadas pelo programa.
6. Confira o orçamento gerado.

O arquivo com a projeção financeira será salvo automaticamente na pasta `output`.

## O que aprendi com este projeto?

Desenvolver o RentSmart foi uma oportunidade de colocar em prática os conhecimentos de Python e Programação Orientada a Objetos.

Além de trabalhar com classes, objetos, herança e métodos, também foi possível entender melhor como organizar um programa, validar informações fornecidas pelo usuário e transformar regras de negócio em cálculos reais.

A proposta foi criar algo simples de utilizar, mas que demonstrasse como a programação pode ajudar a resolver situações do dia a dia.

---

**RentSmart — Mais organização e clareza na hora de planejar seu aluguel.**