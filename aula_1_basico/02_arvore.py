import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Árvore de controles"

    # Cor de fundo da página: verde-azulado escuro (teal)
    page.bgcolor = "#16BA4A"

    # Define o tamanho da tela
    page.window.width = 320
    page.window.height = 600

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Container principal que representa o "cartão" visual
    cartao = ft.Container(
        # Conteúdo do cartão organizado em coluna (um item embaixo do outro)
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza o conteúdo dentro do cartão
            controls=[
                # Título do cartão: texto maior, negrito e cor de destaque
                ft.Text(
                    "Título do cartão",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1FE0C4",
                ),
                # Texto descritivo (abaixo  do título)
                ft.Text("Descrição do cartão", color="#CFEFE9"),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            "Ação 1",
                            bgcolor="#1FE0C4",
                            color="#0B3D3A",
                        ), # Botão de destaque
                        ft.OutlinedButton("Ação 2"), # Botão secundário
                    ]
                ),
            ]
        ),
        padding=16, # Espaçamento interno entre o conteudo
        bgcolor="#123C3C", # Cor de fundo ("Row" - Arranjo em linha)
        border_radius=12, # Arredondamento de canto
    )
    # Adiciona o cartão à página
    page.add(cartao)

ft.run(main)


