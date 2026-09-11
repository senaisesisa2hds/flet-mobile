import flet as ft

def main(page: ft.Page):
    page.title = "Meu primeiro app flet"
    page.add(ft.Text("Olá, mundo!!"))

ft.run(main)