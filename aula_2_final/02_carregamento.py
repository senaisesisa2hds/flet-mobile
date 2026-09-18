import flet as ft
import httpx


def main(page: ft.Page):
    # Título que aparece na barra da janela/aba
    page.title = "Tarefas da API"

    # Cor de fundo da página inteira: verde-azulado bem escuro (teal)
    page.bgcolor = "#0B2027"

    # Centraliza os controles no eixo horizontal da página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    lista_view = ft.ListView(expand=True, spacing=6, width=320)
    progresso = ft.ProgressRing(visible=False, color="#2EC4B6")  # some/aparece durante o carregamento
    botao = ft.ElevatedButton("Carregar tarefas", bgcolor="#2EC4B6", color="#0B2027")

    async def carregar(e):
        # Mostra o indicador e desabilita o botão ANTES de iniciar a requisição
        botao.disabled = True
        progresso.visible = True
        lista_view.controls.clear()
        page.update()  # aplica essas mudanças na tela já, antes de aguardar a rede

        async with httpx.AsyncClient() as client:
            resposta = await client.get(
                "https://jsonplaceholder.typicode.com/todos", params={"_limit": 10}
            )
            dados = resposta.json()

        for tarefa in dados:
            lista_view.controls.append(ft.Text(f"• {tarefa['title']}", color="#CFF4F0"))

        # Restaura o botão e some com o indicador, agora que os dados já chegaram
        botao.disabled = False
        progresso.visible = False
        page.update()

    botao.on_click = carregar
    page.add(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[botao, progresso]), lista_view)


ft.run(main)