"""Programação de dezembro/2026 (escrita pelo Claude com a skill marketing-juridico).

Pauta aprovada pela Dra. Dirciléia em 25/11/2026. Reels com 2 telas (meta de 20 a 25 s).
04/12: ITBI no lugar do programa municipal (não há texto oficial da lei local).
Já prontos em conteudo/datas_comemorativas_2026.py: 03, 08, 21 e 25/12.

Fontes conferidas em 25/11/2026 no planalto.gov.br (Código Civil, CTN com a LC 227/2026,
Leis 6.015/1973, 8.245/1991, 8.934/1994 e 13.097/2015, EC 103/2019, LC 214/2025,
Decreto 3.048/1999 e CPC), no atos.cnj.jus.br (Resolução 35/2007) e no andamento oficial
do RE 1.495.108 no portal do STF (Tema 1.348).

Execute com:  python -m conteudo.programacao_2026_12
Grava os JSON em posts/fila/ (nada vai ao GitHub sem a aprovação da Dra. Dirciléia).
"""
import json

from agente.config import PASTA_FILA

CONFERIDO = "conferido em 25/11/2026"
TAGS_FIXAS = ["#saobernardodocampo", "#abcpaulista", "#advocacia"]
F = "assets/fotos/escolhidas/pexels-{}.jpg".format
V = "assets/videos/pexels-{}.mp4".format
TRILHA = "assets/audio/pixabay-{}.mp3".format

