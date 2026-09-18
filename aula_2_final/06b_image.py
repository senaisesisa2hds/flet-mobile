import flet as ft


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Escolher Foto"

    # Cor de fundo da página inteira: azul-roxo escuro (mesma família da Aula 1)
    page.bgcolor = "#1B1F3B"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding de 60px no topo (fora da área do notch/status bar em celular real) e na base
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    seletor = ft.FilePicker()
    page.services.append(seletor)  # FilePicker também é um "serviço"

    # Placeholder exibido antes de escolher qualquer foto: um quadrado com ícone,
    # do mesmo tamanho final da imagem, para o layout não "pular" quando ela chegar
    placeholder = ft.Container(
        width=200,
        height=200,
        border_radius=16,
        bgcolor="#232A4D",
        alignment=ft.Alignment.CENTER,   # <-- era ft.alignment.center (minúsculo)
        content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=48, color="#5C7CFA"),
    )

    coluna_imagem = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza a imagem/placeholder
        controls=[placeholder],
    )

    async def escolher_foto(e):
        arquivos = await seletor.pick_files(file_type=ft.FilePickerFileType.IMAGE)
        if arquivos:
            # arquivos[0].path aponta para o arquivo escolhido no dispositivo.
            # Envolvemos a Image num Container com border_radius + clip_behavior
            # para os cantos arredondados também "cortarem" a foto (senão a
            # imagem fica quadrada por dentro de uma moldura arredondada)
            coluna_imagem.controls = [
                ft.Container(
                    width=200,
                    height=200,
                    border_radius=16,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(src=arquivos[0].path, width=200, height=200, fit=ft.BoxFit.COVER),
                )
            ]
            page.update()

    # ft.Row centraliza o botão sozinho na largura da página
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(
                    "Escolher foto",
                    icon=ft.Icons.PHOTO_LIBRARY,
                    on_click=escolher_foto,
                    bgcolor="#5C7CFA",
                    color="#161B33",
                )
            ],
        ),
        coluna_imagem,
    )


ft.run(main)