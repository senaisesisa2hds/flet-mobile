# Aula 1 — Fundamentos de Apps Mobile com Python e Flet
### Interface, controles, estado e navegação

> Este material é uma adaptação para **Python + Flet** do conteúdo do livro *Programação para Dispositivos Móveis* (SENAI-SP, 2025), que usa Flutter/Dart. A tabela abaixo mostra o paralelo entre os dois mundos os conceitos são os mesmos, muda a linguagem e a biblioteca.

**Por que Flet?** É a mesma engine de renderização do Flutter (interfaces bonitas, nativas, multiplataforma: Android, iOS, Web, Desktop), mas você escreve tudo em Python puro, sem precisar aprender Dart nem configurar XML/Gradle na mão.

---

## Objetivos de aprendizagem

Ao final desta aula, o aluno será capaz de:

1. Configurar um ambiente de desenvolvimento Flet funcional;
2. Entender e aplicar a árvore de controles (`Page`, `Container`, `Row`, `Column`, `Stack`);
3. Usar controles de entrada e botões, tratando eventos;
4. Gerenciar estado da interface (atualizar a tela em resposta a ações do usuário);
5. Construir listas dinâmicas de controles;
6. Implementar navegação entre múltiplas telas, inclusive com passagem de parâmetros;
7. Usar diálogos, `AppBar` e `NavigationBar`;
8. Construir, sozinho, um aplicativo de múltiplas telas com estado e navegação (**App de Tarefas**).

## Pré-requisitos

- Lógica de programação e Python básico (variáveis, `if/else`, laços, funções, listas e dicionários). Faremos uma revisão rápida focada no que será usado.
- Computador com Python 3.10+ instalado.

---

## Bloco 1 — Ambiente de desenvolvimento

### Teoria

Flet é uma biblioteca Python (`pip install flet`) que embute o motor gráfico do Flutter. Cada app Flet tem uma função `main(page)` que recebe a **página** (`ft.Page`), a raiz de tudo que aparece na tela.

Instalação (recomenda-se um ambiente virtual):

```bash
python -m venv venv
Windows: venv\Scripts\activate
pip install "flet[all]"
```
### Primeiro app

```python

# Fazer código com Professor


```

Rode com `flet run 01_ola.py` (ou `python 01_ola.py`). Obs: Se der erro rode: `python -m pip install --upgrade flet` e confirme `flet --version`. A tela atualiza sozinha (hot reload).

> **Atenção de versão:** em versões antigas de Flet (anteriores a 2025) o comando final era `ft.app(target=main)`. Se você encontrar esse padrão em tutoriais antigos, saiba que hoje o equivalente é `ft.run(main)`.

### Mini-exercício 1b — Cartão de apresentação pessoal

Crie um app que mostre, na janela, seu nome (texto grande) e uma frase curta sobre você (texto menor), usando `page.title`, `page.window.width/height` (tamanho da janela, útil ao rodar no desktop durante o desenvolvimento) e dois controles `ft.Text` com tamanhos (`size=`) diferentes.

**Solução:**

```python


# Fazer código com Professor



```

Rode com `flet run 01b_cartao.py` (ou `python 01b_cartao.py`). Edite o texto e salve — com `flet run` a tela atualiza sozinha (hot reload). Existe também: `flet run --web 01b_cartao.py` e `flet run --android 01b_cartao.py` ou `flet run --ios 01b_cartao.py`.

---
## Bloco 2 — A árvore de controles

### Teoria

Todo app Flet é uma **árvore**: `Page` é a raiz, e cada controle pode ter controles-filhos. Os principais controles de layout ("container controls") são:

| Controle | Para que serve |
|---|---|
| `ft.Page` | Raiz da árvore; representa a tela/janela inteira |
| `ft.Container` | Uma "caixa" com padding, margin, cor de fundo, borda, alinhamento — o "coringa" do layout |
| `ft.Row` | Organiza os filhos **horizontalmente** |
| `ft.Column` | Organiza os filhos **verticalmente** (é o padrão de `page.add()`) |
| `ft.Stack` | Sobrepõe os filhos (posicionamento livre com `top`, `left`, etc.) |
| `ft.Card` | Como um `Container`, mas com sombra e cantos arredondados (estilo "cartão") |

