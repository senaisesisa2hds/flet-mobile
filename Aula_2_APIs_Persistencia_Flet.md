# Aula 2 — APIs REST, Persistência de Dados e Recursos do Dispositivo
### Consumindo a web e guardando dados de verdade 

> Continuação do material da Aula 1. Aqui cobrimos o equivalente Python/Flet aos capítulos 3, 4 e 5 do livro de referência (*Programação para Dispositivos Móveis*, SENAI-SP): consumo de Web Service RESTful, persistência de dados (local e visão geral de nuvem) e recursos de hardware.

| Livro de referência (Flutter/Dart) | Este material (Python/Flet) |
|---|---|
| `http` package | `httpx` |
| `Future` / `async`/`await` (Dart) | `async`/`await` (Python) |
| `jsonEncode` / `jsonDecode` | `json.dumps` / `json.loads` |
| `SharedPreferences` | `page.shared_preferences` |
| `Sqflite` | `sqlite3` (biblioteca padrão do Python) |
| `Geolocator`, `camera`, sensores | `flet-geolocator`, `FilePicker`, outros pacotes `flet-*` |
| `flutter build apk` | `flet build apk` |

## Objetivos de aprendizagem

1. Entender os conceitos de API REST, Web Service e os verbos HTTP;
2. Serializar e desserializar dados em JSON;
3. Fazer requisições GET, POST, PUT/PATCH e DELETE com `httpx`, de forma assíncrona;
4. Tratar erros de rede e exibir feedback visual (carregando/erro);
5. Persistir dados localmente com `page.shared_preferences` (chave-valor) e com `sqlite3` (relacional);
6. Ter uma visão geral de recursos de hardware (localização, câmera/galeria);
7. Saber o caminho para publicar um app Flet;
8. Evoluir o **App de Tarefas** da Aula 1 — que já conta com busca, ordenação por prioridade, edição de tarefas e contador de concluídas — para uma versão que também consome API e persiste dados de verdade entre usos.

## Pré-requisitos

Conteúdo da Aula 1 (controles, estado, navegação). Traga o arquivo do **App de Tarefas** pronto, já com busca, ordenação por prioridade, edição e o contador "X de Y tarefas concluídas".

---

## Bloco 1 — Retomada rápida

Revise: árvore de controles, `page.update()`, listas dinâmicas (evitar bug de closure), e o padrão de navegação (`page.views`, `page.route`, `ft.TemplateRoute`). O projeto de hoje **parte do App de Tarefas pronto da Aula 1** — já com campo de busca por título, ordenação por prioridade, edição de tarefas (reaproveitando o formulário de nova tarefa) e o contador "X de Y tarefas concluídas" no topo da lista. Tudo isso continua funcionando na versão de hoje; vamos apenas conectá-lo a uma API e fazê-lo persistir os dados de verdade.

---

## Bloco 2 — APIs REST e Web Services

### Teoria

- **Web Service**: um programa que expõe funcionalidades para outros programas através da rede (geralmente via HTTP).
- **API (Application Programming Interface)**: o "contrato" de como conversar com esse serviço — quais endereços (endpoints), quais dados enviar/receber.
- **REST**: um estilo de arquitetura onde cada recurso (ex.: uma tarefa, um usuário) tem uma URL própria, e a ação desejada é expressa pelo **verbo HTTP**:

| Verbo | Uso típico | Exemplo |
|---|---|---|
| `GET` | Buscar dado(s) | `GET /tarefas` (lista) ou `GET /tarefas/3` (uma) |
| `POST` | Criar um novo recurso | `POST /tarefas` |
| `PUT` | Atualizar um recurso **inteiro** | `PUT /tarefas/3` |
| `PATCH` | Atualizar **parte** de um recurso | `PATCH /tarefas/3` |
| `DELETE` | Remover um recurso | `DELETE /tarefas/3` |

- A maioria das APIs modernas troca dados em **JSON** (`{"id": 1, "title": "Estudar", "done": false}`) — veremos exatamente como isso funciona em Python já no próximo bloco, antes de fazer nossa primeira requisição.
- **Códigos de status HTTP** mais comuns: `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401/403` (autenticação/permissão), `404 Not Found`, `500 Internal Server Error`.

### API que usaremos nos exemplos

Vamos usar a **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), uma API pública e gratuita, sem necessidade de login, feita justamente para testes e ensino. Ela simula respostas de `POST`/`PUT`/`DELETE` (responde como se tivesse salvo, mas não persiste de verdade no servidor) — por isso, no projeto final, vamos **combinar a API com persistência local**, para que os dados realmente sobrevivam.

> **Nota para quem quiser ir além:** o livro de referência usa o *JSON Server* (Node.js) rodando localmente, o que permite CRUD "de verdade" numa API própria. Se a turma tiver Node.js instalado, é um ótimo exercício avançado rodar `npx json-server db.json` localmente e apontar os exemplos abaixo para `http://localhost:3000` em vez da JSONPlaceholder.

---

## Bloco 3 — JSON: serialização e desserialização

### Teoria

JSON (JavaScript Object Notation) é o formato de troca de dados mais usado em APIs. Em Python, o módulo padrão `json` converte entre **texto JSON** e **objetos Python** (dicts/listas):

```python
import json

tarefa = {"id": 1, "title": "Estudar Flet", "done": False}

texto = json.dumps(tarefa)          # dict Python -> string JSON (para ENVIAR)
print(texto)                        # '{"id": 1, "title": "Estudar Flet", "done": false}'

de_volta = json.loads(texto)        # string JSON -> dict Python (para LER)
print(de_volta["title"])            # Estudar Flet
```

- `json.dumps(obj)`: serializa (Python → texto). Útil para **guardar** dados em um arquivo/armazenamento de chave-valor, ou montar o corpo de um `POST`.
- `json.loads(texto)`: desserializa (texto → Python). É exatamente o que `resposta.json()` do `httpx` fará por baixo dos panos, já no próximo bloco, ao ler uma resposta de API.
- Listas inteiras também funcionam: `json.dumps(lista_de_dicts)` / `json.loads(texto_json)`.

> **Por que ver isso antes de `httpx`?** Toda vez que chamarmos `resposta.json()` daqui em diante, estaremos usando `json.loads` por baixo dos panos. Entender essa conversão primeiro evita que o método pareça "mágico".