POSTS = [
    # ------------------------------------------------------------------ 02/12
    {
        "id": "2026-12-02_checklist-antes-de-comprar",
        "data_publicacao": "2026-12-02", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Vai comprar um imóvel? Faça este *checklist*",
        "subtitulo": "5 pontos para conferir antes de assinar.",
        "foto": F("34992176"),
        "slides": [
            {"titulo": "Matrícula atualizada",
             "texto": "A certidão de inteiro teor mostra o dono, os ônus e as restrições do imóvel "
                      "(Lei 6.015/1973, art. 19, § 11)."},
            {"titulo": "Estado civil de quem vende",
             "texto": "Em regra, a pessoa casada precisa da autorização do cônjuge para vender, exceto na "
                      "separação absoluta de bens (Código Civil, art. 1.647, I)."},
            {"titulo": "Dívidas de condomínio",
             "texto": "Quem compra responde pelos débitos do vendedor com o condomínio, inclusive multas e "
                      "juros (Código Civil, art. 1.345)."},
            {"titulo": "IPTU e taxas",
             "texto": "Os tributos do imóvel passam para quem compra, salvo quando a prova de quitação consta "
                      "do título (CTN, art. 130)."},
            {"titulo": "Escritura e registro",
             "texto": "Pagar e assinar não basta. A propriedade só se transfere com o registro no Cartório de "
                      "Registro de Imóveis (Código Civil, art. 1.245)."},
        ],
        "chamada_final": "Qual destes pontos você não conferia?",
        "legenda": "Comprar um imóvel é, para muita gente, o maior negócio da vida. Antes de assinar, "
                   "confira:\n\n1. Matrícula atualizada, com o dono, os ônus e as restrições do imóvel.\n2. "
                   "Estado civil de quem vende: em regra, o cônjuge precisa autorizar a venda, exceto na "
                   "separação absoluta de bens.\n3. Condomínio: quem compra responde pelos débitos do "
                   "vendedor, inclusive multas e juros.\n4. IPTU e taxas: passam para quem compra, salvo "
                   "quando a prova de quitação consta do título.\n5. Escritura e registro: a propriedade só se "
                   "transfere com o registro.\n\nCada negócio pode exigir outras verificações.\n\nSalve este "
                   "checklist. Qual destes pontos você não conferia?",
        "hashtags": ["#compradeimovel", "#matricula", "#direitoimobiliario", "#regularizacaodeimoveis"] + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, art. 19, § 11 ({CONFERIDO})",
                   f"Código Civil, arts. 1.245, 1.345 e 1.647, I ({CONFERIDO})", f"CTN, art. 130 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 04/12
    {
        "id": "2026-12-04_itbi-valor-de-mercado",
        "data_publicacao": "2026-12-04", "formato": "carrossel", "area": "Direito Tributário",
        "titulo": "ITBI: o que mudou na *base de cálculo*",
        "subtitulo": "As novas regras do Código Tributário Nacional.",
        "foto": F("34855832"), "escurecer": 0.6,
        "slides": [
            {"titulo": "O que é o ITBI",
             "texto": "É o imposto municipal sobre a transmissão onerosa de imóveis entre vivos, como a compra "
                      "e venda (Constituição, art. 156, II)."},
            {"titulo": "O novo valor venal",
             "texto": "Desde janeiro de 2026, o CTN define valor venal como o valor à vista do imóvel, em "
                      "condições normais de mercado (art. 38, § 1º)."},
            {"titulo": "Critérios técnicos",
             "texto": "A estimativa deve usar critérios técnicos, como preços de mercado, dados de cartórios e "
                      "características do imóvel (art. 38, § 2º)."},
            {"titulo": "Transparência",
             "texto": "O município deve divulgar os critérios que usou para estimar o valor (art. 38, § 3º)."},
            {"titulo": "É possível contestar",
             "texto": "O contribuinte pode contestar a estimativa com avaliação contraditória, na forma da lei "
                      "municipal (art. 38, § 3º)."},
        ],
        "chamada_final": "Você sabia que o valor do ITBI pode ser contestado?",
        "legenda": "A Lei Complementar 227, de 13 de janeiro de 2026, mudou as regras do ITBI no Código "
                   "Tributário Nacional.\n\n1. A base de cálculo continua sendo o valor venal, que agora é "
                   "definido como o valor pelo qual o imóvel seria negociado à vista, em condições normais de "
                   "mercado.\n2. Esse valor deve ser estimado por critérios técnicos, como a análise de preços "
                   "do mercado, as informações de cartórios e as características do imóvel.\n3. O município "
                   "deve divulgar os critérios usados.\n4. O contribuinte pode contestar a estimativa com "
                   "avaliação contraditória, em procedimento próprio, conforme a lei municipal.\n\nVocê sabia "
                   "que o valor do ITBI pode ser contestado? Conte nos comentários.",
        "hashtags": ["#itbi", "#direitotributario", "#compradeimovel", "#imposto"] + TAGS_FIXAS,
        "fontes": [f"CTN, art. 38, com a redação da LC 227/2026 ({CONFERIDO})",
                   f"LC 227/2026, arts. 165 e 182 ({CONFERIDO})", f"Constituição, art. 156, II ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 07/12
    {
        "id": "2026-12-07_reel-usucapiao-familiar",
        "data_publicacao": "2026-12-07", "formato": "reel", "area": "Direito Imobiliário",
        "titulo": "2 anos para a *usucapião familiar*",
        "subtitulo": "Quando o ex abandona o lar",
        "video_capa": V("6381010"), "video_final": V("7292491"),
        "trilha": TRILHA("590331-inspiring-emotional"),
        "slides": [
            {"titulo": "O imóvel",
             "texto": "Urbano, de até 250 m², dividido com o ex que abandonou o lar.",
             "video": V("8502728")},
            {"titulo": "A posse",
             "texto": "2 anos de moradia exclusiva, sem oposição e sem outro imóvel.",
             "video": V("7986204")},
        ],
        "chamada_final": "Você conhecia essa regra?",
        "legenda": "Existe uma modalidade de usucapião com prazo de apenas 2 anos: a usucapião familiar "
                   "(Código Civil, art. 1.240-A).\n\nEla pode beneficiar quem:\n\n1. Divide a propriedade de um "
                   "imóvel urbano de até 250 m² com ex-cônjuge ou ex-companheiro que abandonou o lar.\n2. "
                   "Exerce, por 2 anos ininterruptos e sem oposição, a posse direta e exclusiva do imóvel, "
                   "usando-o como sua moradia ou de sua família.\n3. Não é proprietário de outro imóvel urbano "
                   "ou rural.\n\nCumpridos os requisitos, a pessoa adquire o domínio integral. O direito só "
                   "pode ser reconhecido uma vez ao mesmo possuidor.\n\nO abandono do lar precisa ser "
                   "analisado em cada caso.\n\nVocê conhecia essa regra? Conte nos comentários.",
        "hashtags": ["#usucapiaofamiliar", "#usucapiao", "#direitoimobiliario", "#divorcio"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, art. 1.240-A e § 1º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 09/12
    {
        "id": "2026-12-09_reel-ponto-comercial",
        "data_publicacao": "2026-12-09", "formato": "reel", "area": "Direito Empresarial",
        "titulo": "Seu *ponto comercial* pode ser protegido",
        "subtitulo": "Conheça a ação renovatória",
        "video_capa": V("8024269"), "video_final": V("8195368"),
        "trilha": TRILHA("576594-upbeat-corporate"),
        "slides": [
            {"titulo": "Requisitos",
             "texto": "Contrato escrito, 5 anos de locação e 3 no mesmo ramo.",
             "video": V("7735908")},
            {"titulo": "Prazo",
             "texto": "Entre 1 ano e 6 meses antes do fim do contrato.",
             "video": V("13511897")},
        ],
        "chamada_final": "Quando vence o seu contrato?",
        "legenda": "Quem aluga um imóvel para o seu comércio pode ter direito à renovação do contrato, por "
                   "igual prazo. É a chamada ação renovatória (Lei 8.245/1991, art. 51).\n\nOs requisitos são "
                   "cumulativos:\n\n1. Contrato escrito e com prazo determinado.\n2. Prazo mínimo de 5 anos, "
                   "em um contrato ou na soma de contratos escritos e ininterruptos.\n3. Exploração do mesmo "
                   "ramo por pelo menos 3 anos ininterruptos.\n\nAtenção ao prazo: a ação deve ser proposta "
                   "entre 1 ano e 6 meses antes do fim do contrato em vigor. Depois disso, o direito se perde "
                   "(art. 51, § 5º). A lei também prevê casos em que o locador não é obrigado a renovar (art. "
                   "52).\n\nQuando vence o seu contrato? Salve para não esquecer.",
        "hashtags": ["#pontocomercial", "#acaorenovatoria", "#locacaocomercial", "#direitoempresarial"] + TAGS_FIXAS,
        "fontes": [f"Lei 8.245/1991, arts. 51 e 52 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 11/12
    {
        "id": "2026-12-11_aposentadoria-2027",
        "data_publicacao": "2026-12-11", "formato": "carrossel", "area": "Direito Previdenciário",
        "titulo": "Aposentadoria em 2027: o que *muda*",
        "subtitulo": "As regras de transição sobem em janeiro.",
        "foto": F("6626087"),
        "slides": [
            {"titulo": "Para quem valem",
             "texto": "Para quem já era filiado ao INSS quando a Reforma da Previdência entrou em vigor, em "
                      "novembro de 2019 (EC 103/2019)."},
            {"titulo": "Regra dos pontos",
             "texto": "Em 2027: 94 pontos para a mulher e 104 para o homem, com 30 e 35 anos de contribuição "
                      "(art. 15)."},
            {"titulo": "Como somar os pontos",
             "texto": "Some a idade e o tempo de contribuição. Exemplo: 62 anos de idade e 32 de contribuição "
                      "dão 94 pontos."},
            {"titulo": "Idade progressiva",
             "texto": "Em 2027: 60 anos para a mulher e 65 para o homem, com 30 e 35 anos de contribuição "
                      "(art. 16)."},
            {"titulo": "Há outras regras",
             "texto": "Existem ainda a regra por idade e as de pedágio. A mais adequada depende do histórico de "
                      "cada pessoa (arts. 17, 18 e 20)."},
        ],
        "chamada_final": "Você sabe em qual regra se encaixa?",
        "legenda": "Em janeiro, duas regras de transição da aposentadoria ficam mais exigentes. Elas valem para "
                   "quem já era filiado ao INSS quando a Reforma da Previdência entrou em vigor, em novembro "
                   "de 2019.\n\n1. Regra dos pontos (EC 103/2019, art. 15): em 2027, 94 pontos para a mulher, "
                   "com 30 anos de contribuição, e 104 para o homem, com 35 anos. Os pontos são a soma da "
                   "idade com o tempo de contribuição.\n2. Idade progressiva (art. 16): em 2027, 60 anos para "
                   "a mulher, com 30 de contribuição, e 65 para o homem, com 35.\n\nHá ainda a regra por idade "
                   "(art. 18) e as de pedágio (arts. 17 e 20). Para professores, essas duas regras têm "
                   "requisitos reduzidos.\n\nVocê sabe em qual regra se encaixa? Salve este post e confira o "
                   "seu tempo de contribuição.",
        "hashtags": ["#aposentadoria", "#inss", "#regrasdetransicao", "#direitoprevidenciario"] + TAGS_FIXAS,
        "fontes": [f"EC 103/2019, arts. 15, 16, 17, 18, 20 e 36 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 14/12
    {
        "id": "2026-12-14_reel-construiu-terreno-dos-pais",
        "data_publicacao": "2026-12-14", "formato": "reel", "area": "Direito Imobiliário",
        "titulo": "Construiu no terreno dos *pais*?",
        "subtitulo": "Veja o que diz a lei",
        "video_capa": V("8965542"), "video_final": V("8187790"),
        "trilha": TRILHA("409347-inspiring-cinematic"),
        "slides": [
            {"titulo": "De quem é a casa?",
             "texto": "A lei presume que a construção é do dono do terreno.",
             "video": V("8487246")},
            {"titulo": "E quem construiu?",
             "texto": "De boa-fé, em regra, perde a obra, mas tem direito a indenização.",
             "video": V("8057838")},
        ],
        "chamada_final": "Combine antes e coloque no papel.",
        "legenda": "É comum no Brasil: o filho constrói a própria casa no terreno dos pais. Mas a quem ela "
                   "pertence?\n\n1. A lei presume que a construção foi feita pelo dono do terreno e à custa "
                   "dele, até que se prove o contrário (Código Civil, art. 1.253).\n2. Em regra, quem constrói "
                   "em terreno alheio perde a construção para o proprietário. Se agiu de boa-fé, tem direito a "
                   "indenização (art. 1.255).\n3. Se a construção, feita de boa-fé, exceder consideravelmente "
                   "o valor do terreno, quem construiu pode adquirir a propriedade do solo, pagando a "
                   "indenização fixada judicialmente, se não houver acordo (art. 1.255, parágrafo único).\n\n"
                   "Guardar notas e recibos e colocar o combinado no papel ajuda a evitar conflitos, "
                   "inclusive na herança.\n\nVocê conhece alguém nessa situação? Compartilhe.",
        "hashtags": ["#construcao", "#direitoimobiliario", "#regularizacaodeimoveis", "#heranca"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1.253 e 1.255 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 16/12
    {
        "id": "2026-12-16_direito-de-laje",
        "data_publicacao": "2026-12-16", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Mora na *laje*? Ela pode ter matrícula própria",
        "subtitulo": "Conheça o direito real de laje.",
        "foto": F("34640157"), "escurecer": 0.45,
        "slides": [
            {"titulo": "O que é",
             "texto": "O dono da construção-base pode ceder a parte de cima ou de baixo para que outra pessoa "
                      "tenha ali uma unidade distinta (Código Civil, art. 1.510-A)."},
            {"titulo": "Matrícula própria",
             "texto": "A laje é registrada com a abertura de matrícula própria e averbação na matrícula da "
                      "construção-base (Lei 6.015/1973, art. 176, § 9º)."},
            {"titulo": "O que o titular pode fazer",
             "texto": "Com a matrícula, o titular pode usar, gozar e dispor da sua unidade, inclusive vendê-la "
                      "(art. 1.510-A, § 3º)."},
            {"titulo": "O terreno não entra",
             "texto": "A laje não dá ao titular uma fração do terreno nem participação nas áreas já edificadas "
                      "(art. 1.510-A, § 4º)."},
            {"titulo": "Deveres e limites",
             "texto": "O titular paga os tributos da sua unidade e deve respeitar as regras do município "
                      "(art. 1.510-A, §§ 2º e 5º)."},
        ],
        "chamada_final": "Você sabia que a laje pode ser registrada?",
        "legenda": "Filhos que constroem em cima da casa dos pais, uma casa sobre a outra no mesmo terreno: essa "
                   "realidade tem previsão em lei. É o direito real de laje, criado pela Lei 13.465/2017.\n\n1. "
                   "O dono da construção-base pode ceder a superfície superior ou inferior para que outra "
                   "pessoa mantenha ali uma unidade distinta.\n2. A laje ganha matrícula própria no Registro "
                   "de Imóveis.\n3. O titular pode usar, gozar e dispor da sua unidade.\n4. A laje não dá "
                   "direito a fração do terreno.\n5. O titular responde pelos encargos e tributos da sua "
                   "unidade e deve respeitar as posturas do município.\n\nCada situação exige análise dos "
                   "documentos e da construção.\n\nVocê sabia que a laje pode ser registrada? Conte nos "
                   "comentários.",
        "hashtags": ["#direitodelaje", "#laje", "#regularizacaodeimoveis", "#registrodeimoveis"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, art. 1.510-A, com a Lei 13.465/2017 ({CONFERIDO})",
                   f"Lei 6.015/1973, art. 176, § 9º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 18/12
    {
        "id": "2026-12-18_reel-aluguel-reforma-tributaria",
        "data_publicacao": "2026-12-18", "formato": "reel", "area": "Direito Tributário",
        "titulo": "Reforma tributária: e o seu *aluguel*?",
        "subtitulo": "Para pessoas físicas que alugam",
        "video_capa": V("7646762"), "video_final": V("7817154"),
        "trilha": TRILHA("595943-upbeat-corporate"),
        "slides": [
            {"titulo": "Quem entra na regra",
             "texto": "Receita acima de R$ 240 mil por ano e mais de 3 imóveis.",
             "video": V("6794390")},
            {"titulo": "Os dois juntos",
             "texto": "Em regra, é preciso cumprir os dois requisitos no ano anterior.",
             "video": V("7646797")},
        ],
        "chamada_final": "Você tem imóveis alugados?",
        "legenda": "A reforma tributária criou o IBS e a CBS. Mas nem toda pessoa física que aluga imóvel será "
                   "contribuinte desses tributos.\n\nNa locação, a pessoa física entra no regime regular quando, "
                   "no ano anterior, cumprir os dois requisitos (LC 214/2025, art. 251, § 1º, I):\n\n1. "
                   "Receita total com locação acima de R$ 240 mil, valor atualizado pelo IPCA (§ 5º).\n2. "
                   "Locação de mais de 3 imóveis distintos.\n\nA lei também prevê o enquadramento no próprio "
                   "ano, quando o valor exceder esse limite em 20% (§ 2º, II).\n\nO imposto de renda sobre o "
                   "aluguel tem regras próprias e não se confunde com esses tributos.\n\nVocê tem imóveis "
                   "alugados? Compartilhe com quem precisa saber.",
        "hashtags": ["#reformatributaria", "#aluguel", "#ibs", "#direitotributario"] + TAGS_FIXAS,
        "fontes": [f"LC 214/2025, art. 251, §§ 1º, 2º e 5º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 23/12
    {
        "id": "2026-12-23_vender-imovel-de-heranca",
        "data_publicacao": "2026-12-23", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Dá para vender um imóvel de *herança*?",
        "subtitulo": "O que a lei permite antes da partilha.",
        "foto": F("17790673"),
        "slides": [
            {"titulo": "A herança é indivisível",
             "texto": "Até a partilha, o direito dos herdeiros à propriedade e à posse da herança é indivisível "
                      "(Código Civil, art. 1.791, parágrafo único)."},
            {"titulo": "Vender sozinho não vale",
             "texto": "É ineficaz a venda de um bem da herança por um herdeiro, enquanto durar a "
                      "indivisibilidade, sem autorização do juiz (art. 1.793, § 3º)."},
            {"titulo": "Cessão de direitos",
             "texto": "O herdeiro pode ceder a sua parte na herança, como um todo, por escritura pública "
                      "(art. 1.793)."},
            {"titulo": "Venda pelo inventariante",
             "texto": "No inventário em cartório, o inventariante pode ser autorizado por escritura a vender um "
                      "bem, sem autorização do juiz (Resolução CNJ 35/2007, art. 11-A)."},
            {"titulo": "Há condições",
             "texto": "Parte ou todo o valor é vinculado às despesas do inventário, com garantia e prazo de até 1 ano para "
                      "pagá-las (art. 11-A, II, VI e § 1º)."},
        ],
        "chamada_final": "Você já passou por essa situação na família?",
        "legenda": "O imóvel ficou de herança, mas o inventário ainda não terminou. Dá para vender?\n\n1. Até a "
                   "partilha, a herança é indivisível: nenhum herdeiro é dono exclusivo de um bem.\n2. Por "
                   "isso, é ineficaz a venda de um bem por um herdeiro, sem prévia autorização do juiz, "
                   "enquanto durar a indivisibilidade.\n3. O herdeiro pode ceder os seus direitos na herança, "
                   "por escritura pública. A cessão sobre um bem específico, sozinha, é ineficaz.\n4. No "
                   "inventário em cartório, o inventariante pode ser autorizado, por escritura, a vender um "
                   "bem, com condições: parte ou todo o valor vinculado às despesas do inventário, garantia, "
                   "ausência de indisponibilidade de bens dos herdeiros e do cônjuge, e prazo de até 1 ano "
                   "para pagar as despesas, entre outras.\n\nCada família exige análise própria.\n\nVocê já "
                   "passou por essa situação? Conte nos comentários.",
        "hashtags": ["#heranca", "#inventario", "#vendadeimovel", "#direitoimobiliario"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1.791 e 1.793 ({CONFERIDO})",
                   f"Resolução CNJ 35/2007, art. 11-A, incluído pela Resolução 571/2024 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 28/12
    {
        "id": "2026-12-28_reel-inss-negou-recurso",
        "data_publicacao": "2026-12-28", "formato": "reel", "area": "Direito Previdenciário",
        "titulo": "O INSS *negou* o seu pedido?",
        "subtitulo": "Existe recurso administrativo",
        "video_capa": V("8172125"), "video_final": V("7393176"),
        "trilha": TRILHA("590331-inspiring-emotional"),
        "slides": [
            {"titulo": "O prazo",
             "texto": "São 30 dias, contados da ciência da decisão.",
             "video": V("7219070")},
            {"titulo": "Quem julga",
             "texto": "O Conselho de Recursos da Previdência Social, o CRPS.",
             "video": V("7821798")},
        ],
        "chamada_final": "Leia com atenção o motivo da negativa.",
        "legenda": "Receber uma negativa do INSS não significa que o caminho acabou.\n\n1. Cabe recurso ao "
                   "Conselho de Recursos da Previdência Social, o CRPS (Decreto 3.048/1999, art. 305, I).\n2. O "
                   "prazo é de 30 dias, contados da ciência da decisão (art. 305, § 1º, II).\n3. O próprio INSS "
                   "pode rever a sua decisão e reconhecer o direito (art. 305, § 3º).\n\nAntes de recorrer, "
                   "leia com atenção o motivo da negativa: muitas vezes, falta um documento ou há um erro no "
                   "cadastro. Conforme o caso, também é possível buscar o Poder Judiciário.\n\nVocê já passou "
                   "por isso? Salve e compartilhe com quem precisa.",
        "hashtags": ["#inss", "#recursoadministrativo", "#beneficionegado", "#direitoprevidenciario"] + TAGS_FIXAS,
        "fontes": [f"Decreto 3.048/1999, art. 305, I, § 1º, II, e § 3º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 30/12
    {
        "id": "2026-12-30_imovel-na-empresa-itbi",
        "data_publicacao": "2026-12-30", "formato": "carrossel", "area": "Direito Empresarial",
        "titulo": "Imóvel na empresa: o STF *decidiu* sobre o ITBI",
        "subtitulo": "O que diz o Tema 1.348.",
        "foto": F("20776189"), "escurecer": 0.55,
        "slides": [
            {"titulo": "A regra",
             "texto": "O ITBI não incide sobre o imóvel que o sócio transfere à empresa para realizar o capital "
                      "social (Constituição, art. 156, § 2º, I)."},
            {"titulo": "A dúvida",
             "texto": "A imunidade vale também para empresas que vivem de comprar, vender ou alugar imóveis?"},
            {"titulo": "A decisão",
             "texto": "Em 19/10/2026, o STF decidiu que sim: na realização do capital, a imunidade independe da "
                      "atividade da empresa (Tema 1.348, RE 1.495.108)."},
            {"titulo": "Os limites",
             "texto": "A imunidade vai até o valor do capital a ser integralizado (Tema 796), e o município "
                      "pode apurar simulação ou fraude."},
            {"titulo": "E o registro?",
             "texto": "A certidão da Junta Comercial é documento hábil para transferir o imóvel no registro "
                      "(Lei 8.934/1994, art. 64)."},
        ],
        "chamada_final": "Você sabia dessa decisão do STF?",
        "legenda": "Uma decisão importante para quem pensa em colocar imóvel na empresa ou em holding.\n\nA "
                   "Constituição afasta o ITBI na transmissão de bens à pessoa jurídica em realização de "
                   "capital. A dúvida era se isso valia também para empresas com atividade imobiliária.\n\nNo "
                   "julgamento do Tema 1.348 (RE 1.495.108), concluído em 19 de outubro de 2026, o STF decidiu, "
                   "por maioria, que a imunidade na realização do capital social é incondicionada, "
                   "independentemente da atividade da empresa.\n\nDois limites:\n1. O valor do capital social "
                   "a ser integralizado (Tema 796).\n2. Os municípios podem demonstrar eventual simulação ou "
                   "fraude à lei.\n\nNa conferência de 25/11/2026, o andamento do STF registrava a ata do "
                   "julgamento, publicada em 22/10. A decisão ainda pode ser objeto de recurso.\n\nVocê sabia "
                   "dessa decisão? Conte nos comentários.",
        "hashtags": ["#itbi", "#holding", "#direitoempresarial", "#stf"] + TAGS_FIXAS,
        "fontes": [f"STF, Tema 1.348, RE 1.495.108: andamento oficial, julgamento de 19/10/2026 ({CONFERIDO})",
                   f"Constituição, art. 156, § 2º, I ({CONFERIDO})", f"Lei 8.934/1994, art. 64 ({CONFERIDO})"],
    },
]

STORIES = [
    {"id": "2026-12-05_stories-mito-firma-reconhecida", "data_publicacao": "2026-12-05", "tipo": "mito_verdade",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "MITO OU VERDADE?", "titulo": "Contrato com firma reconhecida transfere o imóvel.",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "Mito!", "titulo": "A firma só confirma a *assinatura*.",
          "texto": "A propriedade se transfere com o registro do título no Registro de Imóveis "
                   "(Código Civil, art. 1.245)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Quem não registra *não é dono*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, art. 1.245; CPC, art. 411, I ({CONFERIDO})"]},
    {"id": "2026-12-12_stories-juridiques-usufruto", "data_publicacao": "2026-12-12", "tipo": "juridiques",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "JURIDIQUÊS X PORTUGUÊS", "titulo": "*Usufruto*",
          "texto": "Você sabe o que essa palavra quer dizer?", "rodape": "toque para traduzir"},
         {"etiqueta": "EM PORTUGUÊS", "titulo": "Usar o imóvel sem ser o *dono*.",
          "texto": "O usufrutuário pode morar, administrar e ficar com o aluguel (Código Civil, art. 1.394)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "No imóvel, o usufruto precisa de *registro*.",
          "texto": "Código Civil, art. 1.391.", "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, arts. 1.391 e 1.394 ({CONFERIDO})"]},
    {"id": "2026-12-19_stories-laje-matricula", "data_publicacao": "2026-12-19", "tipo": "voce_sabia",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "VOCÊ SABIA?", "titulo": "A laje pode ter matrícula *própria*.",
          "rodape": "toque para entender"},
         {"etiqueta": "EXPLICANDO", "titulo": "É o direito real de *laje*.",
          "texto": "A unidade de cima ou de baixo é registrada separada da construção-base "
                   "(Lei 6.015/1973, art. 176, § 9º)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Laje registrada, direito *seguro*.",
          "texto": "Código Civil, art. 1.510-A.", "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, art. 1.510-A; Lei 6.015/1973, art. 176, § 9º ({CONFERIDO})"]},
    {"id": "2026-12-26_stories-complete-heranca", "data_publicacao": "2026-12-26", "tipo": "complete",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "COMPLETE A FRASE", "titulo": "Até a partilha, a herança é…",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "Indivisível!", "titulo": "Nenhum herdeiro é dono *exclusivo* de um bem.",
          "texto": "Código Civil, art. 1.791, parágrafo único."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Partilha registrada, imóvel em *ordem*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, art. 1.791, parágrafo único ({CONFERIDO})"]},
]


def gravar():
    PASTA_FILA.mkdir(parents=True, exist_ok=True)
    for p in POSTS + [dict(s, formato="stories") for s in STORIES]:
        arq = PASTA_FILA / f"{p['id']}.json"
        if arq.exists():  # preserva o que já foi produzido (imagens, vídeo, testes)
            antigo = json.loads(arq.read_text(encoding="utf-8"))
            p = {**{k: antigo[k] for k in ("imagens", "video", "musica", "testes_video", "alertas_oab",
                                           "story_aviso") if k in antigo}, **p}
        arq.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(POSTS), len(STORIES)


if __name__ == "__main__":
    print(gravar())