Propriedades comuns de `Container`: `width`, `height`, `padding`, `margin`, `bgcolor`, `border_radius`, `alignment=ft.Alignment.CENTER`, `expand=True` (ocupa o espaço disponível).

```python


# Fazer código com Professor



```

> **Note o padrão de aninhamento:** `Container` → `Column` → (`Text`, `Text`, `Row` → (`Button`, `Button`)). Pensar em "caixas dentro de caixas" é a chave para montar qualquer tela.

### Mini-exercício 2b — Cartão de perfil

Monte um `Container` com `border_radius`, contendo uma `Column` com: um `ft.Text` (nome, `size=22`, negrito), um `ft.Text` (profissão, cor cinza) e uma `ft.Row` com dois `ft.Icon` (por exemplo `ft.Icons.EMAIL` e `ft.Icons.PHONE`) ao lado de textos de contato.

**Solução:**

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Perfil"

    # Cor de fundo da página inteira: azul marinho escuro
    page.bgcolor = "#0D1B2A"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    page.add(
        # Container principal: um "cartão" com largura fixa e visual arredondado
        ft.Container(
            width=300,  # largura fixa do cartão
            padding=20,  # espaçamento interno entre o conteúdo e as bordas
            bgcolor="#1B263B",  # cor de fundo do cartão (azul um pouco mais claro que o fundo)
            border_radius=16,  # arredondamento das bordas
            content=ft.Column(  # organiza os itens verticalmente, um abaixo do outro
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza tudo dentro do cartão
                controls=[
                    # Nome em destaque: tamanho maior, negrito e cor de destaque
                    ft.Text("João Pereira", size=22, weight=ft.FontWeight.BOLD, color="#48CAE4"),

                    # Cargo/função, em azul claro suave para dar menos destaque
                    ft.Text("Desenvolvedor mobile", color="#90E0EF"),

                    # Linha com ícone de e-mail + o texto do e-mail, centralizada
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.EMAIL, color="#48CAE4"),
                            ft.Text("joao@email.com", color="#E0FBFC"),
                        ],
                    ),

                    # Linha com ícone de telefone + o texto do telefone, centralizada
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.PHONE, color="#48CAE4"),
                            ft.Text("(11) 90000-0000", color="#E0FBFC"),
                        ],
                    ),
                ]
            ),
        )
    )

# Inicia a aplicação, chamando a função main() como ponto de entrada
ft.run(main)
```

### Mini-exercício 2c — Grade de cards

Usando `Row` com vários `Container` dentro (cada um representando um produto com nome e preço), monte uma "prateleira" horizontal de 3 produtos. Dica: use `ft.Row(scroll=ft.ScrollMode.AUTO)` para permitir rolagem horizontal se não couber na tela.

**Solução:**

```python


# Fazer código com Professor



```

Repare que criamos uma **função** `card_produto(nome, preco)` que devolve um controle — o mesmo padrão do Mini-exercício 2, agora com Flet.

---

## Bloco 3 — Controles de entrada e botões

### Teoria

| Categoria | Controles |
|---|---|
| Botões | `ElevatedButton`, `FilledButton`, `OutlinedButton`, `TextButton`, `IconButton`, `FloatingActionButton` |
| Entrada de texto | `TextField` (`label`, `hint_text`, `password=True`, `multiline=True`, `keyboard_type=`) |
| Seleção | `Checkbox`, `Switch`, `Slider`, `Dropdown`, `Radio` (dentro de um `RadioGroup`) |

Todo controle interativo tem um `on_<evento>` — o mais comuns são `on_click` (botões) e `on_change` (campos de entrada/seleção). A função de evento recebe um parâmetro (convencionalmente chamado `e`), que representa o evento; `e.control` é o próprio controle que dispara o evento.

```python


# Fazer código com Professor



