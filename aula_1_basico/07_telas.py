import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Navegação"

    def view_inicio():
        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Início")),
            bgcolor="#221A3D",  # cor de fundo desta tela: roxo escuro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o conteúdo
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),  # padding vertical de 60px
            controls=[
                ft.Text("Tela inicial", color="#C9B6F2", size=18),
                ft.ElevatedButton(
                    "Ir para Sobre",
                    on_click=lambda e: page.navigate("/sobre"),
                    bgcolor="#9B7EDE",
                    color="#221A3D",
                ),
            ],
        )

    def view_sobre():
        return ft.View(
            route="/sobre",
            appbar=ft.AppBar(title=ft.Text("Sobre")),
            bgcolor="#1A2E3D",  # cor de fundo desta tela: azul petróleo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.Padding(top=60, bottom=60, left=0, right=0),
            controls=[ft.Text("Esta é a tela Sobre.", color="#9FD3E8")],
        )

    def route_change(e):
        # Reconstrói a pilha de views a partir da rota atual
        page.views.clear()
        page.views.append(view_inicio())
        if page.route == "/sobre":
            page.views.append(view_sobre())
        page.update()

    def view_pop(e):
        page.views.pop()
        page.navigate(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)  # constrói a(s) view(s) da rota inicial

ft.run(main)