### Mini-exercício 1 — Ida e volta

1. Crie uma lista Python com 3 dicts de tarefas (`id`, `title`, `done`);
2. Converta para uma string JSON com `json.dumps` e imprima;
3. "Simule" que essa string veio de um arquivo/API: converta de volta com `json.loads` e imprima quantas tarefas estão com `done=True`.

**Solução:**

```python
import json

# Lista Python de tarefas, nossa "fonte de verdade" antes de qualquer conversão
tarefas = [
    {"id": 1, "title": "Estudar Flet", "done": True},
    {"id": 2, "title": "Fazer o projeto", "done": False},
    {"id": 3, "title": "Revisar POO", "done": True},
]

# Passo 2: Python -> JSON (o que faríamos para ENVIAR ou GUARDAR os dados)
texto_json = json.dumps(tarefas)
print("JSON:", texto_json)

# Passo 3: JSON -> Python de novo (o que faríamos ao LER uma resposta de API
# ou um valor recuperado de um arquivo/armazenamento local)
tarefas_lidas = json.loads(texto_json)
concluidas = sum(1 for t in tarefas_lidas if t["done"])
print(f"{concluidas} de {len(tarefas_lidas)} tarefas concluídas.")
```

---

## Bloco 4 — Requisições HTTP com `httpx`

### Teoria

Instale a biblioteca:

```bash
pip install httpx
```

`httpx` é a biblioteca recomendada para fazer requisições HTTP em Python de forma assíncrona (parecida com `requests`, porém com suporte nativo a `async`/`await`, essencial para não travar a interface do app enquanto espera a resposta da rede).

```python
import httpx

async def buscar_tarefas():
    async with httpx.AsyncClient() as client:
        resposta = await client.get("https://jsonplaceholder.typicode.com/todos", params={"_limit": 10})
        resposta.raise_for_status()  # lança exceção se status for erro (4xx/5xx)
        return resposta.json()       # converte o corpo da resposta (JSON) em lista de dicts — é json.loads por baixo dos panos
```

### Mini-exercício 01 — Lista de tarefas vindas da API

Crie um app com um botão "Carregar tarefas" que busca as 10 primeiras tarefas em `GET /todos?_limit=10` e exibe os títulos em uma `ft.ListView`.

**Solução:**

```python
import flet as ft
import httpx


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Tarefas da API"

    # Cor de fundo da página inteira: azul petróleo escuro
    page.bgcolor = "#101B2D"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Lista onde os títulos das tarefas buscadas na API serão exibidos
    lista_view = ft.ListView(expand=True, spacing=6, width=320)

    async def carregar(e):
        # "async def": esta função usa "await" para não travar o app enquanto
        # espera a resposta da rede (entraremos em detalhes no próximo bloco)
        lista_view.controls.clear()
        async with httpx.AsyncClient() as client:
            resposta = await client.get(
                "https://jsonplaceholder.typicode.com/todos", params={"_limit": 10}
            )
            dados = resposta.json()  # texto JSON -> lista de dicts Python (json.loads por baixo dos panos)
        for tarefa in dados:
            lista_view.controls.append(ft.Text(f"• {tarefa['title']}", color="#CDE0F2"))
        page.update()

    page.add(
        ft.ElevatedButton("Carregar tarefas", on_click=carregar, bgcolor="#4C8BF5", color="#0B1622"),
        lista_view,
    )


ft.run(main)
```

Repare que `carregar` é uma função **`async def`** — necessário porque usamos `await` dentro dela. Em Flet, um manipulador de evento (`on_click`, `on_change` etc.) pode ser uma função normal (`def`) ou assíncrona (`async def`); use `async def` sempre que precisar de `await` dentro (requisições de rede, leitura de armazenamento, etc.).

---

## Bloco 5 — Requisições assíncronas no Flet

### Teoria

Por que assíncrono? Se a requisição de rede fosse **síncrona** (bloqueante), o app inteiro travaria (sem responder a toques, sem animações) até a resposta chegar — péssima experiência em uma rede lenta. Com `async`/`await`, o app continua responsivo enquanto espera.

Boas práticas:

- Mostre um indicador de carregamento (`ft.ProgressRing()`) enquanto a requisição está em andamento, escondendo o conteúdo antigo ou desabilitando botões;
- Sempre trate erros (próximo bloco) — toda chamada de rede pode falhar;
- `page.update()` funciona normalmente dentro de uma função `async def`, não precisa de nenhuma versão especial.

### Mini-exercício 02 — Indicador de carregamento

Refaça o Mini-exercício 2 adicionando um `ft.ProgressRing()` que aparece assim que o botão é clicado e desaparece quando os dados chegam. Desabilite o botão durante o carregamento (evita cliques duplicados).

**Solução:**

```python
import flet as ft
import httpx


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Tarefas da API"

    # Cor de fundo da página inteira: verde-azulado bem escuro (teal)
    page.bgcolor = "#0B2027"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    lista_view = ft.ListView(expand=True, spacing=6, width=320)
    progresso = ft.ProgressRing(visible=False, color="#2EC4B6")  # some/aparece durante o carregamento
    botao = ft.ElevatedButton("Carregar tarefas", bgcolor="#2EC4B6", color="#0B2027")

    async def carregar(e):
        # Mostra o indicador e desabilita o botão ANTES de iniciar a requisição
        botao.disabled = True
        progresso.visible = True
        lista_view.controls.clear()
        page.update()  # aplica essas mudanças na tela já, antes de aguardar a rede

        async with httpx.AsyncClient() as client:
            resposta = await client.get(
                "https://jsonplaceholder.typicode.com/todos", params={"_limit": 10}
            )
            dados = resposta.json()

        for tarefa in dados:
            lista_view.controls.append(ft.Text(f"• {tarefa['title']}", color="#CFF4F0"))

        # Restaura o botão e some com o indicador, agora que os dados já chegaram
        botao.disabled = False
        progresso.visible = False
        page.update()

    botao.on_click = carregar
    page.add(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[botao, progresso]), lista_view)


ft.run(main)
```

---

## Bloco 6 — POST, PUT, DELETE e tratamento de erros

### Teoria

