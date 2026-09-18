import flet as ft

def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Avaliação"

    # Cor de fundo da página inteira: marrom escuro (combina bem com dourado das estrelas)
    page.bgcolor = "#2B2118"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Texto que mostra a nota atual
    nota = ft.Text("Sua nota: 0/5", color="#F2C94C", size=16)
    estrelas = []  # lista que guardará os 5 IconButton das estrelas

    def avaliar(indice):
        # Função geradora: cria e devolve um handler que "lembra" o índice da estrela
        # (evita o bug de closure tardio em laços — veremos em detalhe no Bloco 7)
        def handler(e):
            for i, botao in enumerate(estrelas):
                botao.icon = ft.Icons.STAR if i <= indice else ft.Icons.STAR_BORDER
            nota.value = f"Sua nota: {indice + 1}/5"
            page.update()
        return handler

    # Cria as 5 estrelas, cada uma com sua própria cor dourada
    for i in range(5):
        estrelas.append(
            ft.IconButton(ft.Icons.STAR_BORDER, on_click=avaliar(i), icon_color="#F2C94C")
        )

    page.add(
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=estrelas),  # estrelas centralizadas
        nota,
    )

ft.run(main)