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