```python
async with httpx.AsyncClient() as client:
    # Criar
    resp = await client.post("https://jsonplaceholder.typicode.com/todos",
                              json={"title": "Nova tarefa", "completed": False, "userId": 1})
    nova = resp.json()  # a API simulada devolve o objeto criado (com id novo)

    # Atualizar por completo
    resp = await client.put(f"https://jsonplaceholder.typicode.com/todos/{id}",
                             json={"title": "Editada", "completed": True, "userId": 1})

    # Atualizar parcialmente
    resp = await client.patch(f"https://jsonplaceholder.typicode.com/todos/{id}",
                               json={"completed": True})

    # Remover
    resp = await client.delete(f"https://jsonplaceholder.typicode.com/todos/{id}")
```

**Tratamento de erros**: envolva as chamadas em `try/except`, capturando pelo menos:

- `httpx.RequestError`: problema de conexão (sem internet, DNS, timeout);
- `httpx.HTTPStatusError`: a requisição chegou ao servidor, mas voltou com erro (`resposta.raise_for_status()` lança essa exceção para códigos 4xx/5xx).

```python
async def carregar(e):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resposta = await client.get("https://jsonplaceholder.typicode.com/todos")
            resposta.raise_for_status()
            dados = resposta.json()
    except httpx.RequestError:
        # Sem conexão, DNS falhou, ou a requisição nem chegou a ser respondida
        page.show_dialog(ft.SnackBar(ft.Text("Sem conexão com a internet.")))
        return
    except httpx.HTTPStatusError as erro:
        # O servidor respondeu, mas com um código de erro (4xx/5xx)
        page.show_dialog(ft.SnackBar(ft.Text(f"Erro do servidor: {erro.response.status_code}")))
        return
    # ... usar 'dados' normalmente a partir daqui
```

### Mini-exercício 03 — Cadastrar e excluir via API

Monte um mini-app: um `TextField` + botão "Adicionar" que faz `POST /todos` e acrescenta o título retornado a uma `ListView`; cada item da lista tem um botão de excluir que faz `DELETE /todos/{id}` e remove da tela. Trate erros de rede com `SnackBar`.

**Solução:**

```python
import flet as ft
import httpx

API = "https://jsonplaceholder.typicode.com/todos"


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Tarefas via API"

    # Cor de fundo da página inteira: marrom-avermelhado escuro
    page.bgcolor = "#2B1B17"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    campo = ft.TextField(
        label="Nova tarefa", width=240, color="#FFFFFF",
        label_style=ft.TextStyle(color="#E3B7A6"), border_color="#5A3A30",
        focused_border_color="#FF7F51",
    )
    lista_view = ft.ListView(expand=True, spacing=6, width=320)
    tarefas = []  # cache local em memória, só para esta sessão (sem persistência ainda)

    def build_item(tarefa):
        async def excluir(e):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.delete(f"{API}/{tarefa['id']}")
                    resp.raise_for_status()
            except httpx.HTTPError:
                page.show_dialog(ft.SnackBar(ft.Text("Não foi possível excluir agora.")))
                return
            tarefas.remove(tarefa)
            atualizar_lista()

        return ft.Row(
            controls=[
                ft.Text(tarefa["title"], expand=True, color="#F2DCCF"),
                ft.IconButton(ft.Icons.DELETE, on_click=excluir, icon_color="#FF7F51"),
            ]
        )

    def atualizar_lista():
        lista_view.controls.clear()
        for t in tarefas:
            lista_view.controls.append(build_item(t))
        page.update()

    async def adicionar(e):
        if not campo.value:
            return
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(API, json={"title": campo.value, "completed": False, "userId": 1})
                resp.raise_for_status()
                nova = resp.json()
        except httpx.HTTPError:
            page.show_dialog(ft.SnackBar(ft.Text("Não foi possível criar a tarefa agora.")))
            return
        tarefas.append(nova)
        campo.value = ""
        atualizar_lista()

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[campo, ft.ElevatedButton("Adicionar", on_click=adicionar, bgcolor="#FF7F51", color="#2B1B17")],
        ),
        lista_view,
    )


ft.run(main)
```

---

## Bloco 7 — Persistência local: `shared_preferences`

### Teoria

`page.shared_preferences` guarda pares chave-valor **no dispositivo**, sobrevivendo ao fechar o app (equivalente ao `SharedPreferences` do Flutter/Android). É assíncrono (precisa de `await`) e ideal para configurações simples, preferências do usuário, ou pequenas listas — **não** para grandes volumes de dados relacionais (para isso, SQLite, no próximo bloco).

```python
# Gravar
await page.shared_preferences.set("nome_usuario", "Maria")
await page.shared_preferences.set("modo_escuro", True)

# Ler (usar valor padrão se a chave não existir)
nome = await page.shared_preferences.get("nome_usuario") or "Visitante"

# Verificar existência / remover / limpar tudo
existe = await page.shared_preferences.contains_key("nome_usuario")
await page.shared_preferences.remove("nome_usuario")
await page.shared_preferences.clear()   # cuidado: apaga TODAS as chaves do dispositivo
```

> **Dica de nomenclatura:** como o armazenamento é compartilhado entre apps Flet rodando no mesmo dispositivo/usuário, prefixe suas chaves, ex.: `"minhaescola.tarefas.lista"`.

Para guardar **listas de dicts** (como nossas tarefas), combinamos com o `json.dumps`/`json.loads` que já vimos no Bloco 3:

```python
import json

async def salvar_tarefas(tarefas):
    await page.shared_preferences.set("app_tarefas.lista", json.dumps(tarefas))

async def carregar_tarefas():
    texto = await page.shared_preferences.get("app_tarefas.lista")
    return json.loads(texto) if texto else []
```

### Mini-exercício 4 — Favoritos que sobrevivem ao fechar o app

Crie uma lista fixa de 5 nomes de filmes (`ft.Checkbox` para cada) representando "favoritos". Ao marcar/desmarcar, salve a lista de favoritos (nomes marcados) em `shared_preferences` como JSON. Ao abrir o app, carregue os favoritos salvos e marque os checkboxes correspondentes.

**Solução:**

