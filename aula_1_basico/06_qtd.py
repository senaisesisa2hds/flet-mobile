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