```

Repare em dois detalhes importantes:

1. Alterar `.value` (ou qualquer propriedade) de um controle **não muda a tela sozinho** — é preciso chamar `page.update()` depois.
2. `error_text` é uma forma simples de validação visual em `TextField`.

> **Dica de centralização:** controles como `Checkbox` e `Row`/`Column` tendem a ocupar toda a largura disponível e alinhar o conteúdo interno à esquerda. Para centralizar de verdade, envolva-os numa `ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[...])`.

### Mini-exercício 3b — Formulário de cadastro

Crie um formulário com: `TextField` para nome, `TextField` para e-mail, `Dropdown` para "Estado" (3 opções), um `Checkbox` "Quero receber novidades" e um botão "Cadastrar" que mostra um resumo dos dados digitados em um `ft.Text` abaixo do formulário.

**Solução:**

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Cadastro"

    # Cor de fundo da página inteira: roxo escuro
    page.bgcolor = "#241E3D"

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Campo de texto para o nome
    nome = ft.TextField(
        label="Nome",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#B8A9D9"),
        border_color="#6C5B9E",
        focused_border_color="#B388EB",
    )

    # Campo de texto para o e-mail
    email = ft.TextField(
        label="E-mail",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#B8A9D9"),
        border_color="#6C5B9E",
        focused_border_color="#B388EB",
    )

    # Dropdown de seleção de estado
    estado = ft.Dropdown(
        label="Estado",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#B8A9D9"),
        border_color="#6C5B9E",
        options=[ft.dropdown.Option("SP"), ft.dropdown.Option("RJ"), ft.dropdown.Option("MG")],
    )

    # Checkbox de aceite para receber novidades
    novidades = ft.Checkbox(
        label="Quero receber novidades",
        active_color="#B388EB",
        label_style=ft.TextStyle(color="#E5DCF5"),
    )

    # Texto de resumo, exibido após o cadastro
    resumo = ft.Text(color="#B388EB")

    def cadastrar(e):
        resumo.value = (
            f"{nome.value} ({email.value}) — {estado.value or 'sem estado'} — "
            f"novidades: {'sim' if novidades.value else 'não'}"
        )
        page.update()

    # Column explícita centralizando todos os controles, inclusive o checkbox
    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nome,
                email,
                estado,
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[novidades]),
                ft.ElevatedButton(
                    "Cadastrar",
                    on_click=cadastrar,
                    bgcolor="#B388EB",
                    color="#241E3D",
                ),
                resumo,
            ],
        )
    )

ft.run(main)
```

### Mini-exercício 4 — Contador (+/-)

Um clássico para fixar `on_click` + `page.update()`: um `ft.Text` mostrando um número (iniciando em 0) e dois `IconButton` (`ft.Icons.REMOVE` e `ft.Icons.ADD`) para diminuir/aumentar o valor.

**Solução:**

```python


# Fazer código com Professor



```

> **Por que `nonlocal`?** `valor` é uma variável da função `main`; as funções `somar`/`subtrair` estão *dentro* dela e precisam avisar ao Python que vão alterar (não criar uma nova) `valor`. Isso é "estado" em Flet: uma variável comum, e uma função que a atualiza e chama `page.update()`.

---

## Bloco 4b — Estado e atualização da interface

### Teoria

Diferente do Flutter (que tem `StatefulWidget` + `setState()`), em Flet **qualquer variável Python é seu estado**. A regra de ouro é:

> Mude a variável (ou a propriedade do controle) → depois chame `page.update()`.

Boas práticas:

- Guarde o estado em variáveis fora das funções de evento (na função `main`, por exemplo), e reconstrua/atualize os controles a partir dele.
- Para trechos de tela que mudam bastante (por exemplo, listas), é comum escrever uma função `atualizar_tela()` que limpa e reconstrói aquele pedaço, chamada sempre que o estado muda.
- Evite duplicar o dado em vários lugares; tenha **uma fonte de verdade** (a variável/lista) e derive a tela dela.

```python


# Fazer código com Professor



```

### Mini-exercício 5 — Avaliação por estrelas

Crie 5 `IconButton` (`ft.Icons.STAR_BORDER` / `ft.Icons.STAR`) em uma `Row`, representando uma avaliação de 1 a 5 estrelas. Ao clicar em uma estrela, todas as estrelas até ali (inclusive) ficam preenchidas (`ft.Icons.STAR`), e as seguintes ficam vazias. Mostre também um texto "Sua nota: X/5".