```python
import flet as ft
import json

FILMES = ["Matrix", "Interestelar", "Cidade de Deus", "Vingadores", "Coringa"]
CHAVE = "app_favoritos.filmes"


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Filmes favoritos"

    # Cor de fundo da página inteira: roxo escuro
    page.bgcolor = "#241E3D"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    checkboxes = {}  # nome do filme -> Checkbox correspondente

    async def carregar_favoritos():
        # Lê o JSON salvo (se existir) e marca os checkboxes já favoritados
        texto = await page.shared_preferences.get(CHAVE)
        favoritos = json.loads(texto) if texto else []
        for filme, caixa in checkboxes.items():
            caixa.value = filme in favoritos
        page.update()

    async def alternar(e):
        # Sempre que qualquer checkbox muda, recalcula a lista inteira de favoritos e salva
        favoritos = [filme for filme, caixa in checkboxes.items() if caixa.value]
        await page.shared_preferences.set(CHAVE, json.dumps(favoritos))

    for filme in FILMES:
        checkboxes[filme] = ft.Checkbox(
            label=filme, on_change=alternar,
            active_color="#B388EB", label_style=ft.TextStyle(color="#D8CFF2"),
        )

    page.add(
        ft.Text("Meus filmes favoritos", size=20, weight=ft.FontWeight.BOLD, color="#F2C94C"),
        *checkboxes.values(),
    )
    page.run_task(carregar_favoritos)  # dispara a carga assíncrona assim que o app inicia


ft.run(main)
```

> **`page.run_task(...)`**: como `main()` não é assíncrona neste exemplo, usamos `page.run_task()` para "disparar" a função assíncrona `carregar_favoritos()` assim que o app inicia (não dá para usar `await` fora de uma função `async`).

---

## Bloco 8 — Persistência local: SQLite com `sqlite3`

### Teoria

Para dados **relacionais** (várias tabelas, buscas, filtros, grandes volumes), usamos SQLite via `sqlite3` — módulo **padrão** do Python (não precisa instalar nada). É o equivalente direto ao *Sqflite* do Flutter.

Onde salvar o arquivo do banco em um app mobile? Flet expõe a variável de ambiente `FLET_APP_STORAGE_DATA`, uma pasta privada do app que persiste entre usos (e não é apagada pelo sistema):

```python
import os
import sqlite3

pasta_dados = os.environ.get("FLET_APP_STORAGE_DATA", ".")
caminho_bd = os.path.join(pasta_dados, "contatos.db")

conexao = sqlite3.connect(caminho_bd)
conexao.execute("""
    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT
    )
""")
conexao.commit()
```

Operações básicas:

```python
# Inserir
conexao.execute("INSERT INTO contatos (nome, telefone) VALUES (?, ?)", (nome, telefone))
conexao.commit()

# Listar
cursor = conexao.execute("SELECT id, nome, telefone FROM contatos ORDER BY nome")
linhas = cursor.fetchall()   # lista de tuplas (id, nome, telefone)

# Excluir
conexao.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
conexao.commit()
```

> Sempre use `?` como marcador de posição (parâmetro) em vez de montar a SQL com f-string — isso evita *SQL Injection* e é a forma correta de passar valores.

### Mini-exercício 5 — Cadastro de contatos com SQLite

Crie um app com `TextField` (nome) + `TextField` (telefone) + botão "Salvar" que insere no banco; abaixo, uma `ListView` que lista todos os contatos (lidos do banco) com botão de excluir.

**Solução:**

