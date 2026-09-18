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