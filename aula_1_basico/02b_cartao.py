import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Perfil"

    # Cor de fundo da página inteira: azul marinho escuro
    page.bgcolor = "#0D1B2A"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    page.add(
        # Container principal: um "cartão" com largura fixa e visual arredondado
        ft.Container(
            width=300,  # largura fixa do cartão
            padding=20,  # espaçamento interno entre o conteúdo e as bordas
            bgcolor="#1B263B",  # cor de fundo do cartão (azul um pouco mais claro que o fundo)
            border_radius=16,  # arredondamento das bordas
            content=ft.Column(  # organiza os itens verticalmente, um abaixo do outro
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza tudo dentro do cartão
                controls=[
                    # Nome em destaque: tamanho maior, negrito e cor de destaque
                    ft.Text("João Pereira", size=22, weight=ft.FontWeight.BOLD, color="#48CAE4"),

                    # Cargo/função, em azul claro suave para dar menos destaque
                    ft.Text("Desenvolvedor mobile", color="#90E0EF"),

                    # Linha com ícone de e-mail + o texto do e-mail, centralizada
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.EMAIL, color="#48CAE4"),
                            ft.Text("joao@email.com", color="#E0FBFC"),
                        ],
                    ),

                    # Linha com ícone de telefone + o texto do telefone, centralizada
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.PHONE, color="#48CAE4"),
                            ft.Text("(11) 90000-0000", color="#E0FBFC"),
                        ],
                    ),
                ]
            ),
        )
    )

# Inicia a aplicação, chamando a função main() como ponto de entrada
ft.run(main)