```python
import os
import sqlite3
import re
import flet as ft


# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================

# Define onde o banco de dados será armazenado.
# No celular, o Flet utiliza a pasta própria de armazenamento do aplicativo.
pasta_dados = os.environ.get("FLET_APP_STORAGE_DATA", ".")

# Nome e caminho do banco de dados.
caminho_bd = os.path.join(pasta_dados, "contatos.db")


def main(page: ft.Page):

    # ========================================================
    # CONFIGURAÇÃO DA PÁGINA
    # ========================================================

    # Título que aparece na barra da janela/aba.
    page.title = "Contatos (SQLite)"

    # Cor de fundo da página inteira.
    page.bgcolor = "#0F2019"

    # Centraliza os controles horizontalmente.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Espaçamento interno da página.
    page.padding = ft.Padding(
        top=60,
        bottom=60,
        left=20,
        right=20
    )

    # ========================================================
    # BANCO DE DADOS
    # ========================================================

    # Abre ou cria o banco de dados.
    conexao = sqlite3.connect(caminho_bd)

    # Cria a tabela caso ela ainda não exista.
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT
        )
        """
    )

    conexao.commit()

    # ========================================================
    # CAMPOS DO FORMULÁRIO
    # ========================================================

    nome = ft.TextField(
        label="Nome",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#9FCBAE"),
        border_color="#2E5240",
        focused_border_color="#6FCF97",
    )

    telefone = ft.TextField(
        label="Telefone",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#9FCBAE"),
        border_color="#2E5240",
        focused_border_color="#6FCF97",

        # Mostra uma dica para o usuário.
        hint_text="(11) 99999-8888",

        # Teclado numérico no celular.
        keyboard_type=ft.KeyboardType.PHONE,

        # Limita a quantidade de caracteres.
        max_length=15,
    )

    # ========================================================
    # FORMATAÇÃO DO TELEFONE
    # ========================================================

    def formatar_telefone(e):
        """
        Formata automaticamente o telefone para:

        (11) 99999-8888

        O usuário pode digitar somente números.
        """

        # Remove tudo que não for número.
        numeros = re.sub(r"\D", "", telefone.value or "")

        # Limita a 11 números:
        # 2 números do DDD + 9 números do celular.
        numeros = numeros[:11]

        if len(numeros) <= 2:
            telefone.value = numeros

        elif len(numeros) <= 7:
            telefone.value = f"({numeros[:2]}) {numeros[2:]}"

        else:
            telefone.value = (
                f"({numeros[:2]}) "
                f"{numeros[2:7]}-"
                f"{numeros[7:]}"
            )

        # Atualiza somente o campo telefone.
        telefone.update()

    # Executa a formatação enquanto o usuário digita.
    telefone.on_change = formatar_telefone

    # ========================================================
    # LISTA DE CONTATOS
    # ========================================================

    lista_view = ft.ListView(
        expand=True,
        spacing=6,
        width=320
    )

    # ========================================================
    # CRIA O ITEM VISUAL DE CADA CONTATO
    # ========================================================

    def build_item(id_contato, nome_c, telefone_c):

        def excluir(e):
            # Exclui o contato pelo ID.
            conexao.execute(
                "DELETE FROM contatos WHERE id = ?",
                (id_contato,)
            )

            conexao.commit()

            # Atualiza a lista.
            atualizar_lista()

        return ft.Row(
            controls=[
                ft.Text(
                    f"{nome_c} — {telefone_c or 'sem telefone'}",
                    expand=True,
                    color="#DDF2E6"
                ),

                ft.IconButton(
                    ft.Icons.DELETE,
                    on_click=excluir,
                    icon_color="#6FCF97"
                ),
            ]
        )

    # ========================================================
    # ATUALIZA A LISTA DE CONTATOS
    # ========================================================

    def atualizar_lista():

        # Limpa a lista atual.
        lista_view.controls.clear()

        # Busca novamente os contatos diretamente no banco.
        cursor = conexao.execute(
            """
            SELECT id, nome, telefone
            FROM contatos
            ORDER BY nome
            """
        )

        # Adiciona cada contato à tela.
        for id_c, nome_c, telefone_c in cursor.fetchall():

            lista_view.controls.append(
                build_item(
                    id_c,
                    nome_c,
                    telefone_c
                )
            )

        page.update()

    # ========================================================
    # SALVAR CONTATO
    # ========================================================

    def salvar(e):

        # --------------------------------------------
        # VALIDAÇÃO DO NOME
        # --------------------------------------------

        if not nome.value or not nome.value.strip():

            nome.error_text = "Informe o nome"

            page.update()

            return

        nome.error_text = None

        # --------------------------------------------
        # VALIDAÇÃO DO TELEFONE
        # --------------------------------------------

        # Retira máscara e deixa somente números.
        numero = re.sub(
            r"\D",
            "",
            telefone.value or ""
        )

        # Se o usuário informou telefone,
        # verifica se possui exatamente 11 números.
        if numero and len(numero) != 11:

            telefone.error_text = (
                "Informe um celular com 11 números. "
                "Ex.: (11) 99999-8888"
            )

            page.update()

            return

        telefone.error_text = None

        # --------------------------------------------
        # SALVA NO BANCO
        # --------------------------------------------

        conexao.execute(
            """
            INSERT INTO contatos (nome, telefone)
            VALUES (?, ?)
            """,
            (
                nome.value.strip(),
                telefone.value
            )
        )

        conexao.commit()

        # Limpa os campos depois de salvar.
        nome.value = ""
        telefone.value = ""

        # Atualiza a lista.
        atualizar_lista()

    # ========================================================
    # LAYOUT
    # ========================================================

    page.add(

        # Column coloca os campos um abaixo do outro.
        ft.Column(
            controls=[
                nome,
                telefone,

                ft.ElevatedButton(
                    "Salvar",
                    on_click=salvar,
                    bgcolor="#6FCF97",
                    color="#0F2019",
                    width=280
                ),
            ],

            # Centraliza os campos.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            # Espaçamento entre os controles.
            spacing=10,
        ),

        # Lista dos contatos cadastrados.
        lista_view,
    )

    # Exibe os contatos já existentes
    # assim que o aplicativo é aberto.
    atualizar_lista()


# ============================================================
# INICIA O APLICATIVO
# ============================================================

ft.run(main)

```

> **Quando usar cada persistência?** `shared_preferences` para poucos valores simples (preferências, tokens, favoritos); `sqlite3` para dados estruturados/relacionais e volumosos; e, para sincronizar entre dispositivos/usuários, seria necessário um backend na nuvem (Firebase, Supabase, uma API própria) — fora do escopo desta aula, mas o caminho seria repetir o que fizemos nos Blocos 4–6 (requisições HTTP), só que salvando de fato no servidor.

---

## Bloco 9 — Recursos de hardware: visão geral

O Flet acessa recursos do dispositivo por meio de **pacotes de extensão** (`pip install flet-<recurso>`), controles não-visuais adicionados a `page.services`. Como testar de verdade exige um celular físico ou emulador configurado, tratamos este bloco como uma visão geral — os desafios de hoje são opcionais/demonstrativos.

| Recurso | Pacote | Ideia geral |
|---|---|---|
| Localização/GPS | `flet-geolocator` | Pedir permissão e ler latitude/longitude |
| Câmera/Galeria | `ft.FilePicker` (nativo do Flet) | Escolher/tirar uma foto |
| Áudio | `flet-audio` | Tocar arquivos de áudio |
| Vídeo | `flet-video` | Reproduzir vídeos |

Exemplo (demonstrativo) de localização:

```python
import flet as ft
import flet_geolocator as fg
import httpx


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Meu Endereço"

    # Cor de fundo da página inteira: azul petróleo escuro
    page.bgcolor = "#101B2D"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding de 60px no topo (fora da área do notch/status bar em celular real) e na base
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    geo = fg.Geolocator()
    page.services.append(geo)  # controles não-visuais (serviços) vão em page.services

    botao = ft.ElevatedButton("Obter meu endereço", bgcolor="#4C8BF5", color="#0B1622")

    # Cartão de resultado: começa invisível e só aparece depois que o endereço chega
    cartao_endereco = ft.Container(visible=False)

    def linha(rotulo: str, valor: str | None) -> ft.Row:
        # Monta uma linha "Rótulo: valor" reutilizável para cada campo do endereço
        return ft.Row(
            controls=[
                ft.Text(rotulo, color="#7F9BC2", width=90),
                ft.Text(valor or "-", color="#E8F0FB", expand=True),
            ]
        )

    async def obter_local(e):
        botao.disabled = True
        cartao_endereco.visible = False
        page.update()

        # 1) Pede permissão e lê a posição atual (lat/lon) do dispositivo
        await geo.request_permission()
        posicao = await geo.get_current_position()

        # 2) Geocodificação reversa: converte lat/lon em endereço, usando o
        #    serviço gratuito Nominatim (OpenStreetMap) — não exige chave de API
        async with httpx.AsyncClient() as client:
            resposta = await client.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"format": "jsonv2", "lat": posicao.latitude, "lon": posicao.longitude},
                headers={"User-Agent": "meu-app-flet/1.0"},  # o Nominatim exige um User-Agent identificável
            )
            dados = resposta.json()

        # O Nominatim já devolve o endereço quebrado em campos, dentro de "address"
        endereco = dados.get("address", {})

        rua = endereco.get("road")
        numero = endereco.get("house_number")
        rua_numero = f"{rua}, {numero}" if rua and numero else (rua or "-")

        bairro = endereco.get("suburb") or endereco.get("neighbourhood")
        cidade = endereco.get("city") or endereco.get("town") or endereco.get("village")
        estado = endereco.get("state")
        cep = endereco.get("postcode")
        pais = endereco.get("country")

        # 3) Monta o cartão com uma linha para cada campo do endereço
        cartao_endereco.content = ft.Column(
            spacing=6,
            controls=[
                ft.Text("Endereço encontrado", size=16, weight=ft.FontWeight.BOLD, color="#4C8BF5"),
                linha("Rua", rua_numero),
                linha("Bairro", bairro),
                linha("Cidade", cidade),
                linha("Estado", estado),
                linha("CEP", cep),
                linha("País", pais),
            ],
        )
        cartao_endereco.visible = True

        botao.disabled = False
        page.update()

    botao.on_click = obter_local

    # ft.Row centraliza o botão sozinho na largura da página
    page.add(
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[botao]),
        cartao_endereco,
    )


ft.run(main)
```

