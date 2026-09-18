import os
import sqlite3
import re
import flet as ft


# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================

# Define onde o banco de dados será armazenado.
# No celular, o Flet utiliza a pasta própria de armazenamento do aplicativo.
pasta_dados = os.environ.get("FLET_APP_STORAGE_DATA", ".")

# Nome e caminho do banco de dados.
caminho_bd = os.path.join(pasta_dados, "contatos.db")


def main(page: ft.Page):

    # ========================================================
    # CONFIGURAÇÃO DA PÁGINA
    # ========================================================

    # Título que aparece na barra da janela/aba.
    page.title = "Contatos (SQLite)"

    # Cor de fundo da página inteira.
    page.bgcolor = "#0F2019"

    # Centraliza os controles horizontalmente.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Espaçamento interno da página.
    page.padding = ft.Padding(
        top=60,
        bottom=60,
        left=20,
        right=20
    )

    # ========================================================
    # BANCO DE DADOS
    # ========================================================

    # Abre ou cria o banco de dados.
    conexao = sqlite3.connect(caminho_bd)

    # Cria a tabela caso ela ainda não exista.
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT
        )
        """
    )

    conexao.commit()

    # ========================================================
    # CAMPOS DO FORMULÁRIO
    # ========================================================

    nome = ft.TextField(
        label="Nome",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#9FCBAE"),
        border_color="#2E5240",
        focused_border_color="#6FCF97",
    )

    telefone = ft.TextField(
        label="Telefone",
        width=280,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#9FCBAE"),
        border_color="#2E5240",
        focused_border_color="#6FCF97",

        # Mostra uma dica para o usuário.
        hint_text="(11) 99999-8888",

        # Teclado numérico no celular.
        keyboard_type=ft.KeyboardType.PHONE,

        # Limita a quantidade de caracteres.
        max_length=15,
    )

    # ========================================================
    # FORMATAÇÃO DO TELEFONE
    # ========================================================

    def formatar_telefone(e):
        """
        Formata automaticamente o telefone para:

        (11) 99999-8888

        O usuário pode digitar somente números.
        """

        # Remove tudo que não for número.
        numeros = re.sub(r"\D", "", telefone.value or "")

        # Limita a 11 números:
        # 2 números do DDD + 9 números do celular.
        numeros = numeros[:11]

        if len(numeros) <= 2:
            telefone.value = numeros

        elif len(numeros) <= 7:
            telefone.value = f"({numeros[:2]}) {numeros[2:]}"

        else:
            telefone.value = (
                f"({numeros[:2]}) "
                f"{numeros[2:7]}-"
                f"{numeros[7:]}"
            )

        # Atualiza somente o campo telefone.
        telefone.update()

    # Executa a formatação enquanto o usuário digita.
    telefone.on_change = formatar_telefone

    # ========================================================
    # LISTA DE CONTATOS
    # ========================================================

    lista_view = ft.ListView(
        expand=True,
        spacing=6,
        width=320
    )

    # ========================================================
    # CRIA O ITEM VISUAL DE CADA CONTATO
    # ========================================================

    def build_item(id_contato, nome_c, telefone_c):

        def excluir(e):
            # Exclui o contato pelo ID.
            conexao.execute(
                "DELETE FROM contatos WHERE id = ?",
                (id_contato,)
            )

            conexao.commit()

            # Atualiza a lista.
            atualizar_lista()

        return ft.Row(
            controls=[
                ft.Text(
                    f"{nome_c} — {telefone_c or 'sem telefone'}",
                    expand=True,
                    color="#DDF2E6"
                ),

                ft.IconButton(
                    ft.Icons.DELETE,
                    on_click=excluir,
                    icon_color="#6FCF97"
                ),
            ]
        )

    # ========================================================
    # ATUALIZA A LISTA DE CONTATOS
    # ========================================================

    def atualizar_lista():

        # Limpa a lista atual.
        lista_view.controls.clear()

        # Busca novamente os contatos diretamente no banco.
        cursor = conexao.execute(
            """
            SELECT id, nome, telefone
            FROM contatos
            ORDER BY nome
            """
        )

        # Adiciona cada contato à tela.
        for id_c, nome_c, telefone_c in cursor.fetchall():

            lista_view.controls.append(
                build_item(
                    id_c,
                    nome_c,
                    telefone_c
                )
            )

        page.update()

    # ========================================================
    # SALVAR CONTATO
    # ========================================================

    def salvar(e):

        # --------------------------------------------
        # VALIDAÇÃO DO NOME
        # --------------------------------------------

        if not nome.value or not nome.value.strip():

            nome.error_text = "Informe o nome"

            page.update()

            return

        nome.error_text = None

        # --------------------------------------------
        # VALIDAÇÃO DO TELEFONE
        # --------------------------------------------

        # Retira máscara e deixa somente números.
        numero = re.sub(
            r"\D",
            "",
            telefone.value or ""
        )

        # Se o usuário informou telefone,
        # verifica se possui exatamente 11 números.
        if numero and len(numero) != 11:

            telefone.error_text = (
                "Informe um celular com 11 números. "
                "Ex.: (11) 99999-8888"
            )

            page.update()

            return

        telefone.error_text = None

        # --------------------------------------------
        # SALVA NO BANCO
        # --------------------------------------------

        conexao.execute(
            """
            INSERT INTO contatos (nome, telefone)
            VALUES (?, ?)
            """,
            (
                nome.value.strip(),
                telefone.value
            )
        )

        conexao.commit()

        # Limpa os campos depois de salvar.
        nome.value = ""
        telefone.value = ""

        # Atualiza a lista.
        atualizar_lista()

    # ========================================================
    # LAYOUT
    # ========================================================

    page.add(

        # Column coloca os campos um abaixo do outro.
        ft.Column(
            controls=[
                nome,
                telefone,

                ft.ElevatedButton(
                    "Salvar",
                    on_click=salvar,
                    bgcolor="#6FCF97",
                    color="#0F2019",
                    width=280
                ),
            ],

            # Centraliza os campos.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            # Espaçamento entre os controles.
            spacing=10,
        ),

        # Lista dos contatos cadastrados.
        lista_view,
    )

    # Exibe os contatos já existentes
    # assim que o aplicativo é aberto.
    atualizar_lista()


# ============================================================
# INICIA O APLICATIVO
# ============================================================

ft.run(main)