**Solução:**

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Avaliação"

    # Cor de fundo da página inteira: marrom escuro (combina bem com dourado das estrelas)
    page.bgcolor = "#2B2118"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Texto que mostra a nota atual
    nota = ft.Text("Sua nota: 0/5", color="#F2C94C", size=16)
    estrelas = []  # lista que guardará os 5 IconButton das estrelas

    def avaliar(indice):
        # Função geradora: cria e devolve um handler que "lembra" o índice da estrela
        # (evita o bug de closure tardio em laços — veremos em detalhe no Bloco 7)
        def handler(e):
            for i, botao in enumerate(estrelas):
                botao.icon = ft.Icons.STAR if i <= indice else ft.Icons.STAR_BORDER
            nota.value = f"Sua nota: {indice + 1}/5"
            page.update()
        return handler

    # Cria as 5 estrelas, cada uma com sua própria cor dourada
    for i in range(5):
        estrelas.append(
            ft.IconButton(ft.Icons.STAR_BORDER, on_click=avaliar(i), icon_color="#F2C94C")
        )

    page.add(
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=estrelas),  # estrelas centralizadas
        nota,
    )

ft.run(main)
```

> Repare que `avaliar(indice)` **devolve uma função** — é o mesmo truque do card de produto (Bloco 4), agora aplicado a eventos: cada botão precisa "lembrar" seu próprio índice, e uma função geradora resolve isso (voltaremos a esse ponto no próximo bloco).

---

## Bloco 5b — Listas dinâmicas de controles

### Teoria

Uma tela de lista (tarefas, produtos, mensagens...) segue sempre o mesmo roteiro:

1. Guarde os dados em uma **lista Python** (de dicionários, geralmente);
2. Tenha um controle contêiner vazio na tela, geralmente um `ft.ListView` (rola automaticamente) ou uma `ft.Column`;
3. Escreva uma função `atualizar_lista()` que limpa esse contêiner (`.controls.clear()`) e o reconstrói a partir da lista de dados, usando uma função auxiliar `build_item(dado)`;
4. Toda vez que os dados mudarem (adicionar/remover/editar), chame `atualizar_lista()`.

**Cuidado com o "closure tardio" (late binding) em laços:** se você criar botões dentro de um `for` usando `lambda e: fazer_algo(item)` diretamente, todos os botões acabam "vendo" o **último** valor de `item` do laço, não o valor de quando foram criados. A solução mais simples é usar uma **função separada** que recebe o item como parâmetro (como fizemos em `card_produto` e `avaliar`).

```python


# Fazer código com Professor



```

> **Por que `remover` funciona sem bug de closure?** Porque `nome` é o **parâmetro** de `build_item`, criado de novo a cada chamada — diferente de uma variável de laço compartilhada.

### Mini-exercício 6 — Lista de compras com quantidade

Evolua o exemplo acima: cada item agora é um dicionário `{"nome": ..., "quantidade": ...}`. Adicione botões `+`/`-` para alterar a quantidade de cada item (sem removê-lo), além do botão de excluir.

**Solução (resumida — reaproveita a estrutura acima):**

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Lista de compras"

    # Cor de fundo da página inteira: verde-azulado escuro (petróleo)
    page.bgcolor = "#0E3B3B"

    # Centraliza o conteúdo horizontalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Fonte de verdade: lista de dicionários com nome e quantidade
    itens = [{"nome": "Leite", "qtd": 1}, {"nome": "Pão", "qtd": 2}]

    lista_view = ft.ListView(expand=True, spacing=8, width=340)
    campo = ft.TextField(
        label="Novo item",
        expand=True,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#7FD9D0"),
        border_color="#2E7C74",
        focused_border_color="#4FE0D0",
    )

    def build_item(item):
        # Recebe o próprio dicionário do item — permite alterar "qtd" in place
        def alterar_qtd(delta):
            # Função geradora: cria um handler que "lembra" se é +1 ou -1
            def handler(e):
                item["qtd"] = max(1, item["qtd"] + delta)
                atualizar_lista()
            return handler

        def remover(e):
            itens.remove(item)
            atualizar_lista()

        return ft.Row(
            controls=[
                ft.Text(item["nome"], expand=True, color="#DFF7F3"),
                ft.IconButton(ft.Icons.REMOVE, on_click=alterar_qtd(-1), icon_color="#4FE0D0"),
                ft.Text(str(item["qtd"]), color="#DFF7F3"),
                ft.IconButton(ft.Icons.ADD, on_click=alterar_qtd(1), icon_color="#4FE0D0"),
                ft.IconButton(ft.Icons.DELETE, on_click=remover, icon_color="#FF8585"),
            ]
        )

    def atualizar_lista():
        lista_view.controls.clear()
        for item in itens:
            lista_view.controls.append(build_item(item))
        page.update()

    def adicionar(e):
        if campo.value:
            itens.append({"nome": campo.value, "qtd": 1})
            campo.value = ""
            atualizar_lista()

    page.add(
        ft.Row(
            width=340,
            controls=[
                campo,
                ft.ElevatedButton(
                    "Adicionar", on_click=adicionar, bgcolor="#4FE0D0", color="#0E3B3B"
                ),
            ],
        ),
        lista_view,
    )
    atualizar_lista()

ft.run(main)
```