Exemplo (demonstrativo) de escolha de imagem da galeria com `FilePicker`. Repare que, na versão atual do Flet, `pick_files()` é assíncrono e **devolve a lista de arquivos diretamente** (não usa mais um evento `on_result` separado):

```python
import flet as ft


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Escolher Foto"

    # Cor de fundo da página inteira: azul-roxo escuro (mesma família da Aula 1)
    page.bgcolor = "#1B1F3B"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding de 60px no topo (fora da área do notch/status bar em celular real) e na base
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    seletor = ft.FilePicker()
    page.services.append(seletor)  # FilePicker também é um "serviço"

    # Placeholder exibido antes de escolher qualquer foto: um quadrado com ícone,
    # do mesmo tamanho final da imagem, para o layout não "pular" quando ela chegar
    placeholder = ft.Container(
        width=200,
        height=200,
        border_radius=16,
        bgcolor="#232A4D",
        alignment=ft.Alignment.CENTER,   # <-- era ft.alignment.center (minúsculo)
        content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=48, color="#5C7CFA"),
    )

    coluna_imagem = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza a imagem/placeholder
        controls=[placeholder],
    )

    async def escolher_foto(e):
        arquivos = await seletor.pick_files(file_type=ft.FilePickerFileType.IMAGE)
        if arquivos:
            # arquivos[0].path aponta para o arquivo escolhido no dispositivo.
            # Envolvemos a Image num Container com border_radius + clip_behavior
            # para os cantos arredondados também "cortarem" a foto (senão a
            # imagem fica quadrada por dentro de uma moldura arredondada)
            coluna_imagem.controls = [
                ft.Container(
                    width=200,
                    height=200,
                    border_radius=16,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(src=arquivos[0].path, width=200, height=200, fit=ft.BoxFit.COVER),
                )
            ]
            page.update()

    # ft.Row centraliza o botão sozinho na largura da página
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(
                    "Escolher foto",
                    icon=ft.Icons.PHOTO_LIBRARY,
                    on_click=escolher_foto,
                    bgcolor="#5C7CFA",
                    color="#161B33",
                )
            ],
        ),
        coluna_imagem,
    )


ft.run(main)
```

> **Para se aprofundar em casa:** documentação oficial em `docs.flet.dev`, seção de cada pacote (`geolocator`, `audio`, `video`, etc.) tem exemplos completos e testáveis.

---

## Bloco 10 — Projeto final guiado: App de Tarefas Online

### Especificação

Evolução do App de Tarefas da Aula 1 — que já tem busca por título, ordenação por prioridade, edição de tarefas e o contador de concluídas. Hoje, mantemos **todos** esses recursos e acrescentamos:

1. **Carregamento inicial:** ao abrir o app, tenta carregar as tarefas salvas localmente (`shared_preferences`, como JSON). Se não houver nada salvo (primeiro uso), busca 8 tarefas iniciais na API (`GET /todos?_limit=8`) e já salva localmente.
2. **Nova tarefa:** ao salvar, envia `POST` para a API (simulada) e, independentemente da resposta, adiciona a tarefa à lista local com um novo id e **salva localmente** — para realmente persistir entre usos do app, já que a API de testes não guarda os dados de verdade.
3. **Editar tarefa:** ao salvar as alterações, envia `PUT` para a API (simulada), atualiza a tarefa local e salva.
4. **Concluir/desmarcar:** ao mudar o `Checkbox`, envia `PATCH` para a API (simulado) e salva localmente.
5. **Excluir:** confirma com `AlertDialog`, envia `DELETE` para a API (simulado), remove localmente e salva.
6. Indicador de carregamento (`ProgressRing`) durante o carregamento inicial; `SnackBar` para erros de rede (o app continua funcionando offline, só com a persistência local, mesmo se a API falhar).

### Pontos-chave de implementação

- Guardamos as tarefas em `tasks: list[dict]`, exatamente como na Aula 1, **mais** uma função `salvar_local()` (chama `page.shared_preferences.set`) chamada sempre que `tasks` muda.
- A busca e a ordenação por prioridade continuam vivendo em uma única função auxiliar, `tarefas_visiveis()` — nada muda aí, ela só passa a operar sobre dados vindos da API/armazenamento local em vez de uma lista fixa no código.
- A edição reaproveita o mesmo formulário de nova tarefa (`view_nova(task=None)`), exatamente como fizemos na Aula 1, agora também sincronizando com a API via `PUT`.
- Como `main()` agora precisa de `await` logo na abertura do app (para carregar dados salvos), declaramos `async def main(page: ft.Page):` — funciona normalmente com `ft.run(main)`.
- Erros de rede **não travam o app**: cada chamada HTTP tem seu próprio `try/except`, e o app sempre confia na cópia local como fonte de verdade da tela.

### Código completo

