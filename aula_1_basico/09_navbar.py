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