---

## Bloco 7 — Navegação entre telas (Views e rotas)

### Teoria

Um app "de verdade" quase sempre tem mais de uma tela. Em Flet isso é feito com:

- `page.route`: string da rota atual (ex.: `"/"`, `"/nova"`, `"/tarefa/3"`);
- `page.views`: lista (pilha) de `ft.View` — cada `View` é uma tela completa, com sua própria `appbar` e `controls`;
- `page.on_route_change`: evento disparado sempre que a rota muda — aqui você decide **quais Views devem existir** para a rota atual;
- `page.on_view_pop`: evento disparado quando o usuário volta (botão voltar do sistema/AppBar);
- `page.navigate("/rota")`: navega para uma rota (uso síncrono, dentro de `on_click` por exemplo).

O padrão recomendado é sempre **reconstruir `page.views` a partir de `page.route`**, dentro de `on_route_change`. Cada `ft.View` aceita as mesmas propriedades de alinhamento e padding de uma `Page`, então centralizar e aplicar padding funciona igual.

```python


# Fazer código com Professor



```

### Passagem de parâmetros com `TemplateRoute`

Para rotas com parâmetro (ex.: `/produto/7`), use `ft.TemplateRoute`:

```python
troute = ft.TemplateRoute(page.route)
if troute.match("/produto/:id"):
    produto_id = troute.id   # string; converta com int(troute.id) se precisar
    ...
```

### Mini-exercício 8 — Login simples com passagem de nome

Crie duas telas: `"/"` com um `TextField` (nome) e um botão "Entrar" que navega para `"/boas-vindas/<nome digitado>"`; e a rota `"/boas-vindas/:nome"`, que exibe "Bem-vindo(a), `<nome>`!" e um botão "Sair" que volta para `"/"`.

**Solução:**

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Login"

    # Campo de nome compartilhado entre as chamadas de view_login()
    campo_nome = ft.TextField(
        label="Seu nome",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#F2B880"),
        border_color="#7A4A2E",
        focused_border_color="#F2994A",
    )

    def view_login():
        def entrar(e):
            if campo_nome.value:
                page.navigate(f"/boas-vindas/{campo_nome.value}")
        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Login")),
            bgcolor="#2E1F14",  # cor de fundo desta tela: marrom escuro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o formulário
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                campo_nome,
                ft.ElevatedButton(
                    "Entrar", on_click=entrar, bgcolor="#F2994A", color="#2E1F14"
                ),
            ],
        )

    def view_boas_vindas(nome):
        return ft.View(
            route=f"/boas-vindas/{nome}",
            appbar=ft.AppBar(title=ft.Text("Boas-vindas")),
            bgcolor="#142E2A",  # cor de fundo desta tela: verde-azulado escuro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza a mensagem
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                ft.Text(f"Bem-vindo(a), {nome}!", size=22, color="#5FE0C0"),
                ft.ElevatedButton(
                    "Sair",
                    on_click=lambda e: page.navigate("/"),
                    bgcolor="#5FE0C0",
                    color="#142E2A",
                ),
            ],
        )

    def route_change(e):
        page.views.clear()
        page.views.append(view_login())
        troute = ft.TemplateRoute(page.route)
        if troute.match("/boas-vindas/:nome"):
            page.views.append(view_boas_vindas(troute.nome))
        page.update()

    def view_pop(e):
        page.views.pop()
        page.navigate(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)