```python
import json
import flet as ft
import httpx

# Endpoint da API de tarefas (simulada: aceita POST/PUT/PATCH/DELETE, mas não
# persiste de verdade no servidor — por isso combinamos com persistência local)
API = "https://jsonplaceholder.typicode.com/todos"

# Chave usada no armazenamento local (shared_preferences) para guardar a lista de tarefas
CHAVE_LOCAL = "app_tarefas_online.lista"

# Cores de prioridade (a mesma paleta usada na Aula 1, para manter a identidade visual do app)
PRIORITY_COLOR = {"alta": "#FF6B6B", "media": "#F2C94C", "baixa": "#6FCF97"}
PRIORITY_LABEL = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}

# Ordem numérica de prioridade, usada para ordenar a lista (alta -> média -> baixa)
PRIORITY_ORDER = {"alta": 0, "media": 1, "baixa": 2}

# Cores de fundo, uma para cada tela do app (mesma paleta azul/roxa escura da Aula 1)
BG_LISTA = "#161B33"
BG_NOVA = "#241B3D"
BG_DETALHE = "#1B2E3D"
BG_DESTAQUE = "#5C7CFA"  # cor de destaque (botões, ícones) usada nas 3 telas


# Repare que main() agora é "async def": precisamos de "await" logo na abertura
# do app, para tentar carregar as tarefas salvas localmente antes de desenhar a tela.
async def main(page: ft.Page):
    page.title = "App de Tarefas Online"

    # ---------- Estado do app ----------
    tasks: list[dict] = []            # fonte de verdade das tarefas (preenchida em carregar_inicial)
    next_id = [1]                     # próximo id local a usar ao criar uma tarefa
    search_query = [""]               # termo de busca atual, usado para filtrar a lista
    carregando = ft.ProgressRing(visible=True, color=BG_DESTAQUE)  # indicador do carregamento inicial

    # ---------- Persistência local (shared_preferences) ----------
    async def salvar_local():
        # Sempre que "tasks" muda, guardamos a lista inteira como uma única string JSON
        await page.shared_preferences.set(CHAVE_LOCAL, json.dumps(tasks))

    async def carregar_inicial():
        # 1) Tenta carregar o que já foi salvo localmente em usos anteriores
        texto = await page.shared_preferences.get(CHAVE_LOCAL)
        if texto:
            tasks.extend(json.loads(texto))
            next_id[0] = max((t["id"] for t in tasks), default=0) + 1
        else:
            # 2) Primeiro uso: não há nada salvo ainda, então buscamos 8 tarefas na API
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resposta = await client.get(API, params={"_limit": 8})
                    resposta.raise_for_status()
                    dados = resposta.json()
                for i, item in enumerate(dados, start=1):
                    tasks.append(
                        {
                            "id": i,
                            "title": item["title"],
                            "description": "Tarefa importada da API.",
                            "priority": "media",
                            "done": item["completed"],
                        }
                    )
                next_id[0] = len(tasks) + 1
                await salvar_local()  # já grava localmente, para não depender da API nas próximas vezes
            except httpx.HTTPError:
                page.show_dialog(ft.SnackBar(ft.Text("Sem conexão — iniciando com lista vazia.")))
        carregando.visible = False
        page.update()

    # ---------- Helper de dados: busca + ordenação (igual à Aula 1) ----------
    def tarefas_visiveis() -> list[dict]:
        """Retorna as tarefas filtradas pelo texto de busca (por título) e
        ordenadas por prioridade: alta -> média -> baixa."""
        termo = search_query[0].strip().lower()
        filtradas = [t for t in tasks if termo in t["title"].lower()]
        return sorted(filtradas, key=lambda t: PRIORITY_ORDER[t["priority"]])

    # ---------- Tela: Lista de tarefas ----------
    def build_task_row(t: dict, atualizar_contador) -> ft.Container:
        def ir_para_detalhe(e):
            page.navigate(f"/tarefa/{t['id']}")

        titulo = ft.Text(
            t["title"],
            expand=True,
            color="#6E7695" if t["done"] else "#E9ECFB",
        )

        async def alternar_concluida(e):
            t["done"] = e.control.value
            # Atualiza a cor do título e o contador imediatamente na tela...
            titulo.color = "#6E7695" if t["done"] else "#E9ECFB"
            atualizar_contador()
            page.update()
            # ...e só então persiste: primeiro localmente (sempre funciona)...
            await salvar_local()
            # ...depois tenta sincronizar com a API (melhor esforço: se falhar,
            # o dado local já está correto e o app continua funcionando offline)
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    await client.patch(f"{API}/{t['id']}", json={"completed": t["done"]})
            except httpx.HTTPError:
                pass

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
        # Texto do contador "X de Y tarefas concluídas"
        contador_text = ft.Text(color="#8892C4", size=13)

        def atualizar_contador():
            concluidas = sum(1 for t in tasks if t["done"])
            total = len(tasks)
            contador_text.value = f"{concluidas} de {total} tarefas concluídas"

        lista_view = ft.ListView(expand=True, spacing=8, width=340)

        def atualizar_lista():
            # Reconstrói as linhas com base no texto de busca atual + ordenação por prioridade
            lista_view.controls.clear()
            for t in tarefas_visiveis():
                lista_view.controls.append(build_task_row(t, atualizar_contador))
            page.update()

        def on_search_change(e):
            search_query[0] = e.control.value
            atualizar_lista()

        campo_busca = ft.TextField(
            label="Buscar por título",
            value=search_query[0],
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
            prefix_icon=ft.Icons.SEARCH,
            on_change=on_search_change,
        )

        # Preenche contador e lista pela primeira vez
        atualizar_contador()
        for t in tarefas_visiveis():
            lista_view.controls.append(build_task_row(t, atualizar_contador))

        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Minhas Tarefas")),
            bgcolor=BG_LISTA,  # cor de fundo desta tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza a lista
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                carregando,     # ProgressRing: visível só durante o carregamento inicial da API
                contador_text,
                campo_busca,
                lista_view,
            ],
            floating_action_button=ft.FloatingActionButton(
                icon=ft.Icons.ADD, on_click=lambda e: page.navigate("/nova"), bgcolor=BG_DESTAQUE
            ),
        )

    # ---------- Tela: Nova tarefa / Editar tarefa ----------
    def view_nova(task: dict | None = None) -> ft.View:
        # Se "task" for passado, esta tela funciona em modo edição, reaproveitando
        # o mesmo formulário usado para criar uma tarefa nova (padrão da Aula 1).
        editando = task is not None

        titulo = ft.TextField(
            label="Título", width=300, color="#FFFFFF",
            value=task["title"] if editando else "",
            label_style=ft.TextStyle(color="#B7A9E0"), border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )
        descricao = ft.TextField(
            label="Descrição", multiline=True, min_lines=3, width=300, color="#FFFFFF",
            value=task["description"] if editando else "",
            label_style=ft.TextStyle(color="#B7A9E0"), border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
        )
        prioridade = ft.RadioGroup(
            value=task["priority"] if editando else "media",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(value="alta", label="Alta", label_style=ft.TextStyle(color="#D8CFF2"), fill_color=BG_DESTAQUE),
                    ft.Radio(value="media", label="Média", label_style=ft.TextStyle(color="#D8CFF2"), fill_color=BG_DESTAQUE),
                    ft.Radio(value="baixa", label="Baixa", label_style=ft.TextStyle(color="#D8CFF2"), fill_color=BG_DESTAQUE),
                ]
            ),
        )

        async def salvar(e):
            if not titulo.value:
                titulo.error_text = "Informe um título"
                page.update()
                return

            if editando:
                # Atualiza a tarefa existente in-place (mesmo dicionário usado na lista/detalhe)
                task["title"] = titulo.value
                task["description"] = descricao.value or ""
                task["priority"] = prioridade.value
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        await client.put(
                            f"{API}/{task['id']}",
                            json={"title": task["title"], "completed": task["done"], "userId": 1},
                        )
                except httpx.HTTPError:
                    pass  # a tarefa já foi atualizada localmente de qualquer forma
                await salvar_local()
                page.navigate(f"/tarefa/{task['id']}")
                page.show_dialog(ft.SnackBar(ft.Text("Tarefa atualizada com sucesso!")))
            else:
                nova_tarefa = {
                    "id": next_id[0],
                    "title": titulo.value,
                    "description": descricao.value or "",
                    "priority": prioridade.value,
                    "done": False,
                }
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        await client.post(API, json={"title": titulo.value, "completed": False, "userId": 1})
                except httpx.HTTPError:
                    pass  # a tarefa é salva localmente de qualquer forma
                tasks.append(nova_tarefa)
                next_id[0] += 1
                await salvar_local()
                page.navigate("/")
                page.show_dialog(ft.SnackBar(ft.Text("Tarefa criada com sucesso!")))

        return ft.View(
            route=f"/editar/{task['id']}" if editando else "/nova",
            appbar=ft.AppBar(title=ft.Text("Editar tarefa" if editando else "Nova tarefa")),
            bgcolor=BG_NOVA,  # cor de fundo desta tela
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o formulário
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                titulo,
                descricao,
                ft.Text("Prioridade:", color="#D8CFF2"),
                prioridade,
                ft.ElevatedButton(
                    "Salvar alterações" if editando else "Salvar",
                    on_click=salvar, bgcolor=BG_DESTAQUE, color="#161B33"
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

        async def excluir_confirmado(e):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    await client.delete(f"{API}/{tarefa['id']}")
            except httpx.HTTPError:
                pass  # a tarefa é removida localmente de qualquer forma
            tasks.remove(tarefa)
            await salvar_local()
            page.pop_dialog()
            page.navigate("/")
            page.show_dialog(ft.SnackBar(ft.Text("Tarefa excluída.")))

        def cancelar(e):
            page.pop_dialog()

        def ir_para_edicao(e):
            page.navigate(f"/editar/{tarefa['id']}")

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
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            "Editar", icon=ft.Icons.EDIT, on_click=ir_para_edicao,
                            bgcolor=BG_DESTAQUE, color="#161B33",
                        ),
                        ft.ElevatedButton(
                            "Excluir", icon=ft.Icons.DELETE, on_click=lambda e: page.show_dialog(dialogo),
                            bgcolor="#FF6B6B", color="#1B2E3D",
                        ),
                    ],
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

        troute_detalhe = ft.TemplateRoute(page.route)
        if troute_detalhe.match("/tarefa/:id"):
            page.views.append(view_detalhe(int(troute_detalhe.id)))

        # Rota de edição: mantém a tela de detalhe embaixo na pilha, para que o botão
        # "voltar" do formulário retorne ao detalhe (e não direto para a lista).
        troute_editar = ft.TemplateRoute(page.route)
        if troute_editar.match("/editar/:id"):
            task_id = int(troute_editar.id)
            page.views.append(view_detalhe(task_id))
            tarefa = next((t for t in tasks if t["id"] == task_id), None)
            page.views.append(view_nova(tarefa))

        page.update()

    def view_pop(e):
        page.views.pop()
        page.navigate(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)          # desenha a tela inicial (lista vazia, com o ProgressRing visível)

    await carregar_inicial()    # busca/carrega os dados de verdade...
    route_change(None)          # ...e reconstrói a lista já com as tarefas prontas


ft.run(main)
```

---

## O que você aprendeu hoje

- Conceitos de API REST, Web Service e verbos HTTP;
- Serializar/desserializar JSON com o módulo `json`, antes mesmo de usá-lo "escondido" dentro de `resposta.json()`;
- Fazer requisições `GET`/`POST`/`PUT`/`PATCH`/`DELETE` com `httpx`, de forma assíncrona;
- Tratar erros de rede com `try/except` e dar feedback ao usuário;
- Persistir dados localmente com `shared_preferences` (chave-valor) e `sqlite3` (relacional);
- Visão geral de recursos de hardware (GPS, câmera/galeria) e do fluxo de publicação (`flet build`);
- Evoluir o App de Tarefas — mantendo busca, ordenação por prioridade, edição e o contador de concluídas da Aula 1 — para consumir uma API real e persistir dados de verdade entre usos (**App de Tarefas Online**).

## Encerramento

Com as duas aulas, o aluno percorreu o mesmo caminho do livro de referência — da interface básica até um app completo com API e persistência — só que inteiramente em Python. Próximos passos sugeridos para quem quiser continuar: gerenciadores de estado mais robustos para apps grandes, autenticação de usuários (`page.login()`), notificações push, testes automatizados de interface, e publicação nas lojas (Play Store/App Store).