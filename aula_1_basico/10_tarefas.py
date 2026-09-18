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