ft.run(main)
```

---

## Bloco 9 — Diálogos, AppBar e NavigationBar

### Teoria

- **`ft.AlertDialog`**: janela modal para confirmações/avisos. Abre com `page.show_dialog(dialogo)` e fecha com `page.pop_dialog()`.
- **`ft.SnackBar`**: mensagem rápida no rodapé da tela (feedback de ação). Também usa `page.show_dialog(...)`.
- **`ft.AppBar`**: barra superior de uma `View` (título, ícone de voltar automático, `actions=[...]`).
- **`ft.NavigationBar`**: barra inferior com "abas" (ex.: Início/Busca/Perfil), definida em `page.navigation_bar` e com evento `on_change`.

```python
import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Diálogos"

    # Cor de fundo da página: vinho/marsala escuro
    page.bgcolor = "#3D0F1E"

    # Centraliza o botão na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    def confirmar_saida(e):
        def sim(e):
            page.pop_dialog()
            page.show_dialog(ft.SnackBar(ft.Text("Você saiu.")))
        def nao(e):
            page.pop_dialog()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmação"),
            content=ft.Text("Deseja realmente sair?"),
            actions=[ft.TextButton("Não", on_click=nao), ft.TextButton("Sim", on_click=sim)],
        )
        page.show_dialog(dialogo)

    # Botão que abre o diálogo de confirmação, com cor de destaque em rosa
    page.add(
        ft.ElevatedButton(
            "Sair", on_click=confirmar_saida, bgcolor="#E0466E", color="#3D0F1E"
        )
    )

ft.run(main)
```

---

## Bloco 10 — Projeto guiado: App de Tarefas

### Especificação

Um app de múltiplas telas que reúne **tudo** desta aula:

- **Tela "/" (Lista de tarefas):** mostra as tarefas em um `ListView`; cada tarefa tem um `Checkbox` (concluída ou não), título, uma "bolinha" colorida de prioridade e, ao tocar na tarefa, navega para o detalhe; um `FloatingActionButton` "+" leva para a tela de nova tarefa.
- **Tela "/nova" (Nova tarefa):** formulário com título, descrição e prioridade (`RadioGroup`); botão "Salvar" adiciona a tarefa e volta para a lista, com um `SnackBar` de confirmação.
- **Tela "/tarefa/:id" (Detalhe):** mostra título, descrição e prioridade completos; botão "Excluir" (com confirmação por `AlertDialog`) e o botão de voltar (automático na `AppBar`).

> Nesta versão, cada tela do app tem sua própria cor de fundo e todas usam `horizontal_alignment=ft.CrossAxisAlignment.CENTER` + `padding=ft.Padding(top=60, bottom=60, left=0, right=0)`, para manter o conteúdo sempre centralizado e respirando na vertical.

### Passo a passo

**1. Estrutura de dados.** Cada tarefa é um dicionário: `{"id": int, "title": str, "description": str, "priority": "alta"|"media"|"baixa", "done": bool}`. Guardamos a lista em `tasks = []` e um contador `next_id = [1]` (lista de 1 elemento, para poder incrementar sem `nonlocal`).

**2. Função auxiliar de cor por prioridade:**

```python
# Cores vivas de prioridade, para contrastar com os fundos escuros das telas
PRIORITY_COLOR = {"alta": "#FF6B6B", "media": "#F2C94C", "baixa": "#6FCF97"}
```

**3. `view_lista()`** monta o `ListView` a partir de `tasks`, usando uma função `build_task_row(t)` (evitando o bug de closure em laço).

**4. `view_nova()`** monta o formulário e, ao salvar, faz `tasks.append({...})`, incrementa `next_id[0]` e chama `page.navigate("/")`.

**5. `view_detalhe(task_id)`** procura a tarefa pelo id (`next((t for t in tasks if t["id"] == task_id), None)`) e monta a tela; se não achar, mostra uma mensagem de erro amigável.

**6. `route_change`/`view_pop`** seguem exatamente o padrão do Bloco 8, usando `ft.TemplateRoute("/tarefa/:id")`.

### Código completo

```python
import flet as ft

# Cores de prioridade (usadas na "bolinha" e no texto de detalhe)
PRIORITY_COLOR = {"alta": "#FF6B6B", "media": "#F2C94C", "baixa": "#6FCF97"}
PRIORITY_LABEL = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}

