import flet as ft
import json

FILMES = ["Matrix", "Interestelar", "Cidade de Deus", "Vingadores", "Coringa"]
CHAVE = "app_favoritos.filmes"


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Filmes favoritos"

    # Cor de fundo da página inteira: roxo escuro
    page.bgcolor = "#241E3D"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    checkboxes = {}  # nome do filme -> Checkbox correspondente

    async def carregar_favoritos():
        # Lê o JSON salvo (se existir) e marca os checkboxes já favoritados
        texto = await page.shared_preferences.get(CHAVE)
        favoritos = json.loads(texto) if texto else []
        for filme, caixa in checkboxes.items():
            caixa.value = filme in favoritos
        page.update()

    async def alternar(e):
        # Sempre que qualquer checkbox muda, recalcula a lista inteira de favoritos e salva
        favoritos = [filme for filme, caixa in checkboxes.items() if caixa.value]
        await page.shared_preferences.set(CHAVE, json.dumps(favoritos))

    for filme in FILMES:
        checkboxes[filme] = ft.Checkbox(
            label=filme, on_change=alternar,
            active_color="#B388EB", label_style=ft.TextStyle(color="#D8CFF2"),
        )

    page.add(
        ft.Text("Meus filmes favoritos", size=20, weight=ft.FontWeight.BOLD, color="#F2C94C"),
        *checkboxes.values(),
    )
    page.run_task(carregar_favoritos)  # dispara a carga assíncrona assim que o app inicia


ft.run(main)