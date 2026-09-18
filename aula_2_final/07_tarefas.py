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