# Cores de fundo, uma para cada tela do app (paleta azul/roxa escura, consistente entre telas)
BG_LISTA = "#161B33"
BG_NOVA = "#241B3D"
BG_DETALHE = "#1B2E3D"
BG_DESTAQUE = "#5C7CFA"  # cor de destaque (botões, ícones) usada nas 3 telas


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "App de Tarefas"

    # Dados iniciais: fonte de verdade das tarefas
    tasks: list[dict] = [
        {"id": 1, "title": "Estudar Flet", "description": "Terminar os mini-exercícios da Aula 1.",
         "priority": "alta", "done": False},
        {"id": 2, "title": "Revisar POO em Python", "description": "Classes, atributos e métodos.",
         "priority": "media", "done": False},
    ]
    next_id = [3]  # lista de 1 elemento, para incrementar sem precisar de "nonlocal"

    # ---------- Tela: Lista de tarefas ----------
    def build_task_row(t: dict) -> ft.Container:
        # Função "builder": recebe a tarefa e devolve a linha pronta (evita closure tardio)
        def ir_para_detalhe(e):
            page.navigate(f"/tarefa/{t['id']}")

        def alternar_concluida(e):
            t["done"] = e.control.value
            page.update()

        # Título com cor apagada quando a tarefa está concluída
        titulo = ft.Text(
            t["title"],
            expand=True,
            color="#6E7695" if t["done"] else "#E9ECFB",
        )

        return ft.Container(
            padding=12,
            border_radius=10,
            bgcolor="#232A4D",  # cor de fundo de cada linha de tarefa
            content=ft.Row(
                controls=[
                    ft.Checkbox(value=t["done"], on_change=alternar_concluida, active_color=BG_DESTAQUE),
                    ft.Container(width=10, height=10, border_radius=5, bgcolor=PRIORITY_COLOR[t["priority"]]),
                    titulo,
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#8892C4"),
                ]
            ),
            on_click=ir_para_detalhe,
        )

    def view_lista() -> ft.View:
        lista_view = ft.ListView(expand=True, spacing=8, width=340)
        for t in tasks:
            lista_view.controls.append(build_task_row(t))

        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Minhas Tarefas")),
            bgcolor=BG_LISTA,  # cor de fundo desta tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza a lista
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[lista_view],
            floating_action_button=ft.FloatingActionButton(
                icon=ft.Icons.ADD, on_click=lambda e: page.navigate("/nova"), bgcolor=BG_DESTAQUE
            ),
        )

    # ---------- Tela: Nova tarefa ----------
    def view_nova() -> ft.View:
        titulo = ft.TextField(
            label="Título", width=300, color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"), border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )
        descricao = ft.TextField(
            label="Descrição", multiline=True, min_lines=3, width=300, color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"), border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )
        prioridade = ft.RadioGroup(
            value="media",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(
                        value="alta",
                        label="Alta",
                        label_style=ft.TextStyle(color="#D8CFF2"),  # cor do texto
                        fill_color=BG_DESTAQUE,  # cor do círculo (selecionado/borda)
                    ),
                    ft.Radio(
                        value="media",
                        label="Média",
                        label_style=ft.TextStyle(color="#D8CFF2"),
                        fill_color=BG_DESTAQUE,
                    ),
                    ft.Radio(
                        value="baixa",
                        label="Baixa",
                        label_style=ft.TextStyle(color="#D8CFF2"),
                        fill_color=BG_DESTAQUE,
                    ),
                ]
            ),
        )

        def salvar(e):
            if not titulo.value:
                titulo.error_text = "Informe um título"
                page.update()
                return
            tasks.append(
                {
                    "id": next_id[0],
                    "title": titulo.value,
                    "description": descricao.value or "",
                    "priority": prioridade.value,
                    "done": False,
                }
            )
            next_id[0] += 1
            page.navigate("/")
            page.show_dialog(ft.SnackBar(ft.Text("Tarefa criada com sucesso!")))

        return ft.View(
            route="/nova",
            appbar=ft.AppBar(title=ft.Text("Nova tarefa")),
            bgcolor=BG_NOVA,  # cor de fundo desta tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o formulário
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                titulo,
                descricao,
                ft.Text("Prioridade:", color="#D8CFF2"),
                prioridade,
                ft.ElevatedButton(
                    "Salvar", on_click=salvar, bgcolor=BG_DESTAQUE, color="#161B33"
                ),
            ],
        )

    # ---------- Tela: Detalhe da tarefa ----------
    def view_detalhe(task_id: int) -> ft.View:
        tarefa = next((t for t in tasks if t["id"] == task_id), None)

        if tarefa is None:
            return ft.View(
                route=f"/tarefa/{task_id}",
                appbar=ft.AppBar(title=ft.Text("Tarefa não encontrada")),
                bgcolor=BG_DETALHE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                padding=ft.Padding(top=60, bottom=60, left=0, right=0),
                controls=[ft.Text("Essa tarefa não existe (ou já foi excluída).", color="#D6E8F0")],
            )

        def excluir_confirmado(e):
            tasks.remove(tarefa)
            page.pop_dialog()
            page.navigate("/")
            page.show_dialog(ft.SnackBar(ft.Text("Tarefa excluída.")))

        def cancelar(e):
            page.pop_dialog()

        dialogo = ft.AlertDialog(
            title=ft.Text("Excluir tarefa?"),
            content=ft.Text("Essa ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Excluir", on_click=excluir_confirmado),
            ],
        )

        return ft.View(
            route=f"/tarefa/{task_id}",
            appbar=ft.AppBar(title=ft.Text("Detalhe da tarefa")),
            bgcolor=BG_DETALHE,  # cor de fundo desta tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o conteúdo do detalhe
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                ft.Text(tarefa["title"], size=24, weight=ft.FontWeight.BOLD, color="#D6E8F0"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,  # centraliza a bolinha + rótulo de prioridade
                    controls=[
                        ft.Container(width=12, height=12, border_radius=6, bgcolor=PRIORITY_COLOR[tarefa["priority"]]),
                        ft.Text(f"Prioridade {PRIORITY_LABEL[tarefa['priority']]}", color="#A9C7D6"),
                    ]
                ),
                ft.Text(
                    tarefa["description"] or "(sem descrição)",
                    color="#D6E8F0",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Excluir",
                    icon=ft.Icons.DELETE,
                    on_click=lambda e: page.show_dialog(dialogo),
                    bgcolor="#FF6B6B",
                    color="#1B2E3D",
                ),
            ],
        )

    # ---------- Roteamento ----------
    def route_change(e):
        # Reconstrói toda a pilha de views a partir da rota atual
        page.views.clear()
        page.views.append(view_lista())

        if page.route == "/nova":
            page.views.append(view_nova())

        troute = ft.TemplateRoute(page.route)
        if troute.match("/tarefa/:id"):
            page.views.append(view_detalhe(int(troute.id)))

        page.update()

    def view_pop(e):
        page.views.pop()
        page.navigate(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)  # constrói a(s) view(s) da rota inicial


ft.run(main)
```

### Desafios extras (para quem terminar antes)

1. Adicione um campo de busca na tela de lista, filtrando as tarefas por título.
2. Ordene a lista por prioridade (alta → média → baixa).
3. Permita **editar** uma tarefa a partir da tela de detalhe (reaproveitando o formulário de `view_nova`).
4. Mostre um contador "X de Y tarefas concluídas" no topo da lista.

### Código completo (Desafios extras)

```python



# Tente/pesquise como implementar os extras



```

---

## O que você aprendeu hoje

- Instalar e rodar um app Flet, com hot reload;
- Montar interfaces com a árvore de controles (`Container`, `Row`, `Column`);
- Usar controles de entrada e botões, tratando eventos com `on_click`/`on_change`;
- Gerenciar estado (variáveis Python + `page.update()`);
- Construir listas dinâmicas de controles, evitando o bug clássico de closure em laços;
- Navegar entre telas com `page.views`, `page.route` e `ft.TemplateRoute`;
- Usar `AlertDialog` e `SnackBar` para diálogos e feedback;
- Centralizar conteúdo e aplicar padding vertical consistente em `Page` e `View`, com paletas de cor variadas por tela;
- Construir, do zero, um app de múltiplas telas com estado (**App de Tarefas**).

## Prévia da Aula 2

Na próxima aula, o **App de Tarefas** ganhará vida: vamos consumir uma API REST de verdade (GET/POST/PUT/DELETE), tratar requisições assíncronas, persistir dados localmente (para sobreviver ao fechar o app) e dar uma olhada em recursos de hardware do dispositivo (localização/GPS, câmera). O projeto final combinará tudo isso em uma versão "online" do app de hoje.