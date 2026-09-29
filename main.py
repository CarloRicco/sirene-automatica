import sys
import json
import os
import winsound
import wave
from copy import deepcopy
from datetime import datetime, timedelta

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# =============================================================
# JANELA DE HORÁRIOS ESPECIAIS
# =============================================================

class JanelaExcecoes(QDialog):

    def __init__(
        self,
        parent=None,
        configuracoes=None
    ):

        super().__init__(parent)

        self.setObjectName("janela_excecoes")

        self.configuracoes = configuracoes or {}
        

        # =========================================================
        # JANELA SEM BARRA NATIVA DO WINDOWS
        # =========================================================

        self.setWindowFlags(
            Qt.Dialog |
            Qt.FramelessWindowHint
        )

        # =========================================================
        # BARRA DE TÍTULO PERSONALIZADA
        # =========================================================

        barra_titulo = QWidget()

        barra_titulo.setObjectName(
            "barra_titulo_excecoes"
        )

        barra_titulo.mousePressEvent = self._barra_mouse_press
        barra_titulo.mouseMoveEvent = self._barra_mouse_move
        barra_titulo.mouseReleaseEvent = self._barra_mouse_release

        barra_titulo.setFixedHeight(
            44
        )

        layout_barra = QHBoxLayout(
            barra_titulo
        )

        layout_barra.setContentsMargins(
            16,
            0,
            8,
            0
        )

        layout_barra.setSpacing(
            4
        )

        titulo_barra = QLabel(
            "🔔 Horários Especiais"
        )

        titulo_barra.setObjectName(
            "titulo_barra_excecoes"
        )

        layout_barra.addWidget(
            titulo_barra
        )

        layout_barra.addStretch()

        botao_fechar = QPushButton(
            "×"
        )

        botao_fechar.setObjectName(
            "botao_fechar_excecoes"
        )

        botao_fechar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }

            QPushButton:hover {
                background-color: #e04b3f;
            }

            QPushButton:pressed {
                background-color: #962d22;
            }
        """)

        botao_fechar.setFixedSize(
            36,
            36
        )

        botao_fechar.clicked.connect(
            self.reject
        )

        layout_barra.addWidget(
            botao_fechar
        )

        self.setMinimumSize(
            760,
            620
        )

        self.resize(
            760,
            620
        )


        # =====================================================
        # ESTILO DA JANELA
        # =====================================================

        self.setStyleSheet("""
            QDialog#janela_excecoes {
                background-color: #0b1424;
                color: #f2f5f9;
            }

            QWidget#barra_titulo_excecoes {
                background-color: #16243a;
                border-bottom: 1px solid #29415f;
            }

            QLabel#titulo_barra_excecoes {
                color: #f2f5f9;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#botao_fechar_excecoes {
                background-color: transparent;
                color: #f2f5f9;
                border: none;
                border-radius: 6px;
                font-family: "Segoe UI";
                font-size: 22px;
                font-weight: 400;
            }

            QPushButton#botao_fechar_excecoes:hover {
                background-color: #c0392b;
                color: white;
            }

            QPushButton#botao_fechar_excecoes:pressed {
                background-color: #962d22;
            }


            QLabel {
                color: #dbe4ef;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel#rotulo_campo_excecao {
                color: #8fa6c2;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }
            QLabel#rotulo_data_excecao {
                color: #8fa6c2;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.3px;
            }

            QLabel#titulo_excecao {
                color: #ffffff;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
                padding-bottom: 2px;
            }

            QLabel#descricao_excecao {
                color: #8fa6c2;
                font-family: "Segoe UI";
                font-size: 13px;
                padding-top: 0px;
                padding-bottom: 0px;
            }

            

            QLabel#titulo_excecao_turno {
                color: #ffffff;
                background-color: #16243a;
                border: 1px solid #263d5d;
                border-left: 4px solid #2196e0;
                border-radius: 8px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
                padding: 9px 12px;
                margin-top: 4px;
            }

            QFrame#painel_turno_excecao {
                background-color: #0f1b2d;
                border: 1px solid #263d5d;
                border-radius: 9px;
            }



                QFrame#cartao_turno {
                background-color: #111e32;
                border: 1px solid #2b4567;
                border-radius: 12px;
            }

            QFrame#cartao_turno QLabel#titulo_excecao_turno {
                background-color: #182941;
                border: 1px solid #2d496d;
                border-left: 4px solid #29a3f0;
                border-radius: 8px;
                margin-top: 0px;
                padding: 10px 12px;
            }

            QDateEdit,
            QComboBox,
            QSpinBox {
                background-color: #111d30;
                color: #f2f5f9;
                border: 1px solid #304766;
                border-radius: 7px;
                padding: 7px 10px;
                min-height: 32px;
                font-family: "Segoe UI";
                font-size: 13px;
            }

                QDateEdit {
                min-height: 38px;
                font-size: 14px;
                font-weight: 600;
                padding: 7px 12px;
                border-radius: 8px;
            }

            QDateEdit:hover,
            QComboBox:hover,
            QSpinBox:hover {
                border: 1px solid #2196e0;
            }

                QCalendarWidget {
                background-color: #111d30;
                color: #f2f5f9;
                border: 1px solid #304766;
                border-radius: 8px;
            }

            QCalendarWidget QWidget {
                alternate-background-color: #111d30;
            }

            QCalendarWidget QToolButton {
                background-color: #16243a;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #2196e0;
            }

            QCalendarWidget QSpinBox {
                background-color: #111d30;
                color: #f2f5f9;
                border: none;
            }

            QCalendarWidget QAbstractItemView {
                background-color: #111d30;
                color: #dbe4ef;
                selection-background-color: #2196e0;
                selection-color: #ffffff;
                outline: none;
            }

            QDateEdit:focus,
            QComboBox:focus,
            QSpinBox:focus {
                border: 1px solid #29a3f0;
            }

            QComboBox::drop-down {
                width: 30px;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #111d30;
                color: #f2f5f9;
                border: 1px solid #304766;
                selection-background-color: #2196e0;
                selection-color: #ffffff;
            }

            QCheckBox {
                color: #c9d5e4;
                font-family: "Segoe UI";
                font-size: 13px;
                spacing: 8px;
                padding: 2px 0px;
            }

            QCheckBox::indicator {
                width: 17px;
                height: 17px;
                border-radius: 4px;
                border: 1px solid #49627f;
                background-color: #111d30;
            }

            QCheckBox::indicator:hover {
                border: 1px solid #29a3f0;
            }

            QCheckBox::indicator:checked {
                background-color: #29a3f0;
                border: 1px solid #29a3f0;
            }

            QPushButton {
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
                padding: 0px 18px;
                border-radius: 7px;
            }

            QPushButton#botao_cancelar {
                background-color: #16243a;
                color: #b9c7d8;
                border: 1px solid #304766;
            }

            QPushButton#botao_cancelar:hover {
                background-color: #20334f;
                color: #ffffff;
                border: 1px solid #466384;
            }

            QPushButton#botao_salvar {
                background-color: #2196e0;
                color: #ffffff;
                border: 1px solid #2196e0;
            }

            QPushButton#botao_salvar:hover {
                background-color: #29a3f0;
                border: 1px solid #29a3f0;
            }

            QPushButton#botao_salvar:pressed {
                background-color: #197fbe;
            }
        """)

        layout = QVBoxLayout(self)

        layout.addWidget(
            barra_titulo
        )

        layout.setContentsMargins(
            25,
            16,
            25,
            16
        )

        layout.setSpacing(8)

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = QLabel(
            "CONFIGURAÇÃO DE HORÁRIO ESPECIAL"
        )

        titulo.setObjectName(
            "titulo_excecao"
        )

        layout.addWidget(
            titulo
        )

        descricao = QLabel(
            "Configure uma programação diferente para uma data específica."
        )

        descricao.setWordWrap(
            True
        )

        descricao.setObjectName(
            "descricao_excecao"
        )

        layout.addWidget(
            descricao
        )

        # =====================================================
        # DATA
        # =====================================================

        label_data = QLabel(
            "DATA DA EXCEÇÃO"
        )

        label_data.setObjectName(
            "rotulo_data_excecao"
        )

        layout.addWidget(
            label_data
        )

        self.data_excecao = QDateEdit()

        self.data_excecao.setCalendarPopup(
            True
        )

        self.data_excecao.setDate(
            datetime.now().date()
        )

        self.data_excecao.setDisplayFormat(
            "dd/MM/yyyy"
        )

        # ---------------------------------------------------------
        # ESTILO DO CALENDÁRIO
        # ---------------------------------------------------------
        calendario = self.data_excecao.calendarWidget()

        calendario.setStyleSheet("""
            QCalendarWidget {
                background-color: #101a2c;
                color: #e6edf7;
                border: 1px solid #263750;
            }

            QCalendarWidget QToolButton {
                background-color: #182943;
                color: #ffffff;
                border: none;
                padding: 6px;
                font-size: 10px;
                font-weight: bold;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #1d9bf0;
                color: #ffffff;
            }

            QCalendarWidget QToolButton#qt_calendar_monthbutton {
                color: #ffffff;
                font-weight: bold;
            }

            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                color: #ffffff;
                font-weight: bold;
            }

            QCalendarWidget QMenu {
                background-color: #101a2c;
                color: #e6edf7;
                border: 1px solid #263750;
                padding: 4px;
            }

            QCalendarWidget QMenu::item {
                background-color: transparent;
                color: #e6edf7;
                padding: 7px 18px;
            }

            QCalendarWidget QMenu::item:selected {
                background-color: #1d9bf0;
                color: #ffffff;
            }

            QCalendarWidget QSpinBox {
                background-color: #101a2c;
                color: #ffffff;
                border: 1px solid #263750;
            }

            QCalendarWidget QAbstractItemView {
                background-color: #101a2c;
                color: #dce6f2;
                selection-background-color: #1d9bf0;
                selection-color: #ffffff;
                border: none;
            }
        """)

        layout.addWidget(
            self.data_excecao
        )

        self.data_excecao.dateChanged.connect(
            lambda: self.carregar_excecao_existente()
        )

        self.data_excecao.dateChanged.connect(
            self.carregar_configuracao
        )

        # =====================================================
        # TURNOS
        # =====================================================

        layout_turnos = QHBoxLayout()

        layout_turnos.setSpacing(
            14
        )

        # =====================================================
        # CARTÃO MATUTINO
        # =====================================================

        cartao_matutino = QFrame()

        cartao_matutino.setObjectName(
            "cartao_turno"
        )

        layout_cartao_matutino = QVBoxLayout(
            cartao_matutino
        )

        layout_cartao_matutino.setContentsMargins(
            16,
            16,
            16,
            16
        )

        layout_cartao_matutino.setSpacing(
            12
        )

        titulo_matutino = QLabel(
            "☀  MATUTINO"
        )

        titulo_matutino.setObjectName(
            "titulo_excecao_turno"
        )

        layout_cartao_matutino.addWidget(
            titulo_matutino
        )

        self.matutino_ativo = QCheckBox(
            "Ativar turno matutino"
        )

        self.matutino_ativo.setChecked(
            True
        )

        layout_cartao_matutino.addWidget(
            self.matutino_ativo
        )

        # -----------------------------------------------------
        # DURAÇÃO MATUTINO
        # -----------------------------------------------------

        linha_duracao_matutino = QHBoxLayout()

        rotulo_duracao_matutino = QLabel(
            "Duração da aula:"
        )

        rotulo_duracao_matutino.setObjectName(
            "rotulo_campo_excecao"
        )

        self.duracao_matutino = QComboBox()

        self.duracao_matutino.addItems(
            [
                "30 minutos",
                "35 minutos",
                "40 minutos",
                "45 minutos"
            ]
        )

        self.duracao_matutino.setCurrentText(
            "30 minutos"
        )

        linha_duracao_matutino.addWidget(
            rotulo_duracao_matutino
        )

        linha_duracao_matutino.addWidget(
            self.duracao_matutino,
            1
        )

        layout_cartao_matutino.addLayout(
            linha_duracao_matutino
        )

        # -----------------------------------------------------
        # QUANTIDADE MATUTINO
        # -----------------------------------------------------

        linha_aulas_matutino = QHBoxLayout()

        rotulo_aulas_matutino = QLabel(
            "Quantidade de aulas:"
        )

        rotulo_aulas_matutino.setObjectName(
            "rotulo_campo_excecao"
        )

        self.aulas_matutino = QSpinBox()

        self.aulas_matutino.setMinimum(
            1
        )

        self.aulas_matutino.setMaximum(
            20
        )

        self.aulas_matutino.setValue(
            5
        )

        linha_aulas_matutino.addWidget(
            rotulo_aulas_matutino
        )

        linha_aulas_matutino.addWidget(
            self.aulas_matutino,
            1
        )

        layout_cartao_matutino.addLayout(
            linha_aulas_matutino
        )

        self.recreio_matutino = QCheckBox(
            "Haverá recreio"
        )

        self.recreio_matutino.setChecked(
            False
        )

        layout_cartao_matutino.addWidget(
            self.recreio_matutino
        )

        layout_turnos.addWidget(
            cartao_matutino,
            1
        )

        # =====================================================
        # CARTÃO VESPERTINO
        # =====================================================

        cartao_vespertino = QFrame()

        cartao_vespertino.setObjectName(
            "cartao_turno"
        )

        layout_cartao_vespertino = QVBoxLayout(
            cartao_vespertino
        )

        layout_cartao_vespertino.setContentsMargins(
            16,
            16,
            16,
            16
        )

        layout_cartao_vespertino.setSpacing(
            12
        )

        titulo_vespertino = QLabel(
            "☀  VESPERTINO"
        )

        titulo_vespertino.setObjectName(
            "titulo_excecao_turno"
        )

        layout_cartao_vespertino.addWidget(
            titulo_vespertino
        )

        self.vespertino_ativo = QCheckBox(
            "Ativar turno vespertino"
        )

        self.vespertino_ativo.setChecked(
            False
        )

        layout_cartao_vespertino.addWidget(
            self.vespertino_ativo
        )

        # -----------------------------------------------------
        # DURAÇÃO VESPERTINO
        # -----------------------------------------------------

        linha_duracao_vespertino = QHBoxLayout()

        rotulo_duracao_vespertino = QLabel(
            "Duração da aula:"
        )

        rotulo_duracao_vespertino.setObjectName(
            "rotulo_campo_excecao"
        )

        self.duracao_vespertino = QComboBox()

        self.duracao_vespertino.addItems(
            [
                "30 minutos",
                "35 minutos",
                "40 minutos",
                "45 minutos"
            ]
        )

        self.duracao_vespertino.setCurrentText(
            "30 minutos"
        )

        linha_duracao_vespertino.addWidget(
            rotulo_duracao_vespertino
        )

        linha_duracao_vespertino.addWidget(
            self.duracao_vespertino,
            1
        )

        layout_cartao_vespertino.addLayout(
            linha_duracao_vespertino
        )

        # -----------------------------------------------------
        # QUANTIDADE VESPERTINO
        # -----------------------------------------------------

        linha_aulas_vespertino = QHBoxLayout()

        rotulo_aulas_vespertino = QLabel(
            "Quantidade de aulas:"
        )

        rotulo_aulas_vespertino.setObjectName(
            "rotulo_campo_excecao"
        )

        self.aulas_vespertino = QSpinBox()

        self.aulas_vespertino.setMinimum(
            1
        )

        self.aulas_vespertino.setMaximum(
            20
        )

        self.aulas_vespertino.setValue(
            5
        )

        linha_aulas_vespertino.addWidget(
            rotulo_aulas_vespertino
        )

        linha_aulas_vespertino.addWidget(
            self.aulas_vespertino,
            1
        )

        layout_cartao_vespertino.addLayout(
            linha_aulas_vespertino
        )

        self.recreio_vespertino = QCheckBox(
            "Haverá recreio"
        )

        self.recreio_vespertino.setChecked(
            False
        )

        layout_cartao_vespertino.addWidget(
            self.recreio_vespertino
        )

        layout_turnos.addWidget(
            cartao_vespertino,
            1
        )

        # =====================================================
        # ADICIONA OS DOIS CARTÕES
        # =====================================================

        layout.addLayout(
            layout_turnos
        )
        # =====================================================
        # BOTÕES
        # =====================================================

        layout_botoes = QHBoxLayout()

        layout_botoes.addStretch()

        botao_cancelar = QPushButton(
            "CANCELAR"
        )

        botao_cancelar.setObjectName(
            "botao_cancelar"
        )

        botao_cancelar.clicked.connect(
            self.reject
        )

        botao_salvar = QPushButton(
            "SALVAR EXCEÇÃO"
        )

        botao_salvar.setObjectName(
            "botao_salvar"
        )

        botao_salvar.clicked.connect(
            self.accept
        )

        layout_botoes.addWidget(
            botao_cancelar
        )

        layout_botoes.addWidget(
            botao_salvar
        )

        layout.addLayout(
            layout_botoes
        )

        self.carregar_excecao_existente()

        # ---------------------------------------------------------
        # CARREGA A CONFIGURAÇÃO DA DATA ATUAL
        # ---------------------------------------------------------

        self.carregar_configuracao()


    def carregar_configuracao(self):

        data = self.data_excecao.date().toString(
            "yyyy-MM-dd"
        )

        configuracao = self.configuracoes.get(
            data
        )

        # ---------------------------------------------------------
        # SE NÃO EXISTIR EXCEÇÃO PARA A DATA
        # ---------------------------------------------------------

        if not configuracao:
            self.matutino_ativo.setChecked(
                False
            )
            self.duracao_matutino.setCurrentText(
                "30 minutos"
            )
            self.aulas_matutino.setValue(
                5
            )
            self.recreio_matutino.setChecked(
                False
            )

            self.vespertino_ativo.setChecked(
                False
            )

            self.duracao_vespertino.setCurrentText(
                "30 minutos"
            )

            self.aulas_vespertino.setValue(
                5
            )

            self.recreio_vespertino.setChecked(
                False
            )

            return

        # ---------------------------------------------------------
        # CARREGA MATUTINO
        # ---------------------------------------------------------

        matutino = configuracao.get(
            "matutino",
            {}
        )

        self.matutino_ativo.setChecked(
            matutino.get(
                "ativo",
                False
            )
        )

        self.duracao_matutino.setCurrentText(
            f"{matutino.get('duracao_aula', 30)} minutos"
        )

        self.aulas_matutino.setValue(
            matutino.get(
                "quantidade_aulas",
                5
            )
        )

        self.recreio_matutino.setChecked(
            matutino.get(
                "recreio",
                False
            )
        )

        # ---------------------------------------------------------
        # CARREGA VESPERTINO
        # ---------------------------------------------------------

        vespertino = configuracao.get(
            "vespertino",
            {}
        )

        self.vespertino_ativo.setChecked(
            vespertino.get(
                "ativo",
                False
            )
        )

        self.duracao_vespertino.setCurrentText(
            f"{vespertino.get('duracao_aula', 30)} minutos"
        )

        self.aulas_vespertino.setValue(
            vespertino.get(
                "quantidade_aulas",
                5
            )
        )

        self.recreio_vespertino.setChecked(
            vespertino.get(
                "recreio",
                False
            )
        )


    def carregar_excecao_existente(self):
        caminho_excecoes = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "excecoes.json"
        )

        try:
            if not os.path.exists(caminho_excecoes):
                return

            with open(
                caminho_excecoes,
                "r",
                encoding="utf-8"
            ) as arquivo:
                excecoes = json.load(arquivo)

            data = self.data_excecao.date().toString(
                "yyyy-MM-dd"
            )

            excecao = excecoes.get(data)

            if not excecao:
                return

            matutino = excecao.get(
                "matutino",
                {}
            )

            vespertino = excecao.get(
                "vespertino",
                {}
            )

            self.matutino_ativo.setChecked(
                matutino.get("ativo", False)
            )

            self.duracao_matutino.setCurrentText(
                f"{matutino.get('duracao_aula', 45)} minutos"
            )

            self.aulas_matutino.setValue(
                matutino.get("quantidade_aulas", 5)
            )

            self.recreio_matutino.setChecked(
                matutino.get("recreio", False)
            )

            self.vespertino_ativo.setChecked(
                vespertino.get("ativo", False)
            )

            self.duracao_vespertino.setCurrentText(
                f"{vespertino.get('duracao_aula', 45)} minutos"
            )

            self.aulas_vespertino.setValue(
                vespertino.get("quantidade_aulas", 5)
            )

            self.recreio_vespertino.setChecked(
                vespertino.get("recreio", False)
            )

        except Exception as erro:
            print(
                f"Erro ao carregar exceção existente: {erro}"
            )

    # =========================================================
    # ARRASTAR A JANELA DE HORÁRIOS ESPECIAIS
    # =========================================================

    def _barra_mouse_press(self, evento):

        if evento.button() == Qt.LeftButton:

            self._posicao_mouse = (
                evento.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            evento.accept()

        else:

            super().mousePressEvent(evento)


    def _barra_mouse_move(self, evento):

        if (
            self._posicao_mouse is not None
            and evento.buttons() & Qt.LeftButton
        ):

            self.move(
                evento.globalPosition().toPoint()
                - self._posicao_mouse
            )

            evento.accept()

        else:

            super().mouseMoveEvent(evento)


    def _barra_mouse_release(self, evento):

        if evento.button() == Qt.LeftButton:

            self._posicao_mouse = None

            evento.accept()

        else:

            super().mouseReleaseEvent(evento)


            
class BarraTitulo(QWidget):

    def __init__(self, janela):
        super().__init__(janela)

        self.janela = janela
        self.setObjectName("barra_titulo")
        self.setFixedHeight(44)

        # -------------------------------------------------
        # LAYOUT
        # -------------------------------------------------

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(4)

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------

        self.titulo = QLabel(
            "🔔  Sirene Automática  •  U.E. Gonçalves Dias"
        )

        self.titulo.setObjectName(
            "titulo_barra"
        )

        layout.addWidget(
            self.titulo
        )

        layout.addStretch()

        # -------------------------------------------------
        # BOTÃO MINIMIZAR
        # -------------------------------------------------

        self.botao_minimizar = QPushButton(
            "—"
        )

        self.botao_minimizar.setObjectName(
            "botao_minimizar"
        )

        self.botao_minimizar.clicked.connect(
            self.janela.showMinimized
        )

        # -------------------------------------------------
        # BOTÃO MAXIMIZAR
        # -------------------------------------------------

        self.botao_maximizar = QPushButton(
            "□"
        )

        self.botao_maximizar.setObjectName(
            "botao_maximizar"
        )

        self.botao_maximizar.clicked.connect(
            self.alternar_maximizado
        )

        # -------------------------------------------------
        # BOTÃO FECHAR
        # -------------------------------------------------

        self.botao_fechar = QPushButton(
            "×"
        )

        self.botao_fechar.setObjectName(
            "botao_fechar"
        )

        self.botao_fechar.clicked.connect(
            self.janela.close
        )

        # -------------------------------------------------
        # ESTILO DOS BOTÕES DA BARRA
        # -------------------------------------------------

        estilo_botoes = """
            QPushButton {
                background-color: transparent;
                color: #9fb2ca;
                border: none;
                border-radius: 8px;
                font-family: "Segoe UI";
                font-size: 22px;
                min-width: 46px;
                max-width: 46px;
                min-height: 44px;
                max-height: 44px;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: #243653;
                color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #1c2d46;
            }
            """
        self.botao_minimizar.setStyleSheet(estilo_botoes)
        self.botao_maximizar.setStyleSheet(estilo_botoes)

        self.botao_fechar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-family: "Segoe UI";
                font-size: 22px;
                font-weight: bold;
                min-width: 46px;
                max-width: 46px;
                min-height: 44px;
                max-height: 44px;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: #e04b3f;
                color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #962d22;
            }
        """)

        
        # -------------------------------------------------
        # ADICIONA OS BOTÕES
        # -------------------------------------------------

        layout.addWidget(
            self.botao_minimizar
        )

        layout.addWidget(
            self.botao_maximizar
        )

        layout.addWidget(
            self.botao_fechar
        )

        # -------------------------------------------------
        # CONTROLE DO ARRASTAMENTO
        # -------------------------------------------------

        self._posicao_mouse = None

    # =====================================================
    # MAXIMIZAR / RESTAURAR
    # =====================================================

    def alternar_maximizado(self):

        if self.janela.isMaximized():

            self.janela.showNormal()

            self.botao_maximizar.setText(
                "□"
            )

        else:

            self.janela.showMaximized()

            self.botao_maximizar.setText(
                "❐"
            )

    # =====================================================
    # ARRASTAR A JANELA
    # =====================================================

    def mousePressEvent(self, evento):

        if evento.button() == Qt.LeftButton:

            self._posicao_mouse = (
                evento.globalPosition().toPoint()
                - self.janela.frameGeometry().topLeft()
            )

        super().mousePressEvent(evento)

    def mouseMoveEvent(self, evento):

        if (
            self._posicao_mouse is not None
            and evento.buttons() & Qt.LeftButton
            and not self.janela.isMaximized()
        ):

            self.janela.move(
                evento.globalPosition().toPoint()
                - self._posicao_mouse
            )

        super().mouseMoveEvent(evento)

    def mouseReleaseEvent(self, evento):

        self._posicao_mouse = None

        super().mouseReleaseEvent(evento)



class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------
        # CONFIGURAÇÃO DA JANELA
        # ---------------------------------------------------------

        self.setWindowTitle(
            "Sirene Automática - U.E. Gonçalves Dias"
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Window
        )

        self.setMinimumSize(
            1000,
            850
        )

        self.resize(
            1200,
            850
        )


        # ---------------------------------------------------------
        # CARREGAMENTO DA PROGRAMACAO
        # ---------------------------------------------------------

        self.horarios = self.carregar_horarios()

        # ---------------------------------------------------------
        # CONTROLE DOS TOQUES
        # ---------------------------------------------------------

        self.ultimo_toque = None

        # ---------------------------------------------------------
        # CONFIGURAÇÃO DO AVISO ANTECIPADO
        # ---------------------------------------------------------

        self.tempo_aviso = 3
        self.quantidade_aviso = 1

        # ---------------------------------------------------------
        # DATA DO DIA CARREGADO
        # ---------------------------------------------------------

        self.dia_carregado = datetime.now().strftime(
            "%Y-%m-%d"
        )

        # ---------------------------------------------------------
        # CONTROLE DE ALTERAÇÃO MANUAL DO RELÓGIO
        # ---------------------------------------------------------
        self.ultima_verificacao_relogio = datetime.now()
        
    
        # ---------------------------------------------------------
        # CRIACAO DA INTERFACE
        # ---------------------------------------------------------

        self.criar_interface()

        # ---------------------------------------------------------
        # TIMER DO RELÓGIO
        # ---------------------------------------------------------

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(1000)
        self.atualizar_programacao_hoje()

        # Atualiza imediatamente ao abrir o programa
        self.atualizar_interface()
        

    # =============================================================
    # INTERFACE
    # =============================================================
    # =============================================================
    # OBTÉM A PROGRAMAÇÃO DE UMA DATA
    # =============================================================

    def obter_programacao_para_data(
        self,
        data_referencia,
        dados_horarios=None,
        excecoes=None
    ):

        dias_semana = {
            0: "segunda",
            1: "terca",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sabado",
            6: "domingo"
        }

        nome_dia = dias_semana[data_referencia.weekday()]
        data = data_referencia.strftime("%Y-%m-%d")

        if dados_horarios is None:

            caminho_horarios = os.path.join(
                os.path.dirname(__file__),
                "dados",
                "horarios.json"
            )

            with open(
                caminho_horarios,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados_horarios = json.load(arquivo)

        # A exceção sempre trabalha em uma cópia.
        # Nunca altera a programação semanal normal.
        horarios_dia = deepcopy(
            dados_horarios.get(
                nome_dia,
                {}
            )
        )

        if excecoes is None:

            caminho_excecoes = os.path.join(
                os.path.dirname(__file__),
                "dados",
                "excecoes.json"
            )

            if os.path.exists(caminho_excecoes):

                with open(
                    caminho_excecoes,
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    excecoes = json.load(arquivo)

            else:

                excecoes = {}

        excecao = excecoes.get(data)

        # Só uma exceção marcada como ATIVA substitui
        # a programação normal daquela data.
        if excecao and excecao.get("ativo", False):

            for turno in [
                "matutino",
                "vespertino"
            ]:

                configuracao = excecao.get(
                    turno
                )

                if not configuracao:
                    continue

                ativo = configuracao.get(
                    "ativo",
                    False
                )

                if not ativo:

                    
                    continue

                duracao = configuracao.get(
                    "duracao_aula"
                )

                quantidade = configuracao.get(
                    "quantidade_aulas",
                    5
                )

                recreio = configuracao.get(
                    "recreio",
                    False
                )

                if duracao not in [30, 35, 40, 45]:
                    continue

                horario_inicial = datetime.strptime(
                    "07:30" if turno == "matutino" else "13:30",
                    "%H:%M"
                )

                lista_excepcional = []

                for numero in range(quantidade):

                    # -----------------------------------------------------
                    # INSERE O RECREIO DEPOIS DA 3ª AULA
                    # -----------------------------------------------------
                    minutos_recreio = 15 if recreio and numero >= 3 else 0

                    horario = (
                        horario_inicial
                        + timedelta(
                            minutes=(duracao * numero) + minutos_recreio
                        )
                    ).strftime("%H:%M")

                    # -----------------------------------------------------
                    # DESCRIÇÃO DO HORÁRIO
                    # -----------------------------------------------------
                    if numero == 0:
                        descricao = "Entrada / início das aulas"

                    elif recreio and numero == 3:
                        descricao = "Retorno do recreio"

                    else:
                        descricao = "Troca de aula"

                    lista_excepcional.append(
                        {
                            "horario": horario,
                            "descricao": descricao,
                            "ativo": True
                        }
                    )

                    # -----------------------------------------------------
                    # INSERE O INÍCIO DO RECREIO
                    # DEPOIS DA 3ª AULA
                    # -----------------------------------------------------
                    if recreio and numero == 2:

                        horario_recreio = (
                            horario_inicial
                            + timedelta(
                                minutes=duracao * 3
                            )
                        ).strftime("%H:%M")

                        lista_excepcional.append(
                            {
                                "horario": horario_recreio,
                                "descricao": "Início do recreio",
                                "ativo": True
                            }
                        )

                # ---------------------------------------------------------
                # HORÁRIO DE ENCERRAMENTO
                # ---------------------------------------------------------
                minutos_recreio_total = 15 if recreio and quantidade > 3 else 0

                horario_encerramento = (
                    horario_inicial
                    + timedelta(
                        minutes=(duracao * quantidade)
                        + minutos_recreio_total
                    )
                ).strftime("%H:%M")

                lista_excepcional.append(
                    {
                        "horario": horario_encerramento,
                        "descricao": "Encerramento",
                        "ativo": True
                    }
                )

                horarios_dia[turno] = lista_excepcional

        return nome_dia, horarios_dia


    # =============================================================
    # CARREGAR HORÁRIOS
    # =============================================================

    def carregar_horarios(self):

        try:

            caminho_horarios = os.path.join(
                os.path.dirname(__file__),
                "dados",
                "horarios.json"
            )

            with open(
                caminho_horarios,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

            # Mantém a programação semanal NORMAL intacta.
            self.programacao_semana = dados

            data_atual = datetime.now()

            _, horarios_dia = self.obter_programacao_para_data(
                data_atual,
                dados_horarios=dados,
                excecoes=self.carregar_excecoes()
            )

            self.programacao_dia = horarios_dia

            dia_ativo = horarios_dia.get(
                "ativo",
                True
            )

            if not dia_ativo:
                return []

            horarios = []

            for turno in [
                "matutino",
                "vespertino"
            ]:

                lista_horarios = horarios_dia.get(
                    turno,
                    []
                )

                for item in lista_horarios:

                    if item.get(
                        "ativo",
                        True
                    ):

                        horarios.append(
                            item["horario"]
                        )

            horarios.sort()

            return horarios

        except Exception as erro:

            print(
                f"Erro ao carregar horários: {erro}"
            )

            self.programacao_dia = {}

            return []
    # =============================================================
    # CARREGAR EXCEÇÕES
    # =============================================================

    def carregar_excecoes(self):

        try:

            caminho_excecoes = os.path.join(
                os.path.dirname(__file__),
                "dados",
                "excecoes.json"
            )

            with open(
                caminho_excecoes,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

            return dados

        except Exception as erro:

            print(
                f"Erro ao carregar exceções: {erro}"
            )

            return {}

        # =============================================================
        # INTERFACE
        # =============================================================

    def criar_interface(self):

        # =========================================================
        # JANELA PRINCIPAL
        # =========================================================

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QVBoxLayout(
            widget_central
        )

        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout_principal.setSpacing(
            0
        )

        # ---------------------------------------------------------
        # BARRA DE TÍTULO PERSONALIZADA
        # ---------------------------------------------------------

        self.barra_titulo = BarraTitulo(
            self
        )

        layout_principal.addWidget(
            self.barra_titulo
        )

        # ---------------------------------------------------------
        # ÁREA DA INTERFACE
        # ---------------------------------------------------------

        widget_area = QWidget()

        layout_geral = QHBoxLayout(
            widget_area
        )

        layout_geral.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout_geral.setSpacing(
            0
        )

        layout_principal.addWidget(
            widget_area,
            1
        )

        # =========================================================
        # BARRA LATERAL
        # =========================================================

        painel_lateral = QFrame()
        painel_lateral.setObjectName("painel_lateral")
        painel_lateral.setFixedWidth(220)

        layout_lateral = QVBoxLayout(painel_lateral)
        layout_lateral.setContentsMargins(18, 25, 18, 20)
        layout_lateral.setSpacing(8)

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------

        logo_lateral = QLabel()
        logo_lateral.setObjectName("logo_lateral")
        logo_lateral.setFixedSize(80, 80)
        logo_lateral.setAlignment(Qt.AlignCenter)

        caminho_logo = os.path.join(
            os.path.dirname(__file__),
            "imagens",
            "logo_escola.png"
        )

        pixmap_logo = QPixmap(caminho_logo)

        if not pixmap_logo.isNull():

            pixmap_logo = pixmap_logo.scaled(
                72,
                72,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            logo_lateral.setPixmap(pixmap_logo)

        layout_lateral.addWidget(
            logo_lateral,
            alignment=Qt.AlignCenter
        )

        # ---------------------------------------------------------
        # NOME DO SISTEMA
        # ---------------------------------------------------------

        titulo_lateral = QLabel("SIRENE")
        titulo_lateral.setObjectName("titulo_lateral")
        titulo_lateral.setAlignment(Qt.AlignCenter)

        subtitulo_lateral = QLabel("AUTOMÁTICA")
        subtitulo_lateral.setObjectName("subtitulo_lateral")
        subtitulo_lateral.setAlignment(Qt.AlignCenter)

        escola_lateral = QLabel("U.E. GONÇALVES DIAS")
        escola_lateral.setObjectName("escola_lateral")
        escola_lateral.setAlignment(Qt.AlignCenter)
        escola_lateral.setWordWrap(True)

        layout_lateral.addWidget(titulo_lateral)
        layout_lateral.addWidget(subtitulo_lateral)
        layout_lateral.addSpacing(4)
        layout_lateral.addWidget(escola_lateral)

        # ---------------------------------------------------------
        # LINHA DIVISÓRIA
        # ---------------------------------------------------------

        linha = QFrame()
        linha.setObjectName("linha_lateral")
        linha.setFrameShape(QFrame.HLine)
        linha.setFrameShadow(QFrame.Plain)

        layout_lateral.addSpacing(18)
        layout_lateral.addWidget(linha)
        layout_lateral.addSpacing(12)

        # ---------------------------------------------------------
        # MENU
        # ---------------------------------------------------------

        label_menu = QLabel("MENU PRINCIPAL")
        label_menu.setObjectName("label_menu")

        layout_lateral.addWidget(label_menu)

        botao_inicio = QPushButton("⌂   INÍCIO")
        botao_inicio.setObjectName("botao_menu_ativo")
        botao_inicio.setMinimumHeight(44)

        botao_programacao = QPushButton("▣   PROGRAMAÇÃO")
        botao_programacao.setObjectName("botao_menu")
        botao_programacao.setMinimumHeight(44)

        self.botao_inicio = botao_inicio
        self.botao_programacao = botao_programacao

        botao_programacao.clicked.connect(
            self.abrir_programacao
        )

        botao_inicio.clicked.connect(
            self.abrir_inicio
        )

        botao_teste = QPushButton(
            "🔔   TESTE DA SIRENE"
        )

        botao_teste.setObjectName(
            "botao_menu"
        )

        botao_teste.setMinimumHeight(
            44
        )

        self.botao_teste = botao_teste
        

        layout_lateral.addWidget(botao_inicio)
        layout_lateral.addWidget(botao_programacao)
        layout_lateral.addWidget(botao_teste)

        layout_lateral.addStretch()

        # ---------------------------------------------------------
        # STATUS DA BARRA LATERAL
        # ---------------------------------------------------------

        painel_status_lateral = QFrame()
        painel_status_lateral.setObjectName("status_lateral")

        layout_status_lateral = QVBoxLayout(painel_status_lateral)
        layout_status_lateral.setContentsMargins(12, 12, 12, 12)
        layout_status_lateral.setSpacing(5)

        label_status_lateral_titulo = QLabel("STATUS")
        label_status_lateral_titulo.setObjectName(
            "status_lateral_titulo"
        )

        label_status_lateral = QLabel("●  SISTEMA ATIVO")
        label_status_lateral.setObjectName(
            "status_lateral_ativo"
        )

        label_status_lateral.setAlignment(Qt.AlignCenter)

        layout_status_lateral.addWidget(
            label_status_lateral_titulo
        )

        layout_status_lateral.addWidget(
            label_status_lateral
        )

        layout_lateral.addWidget(
            painel_status_lateral
        )

        # ---------------------------------------------------------
        # VERSÃO
        # ---------------------------------------------------------

        label_versao = QLabel("Versão 0.1")
        label_versao.setObjectName("versao_lateral")
        label_versao.setAlignment(Qt.AlignCenter)

        label_desenvolvedor = QLabel("Desenvolvido por Carlos Norato")
        label_desenvolvedor.setObjectName("desenvolvedor_lateral")
        label_desenvolvedor.setAlignment(Qt.AlignCenter)

        layout_lateral.addSpacing(10)
        layout_lateral.addWidget(label_versao)
        layout_lateral.addWidget(label_desenvolvedor)

        layout_geral.addWidget(painel_lateral)

        # =========================================================
        # ÁREA PRINCIPAL
        # =========================================================

        painel_conteudo = QFrame()
        painel_conteudo.setObjectName("painel_conteudo")

        layout_conteudo_principal = QVBoxLayout(
            painel_conteudo
        )

        layout_conteudo_principal.setContentsMargins(
            28,
            22,
            28,
            18
        )

        layout_conteudo_principal.setSpacing(16)

        # =========================================================
        # CABEÇALHO
        # =========================================================

        layout_cabecalho = QHBoxLayout()
        layout_cabecalho.setSpacing(10)

        bloco_cabecalho = QVBoxLayout()
        bloco_cabecalho.setSpacing(1)

        titulo = QLabel("Painel de Controle")
        titulo.setObjectName("titulo_principal")

        subtitulo = QLabel(
            "Sistema de gerenciamento da sirene escolar"
        )
        subtitulo.setObjectName("subtitulo_principal")

        bloco_cabecalho.addWidget(titulo)
        bloco_cabecalho.addWidget(subtitulo)

        layout_cabecalho.addLayout(bloco_cabecalho)
        layout_cabecalho.addStretch()

        # ---------------------------------------------------------
        # STATUS SUPERIOR
        # ---------------------------------------------------------

        painel_status_superior = QFrame()
        painel_status_superior.setObjectName(
            "status_superior"
        )

        layout_status_superior = QHBoxLayout(
            painel_status_superior
        )

        layout_status_superior.setContentsMargins(
            14,
            8,
            14,
            8
        )

        layout_status_superior.setSpacing(8)

        indicador = QLabel("●")
        indicador.setObjectName("indicador_status")

        texto_status = QLabel("SISTEMA ATIVO")
        texto_status.setObjectName("texto_status_superior")

        layout_status_superior.addWidget(indicador)
        layout_status_superior.addWidget(texto_status)

        layout_cabecalho.addWidget(
            painel_status_superior
        )

        layout_conteudo_principal.addLayout(
            layout_cabecalho
        )

        # =========================================================
        # CARTÕES DE INFORMAÇÃO
        # =========================================================

        layout_cartoes = QHBoxLayout()
        layout_cartoes.setSpacing(14)

        # ---------------------------------------------------------
        # CARTÃO RELÓGIO
        # ---------------------------------------------------------

        painel_relogio = QFrame()
        painel_relogio.setObjectName("cartao")

        layout_relogio = QVBoxLayout(painel_relogio)
        layout_relogio.setContentsMargins(
            20,
            16,
            20,
            15
        )

        layout_relogio.setSpacing(3)

        label_relogio_titulo = QLabel("HORÁRIO ATUAL")
        label_relogio_titulo.setObjectName("label_cartao")

        self.label_relogio = QLabel("00:00:00")
        self.label_relogio.setObjectName("relogio")
        self.label_relogio.setAlignment(Qt.AlignCenter)

        self.label_data = QLabel("00/00/0000")
        self.label_data.setObjectName("data")
        self.label_data.setAlignment(Qt.AlignCenter)

        layout_relogio.addWidget(
            label_relogio_titulo
        )

        layout_relogio.addWidget(
            self.label_relogio
        )

        layout_relogio.addWidget(
            self.label_data
        )

        layout_cartoes.addWidget(
            painel_relogio,
            1
        )

        # ---------------------------------------------------------
        # CARTÃO PRÓXIMO TOQUE
        # ---------------------------------------------------------

        painel_proximo = QFrame()
        painel_proximo.setObjectName("cartao")

        layout_proximo = QVBoxLayout(painel_proximo)
        layout_proximo.setContentsMargins(
            20,
            16,
            20,
            15
        )

        layout_proximo.setSpacing(3)

        label_proximo_titulo = QLabel("PRÓXIMO TOQUE")
        label_proximo_titulo.setObjectName("label_cartao")

        self.label_proximo = QLabel("--:--")
        self.label_proximo.setObjectName("proximo")
        self.label_proximo.setAlignment(Qt.AlignCenter)

        self.label_contagem = QLabel("Aguardando...")
        self.label_contagem.setObjectName("contagem")
        self.label_contagem.setAlignment(Qt.AlignCenter)

        layout_proximo.addWidget(
            label_proximo_titulo
        )

        layout_proximo.addWidget(
            self.label_proximo
        )

        layout_proximo.addWidget(
            self.label_contagem
        )

        layout_cartoes.addWidget(
            painel_proximo,
            1
        )

        # ---------------------------------------------------------
        # CARTÃO STATUS
        # ---------------------------------------------------------

        painel_status = QFrame()
        painel_status.setObjectName("cartao")

        layout_status = QVBoxLayout(painel_status)
        layout_status.setContentsMargins(
            20,
            16,
            20,
            15
        )

        layout_status.setSpacing(3)

        label_status_titulo = QLabel(
            "STATUS DA SIRENE"
        )
        label_status_titulo.setObjectName("label_cartao")

        self.label_status = QLabel(
            "● SISTEMA ATIVO"
        )

        self.label_status.setObjectName(
            "status_ativo"
        )

        self.label_status.setAlignment(
            Qt.AlignCenter
        )

        layout_status.addWidget(
            label_status_titulo
        )

        layout_status.addWidget(
            self.label_status
        )

        layout_cartoes.addWidget(
            painel_status,
            1
        )

        layout_conteudo_principal.addLayout(
            layout_cartoes
        )


        # =========================================================
        # PROGRAMAÇÃO DE HOJE
        # =========================================================

        painel_hoje = QFrame()
        painel_hoje.setObjectName(
            "painel_hoje"
        )

        layout_hoje = QVBoxLayout(
            painel_hoje
        )

        layout_hoje.setContentsMargins(
            20,
            15,
            20,
            15
        )

        layout_hoje.setSpacing(8)

        # ---------------------------------------------------------
        # CABEÇALHO
        # ---------------------------------------------------------

        layout_titulo_hoje = QHBoxLayout()

        label_titulo_hoje = QLabel(
            "PROGRAMAÇÃO DE HOJE"
        )

        label_titulo_hoje.setObjectName(
            "titulo_hoje"
        )

        self.label_dia_hoje = QLabel()

        self.label_dia_hoje.setObjectName(
            "dia_hoje"
        )

        layout_titulo_hoje.addWidget(
            label_titulo_hoje
        )

        layout_titulo_hoje.addStretch()

        layout_titulo_hoje.addWidget(
            self.label_dia_hoje
        )

        layout_hoje.addLayout(
            layout_titulo_hoje
        )

        # ---------------------------------------------------------
        # HORÁRIOS DE HOJE
        # ---------------------------------------------------------

        layout_horarios_hoje = QHBoxLayout()
        layout_horarios_hoje.setSpacing(14)

        # ---------------------------------------------------------
        # MATUTINO
        # ---------------------------------------------------------

        painel_hoje_matutino = QFrame()
        painel_hoje_matutino.setObjectName(
            "painel_horario_hoje"
        )

        layout_hoje_matutino = QVBoxLayout(
            painel_hoje_matutino
        )

        layout_hoje_matutino.setContentsMargins(
            14,
            10,
            14,
            10
        )

        layout_hoje_matutino.setSpacing(3)

        titulo_hoje_matutino = QLabel(
            "☀  MATUTINO"
        )

        titulo_hoje_matutino.setObjectName(
            "titulo_horario_hoje"
        )

        self.label_hoje_matutino = QLabel(
            "Carregando..."
        )

        self.label_hoje_matutino.setObjectName(
            "texto_horario_hoje"
        )

        self.label_hoje_matutino.setWordWrap(
            True
        )

        layout_hoje_matutino.addWidget(
            titulo_hoje_matutino
        )

        layout_hoje_matutino.addWidget(
            self.label_hoje_matutino
        )

        layout_horarios_hoje.addWidget(
            painel_hoje_matutino,
            1
        )

        # ---------------------------------------------------------
        # VESPERTINO
        # ---------------------------------------------------------

        painel_hoje_vespertino = QFrame()
        painel_hoje_vespertino.setObjectName(
            "painel_horario_hoje"
        )

        layout_hoje_vespertino = QVBoxLayout(
            painel_hoje_vespertino
        )

        layout_hoje_vespertino.setContentsMargins(
            14,
            10,
            14,
            10
        )

        layout_hoje_vespertino.setSpacing(3)

        titulo_hoje_vespertino = QLabel(
            "☀  VESPERTINO"
        )

        titulo_hoje_vespertino.setObjectName(
            "titulo_horario_hoje"
        )

        self.label_hoje_vespertino = QLabel(
            "Carregando..."
        )

        self.label_hoje_vespertino.setObjectName(
            "texto_horario_hoje"
        )

        self.label_hoje_vespertino.setWordWrap(
            True
        )

        layout_hoje_vespertino.addWidget(
            titulo_hoje_vespertino
        )

        layout_hoje_vespertino.addWidget(
            self.label_hoje_vespertino
        )

        layout_horarios_hoje.addWidget(
            painel_hoje_vespertino,
            1
        )

        layout_hoje.addLayout(
            layout_horarios_hoje
        )

        layout_conteudo_principal.addWidget(
            painel_hoje
        )

        # =========================================================
        # PROGRAMAÇÃO SEMANAL
        # =========================================================
    
        # =========================================================
        # PROGRAMAÇÃO SEMANAL
        # =========================================================

        painel_programacao = QFrame()
        painel_programacao.setObjectName(
            "painel_programacao"
        )

        self.painel_programacao = painel_programacao

        layout_programacao = QVBoxLayout(
            painel_programacao
        )

        layout_programacao.setContentsMargins(
            20,
            17,
            20,
            17
        )

        layout_programacao.setSpacing(10)

        # ---------------------------------------------------------
        # TÍTULO
        # ---------------------------------------------------------

        layout_titulo_programacao = QHBoxLayout()

        label_programacao_titulo = QLabel(
            "PROGRAMAÇÃO SEMANAL"
        )

        label_programacao_titulo.setObjectName(
            "titulo_secao"
        )

        label_programacao_info = QLabel(
            "Horários programados para acionamento"
        )

        label_programacao_info.setObjectName(
            "info_secao"
        )

        botao_excecoes = QPushButton(
            "HORÁRIOS ESPECIAIS"
        )

        botao_excecoes.setObjectName(
            "botao_excecoes"
        )

        botao_excecoes.setMinimumHeight(
            32
        )

        botao_excecoes.clicked.connect(
            self.abrir_excecoes
        )

        layout_titulo_programacao.addWidget(
            label_programacao_titulo
        )

        layout_titulo_programacao.addStretch()

        layout_titulo_programacao.addWidget(
        label_programacao_info
        )

        layout_titulo_programacao.addWidget(
            botao_excecoes
        )

        layout_programacao.addLayout(
            layout_titulo_programacao
        )

        # ---------------------------------------------------------
        # DIAS DA SEMANA
        # ---------------------------------------------------------

        layout_dias = QHBoxLayout()
        layout_dias.setSpacing(8)

        nomes_dias = {
            "segunda": "SEGUNDA",
            "terca": "TERÇA",
            "quarta": "QUARTA",
            "quinta": "QUINTA",
            "sexta": "SEXTA"
        }

        self.botoes_dias = {}
        self.checkboxes_dias = {}

        for dia, nome in nomes_dias.items():

            # -----------------------------------------------------
            # PAINEL DO DIA
            # -----------------------------------------------------

            painel_dia = QFrame()
            painel_dia.setObjectName("painel_dia")

            layout_dia = QVBoxLayout(painel_dia)

            layout_dia.setContentsMargins(
                8,
                6,
                8,
                6
            )

            layout_dia.setSpacing(4)

            # -----------------------------------------------------
            # BOTÃO DO DIA
            # -----------------------------------------------------

            botao_dia = QPushButton(nome)

            botao_dia.setObjectName(
                "botao_dia"
            )

            botao_dia.setCheckable(True)
            botao_dia.setMinimumHeight(34)

            botao_dia.clicked.connect(
                lambda checked=False, dia=dia:
                self.selecionar_dia_programacao(dia)
            )

            # -----------------------------------------------------
            # CHECKBOX ATIVO
            # -----------------------------------------------------

            checkbox_dia = QCheckBox("ATIVO")

            checkbox_dia.setObjectName(
                "checkbox_dia"
            )

            checkbox_dia.setChecked(
                self.programacao_semana.get(
                    dia,
                    {}
                ).get(
                    "ativo",
                    True
                )
            )

            checkbox_dia.stateChanged.connect(
                lambda estado, dia=dia:
                self.alterar_status_dia(dia, estado)
            )

            # -----------------------------------------------------
            # ADICIONA AO PAINEL
            # -----------------------------------------------------

            layout_dia.addWidget(
                botao_dia
            )

            layout_dia.addWidget(
                checkbox_dia,
                alignment=Qt.AlignCenter
            )

            # -----------------------------------------------------
            # GUARDA OS CONTROLES
            # -----------------------------------------------------

            self.botoes_dias[dia] = botao_dia
            self.checkboxes_dias[dia] = checkbox_dia

            # -----------------------------------------------------
            # ADICIONA O PAINEL AO LAYOUT
            # -----------------------------------------------------

            layout_dias.addWidget(
                painel_dia,
                1
            )

        layout_programacao.addLayout(
            layout_dias
        )

        # ---------------------------------------------------------
        # TURNOS
        # ---------------------------------------------------------

        layout_turnos = QHBoxLayout()
        layout_turnos.setSpacing(14)

        # =========================================================
        # MATUTINO
        # =========================================================

        painel_matutino = QFrame()
        painel_matutino.setObjectName(
            "painel_turno"
        )

        layout_matutino = QVBoxLayout(
            painel_matutino
        )

        layout_matutino.setContentsMargins(
            15,
            11,
            15,
            11
        )

        layout_matutino.setSpacing(5)

        titulo_matutino = QLabel(
            "☀  MATUTINO"
        )

        titulo_matutino.setObjectName(
            "titulo_turno"
        )

        self.label_programacao_matutino = QLabel()

        self.label_programacao_matutino.setObjectName(
            "linha_horario"
        )

        self.label_programacao_matutino.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )

        self.label_programacao_matutino.setWordWrap(
            True
        )

        layout_matutino.addWidget(
            titulo_matutino
        )

        layout_matutino.addWidget(
            self.label_programacao_matutino
        )

        layout_turnos.addWidget(
            painel_matutino,
            1
        )

        # =========================================================
        # VESPERTINO
        # =========================================================

        painel_vespertino = QFrame()
        painel_vespertino.setObjectName(
            "painel_turno"
        )

        layout_vespertino = QVBoxLayout(
            painel_vespertino
        )

        layout_vespertino.setContentsMargins(
            15,
            11,
            15,
            11
        )

        layout_vespertino.setSpacing(5)

        titulo_vespertino = QLabel(
            "☀  VESPERTINO"
        )

        titulo_vespertino.setObjectName(
            "titulo_turno"
        )

        self.label_programacao_vespertino = QLabel()

        self.label_programacao_vespertino.setObjectName(
            "linha_horario"
        )

        self.label_programacao_vespertino.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )

        self.label_programacao_vespertino.setWordWrap(
            True
        )

        layout_vespertino.addWidget(
            titulo_vespertino
        )

        layout_vespertino.addWidget(
            self.label_programacao_vespertino
        )

        layout_turnos.addWidget(
            painel_vespertino,
            1
        )

        layout_programacao.addLayout(
            layout_turnos
        )

        layout_conteudo_principal.addWidget(
            painel_programacao,
            
        )

        # =========================================================
        # TESTE MANUAL
        # =========================================================

        painel_teste = QFrame()
        painel_teste.setObjectName(
            "painel_teste"
        )

        self.painel_teste = painel_teste

        layout_teste = QHBoxLayout(
            painel_teste
        )

        layout_teste.setContentsMargins(
            20,
            13,
            20,
            13
        )

        layout_teste.setSpacing(15)

        # ---------------------------------------------------------
        # INFORMAÇÕES
        # ---------------------------------------------------------

        bloco_teste = QVBoxLayout()
        bloco_teste.setSpacing(3)

        label_teste_titulo = QLabel(
            "TESTE MANUAL"
        )

        label_teste_titulo.setObjectName(
            "titulo_teste"
        )

        self.label_teste = QLabel(
            "Use o botão ao lado para testar a sirene."
        )

        self.label_teste.setObjectName(
            "texto_teste"
        )

        bloco_teste.addWidget(
            label_teste_titulo
        )

        bloco_teste.addWidget(
            self.label_teste
        )

        layout_teste.addLayout(
            bloco_teste
        )

        layout_teste.addStretch()

        # ---------------------------------------------------------
        # CONFIGURAÇÃO DO AVISO ANTECIPADO
        # ---------------------------------------------------------

        bloco_aviso = QVBoxLayout()
        bloco_aviso.setSpacing(4)

        label_aviso = QLabel(
            "AVISAR ANTES:"
        )

        label_aviso.setObjectName(
            "titulo_teste"
        )

        self.combo_tempo_aviso = QComboBox()

        self.combo_tempo_aviso.addItems(
            [
                "3 minutos",
                "5 minutos"
            ]
        )

        self.combo_tempo_aviso.setCurrentText(
            "3 minutos"
        )

        # ---------------------------------------------------------
        # ESTILO DO CAMPO DE TEMPO
        # ---------------------------------------------------------

        self.combo_tempo_aviso.setStyleSheet("""
            QComboBox {
                background-color: #111d30;
                color: #ffffff;
                border: 1px solid #304766;
                border-radius: 7px;
                padding: 6px 10px;
                min-height: 30px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }

            QComboBox:hover {
                border: 1px solid #2196e0;
            }

            QComboBox:focus {
                border: 1px solid #29a3f0;
            }

            QComboBox::drop-down {
                width: 28px;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #111d30;
                color: #ffffff;
                border: 1px solid #304766;
                selection-background-color: #2196e0;
                selection-color: #ffffff;
                padding: 4px;
            }
        """)

        bloco_aviso.addWidget(
            label_aviso
        )

        bloco_aviso.addWidget(
            self.combo_tempo_aviso
        )

        layout_teste.addLayout(
            bloco_aviso
        )

        # ---------------------------------------------------------
        # QUANTIDADE DE TOQUES
        # ---------------------------------------------------------

        bloco_quantidade = QVBoxLayout()
        bloco_quantidade.setSpacing(4)

        label_quantidade = QLabel(
            "TOQUES DO AVISO:"
        )

        label_quantidade.setObjectName(
            "titulo_teste"
        )

        self.combo_quantidade_aviso = QComboBox()

        self.combo_quantidade_aviso.addItems(
            [
                "1 toque",
                "2 toques",
                "3 toques"
            ]
        )

        self.combo_quantidade_aviso.setCurrentText(
            "1 toque"
        )

        # ---------------------------------------------------------
        # ESTILO DO CAMPO DE QUANTIDADE
        # ---------------------------------------------------------

        self.combo_quantidade_aviso.setStyleSheet("""
            QComboBox {
                background-color: #111d30;
                color: #ffffff;
                border: 1px solid #304766;
                border-radius: 7px;
                padding: 6px 10px;
                min-height: 30px;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 600;
            }

            QComboBox:hover {
                border: 1px solid #2196e0;
            }

            QComboBox:focus {
                border: 1px solid #29a3f0;
            }

            QComboBox::drop-down {
                width: 28px;
                border: none;
            }

            QComboBox QAbstractItemView {
                background-color: #111d30;
                color: #ffffff;
                border: 1px solid #304766;
                selection-background-color: #2196e0;
                selection-color: #ffffff;
                padding: 4px;
            }
        """)

        # ---------------------------------------------------------
        # ATUALIZA A CONFIGURAÇÃO DO AVISO
        # ---------------------------------------------------------

        self.combo_tempo_aviso.currentTextChanged.connect(
            self.atualizar_configuracao_aviso
        )

        self.combo_quantidade_aviso.currentTextChanged.connect(
            self.atualizar_configuracao_aviso
        )


        bloco_quantidade.addWidget(
            label_quantidade
        )

        bloco_quantidade.addWidget(
            self.combo_quantidade_aviso
        )

        layout_teste.addLayout(
            bloco_quantidade
        )

        # ---------------------------------------------------------
        # BOTÃO
        # ---------------------------------------------------------

        botao_testar = QPushButton(
            "🔔 TESTAR SIRENE"
        )

        botao_testar.setObjectName(
            "botao_testar"
        )

        botao_testar.setMinimumSize(
            230,
            48
        )

        botao_testar.clicked.connect(
            self.testar_sirene
        )

    

        layout_teste.addWidget(
            botao_testar
        )

        layout_conteudo_principal.addWidget(
            painel_teste
        )

        # =========================================================
        # RODAPÉ
        # =========================================================

        layout_rodape = QHBoxLayout()

        label_rodape = QLabel(
            "SIRENE AUTOMÁTICA • U.E. GONÇALVES DIAS"
        )

        label_rodape.setObjectName(
            "rodape"
        )

        label_rodape_direita = QLabel(
            "Sistema de controle escolar"
        )

        label_rodape_direita.setObjectName(
            "rodape"
        )

        layout_rodape.addWidget(
            label_rodape
        )

        layout_rodape.addStretch()

        layout_rodape.addWidget(
            label_rodape_direita
        )

        layout_conteudo_principal.addLayout(
            layout_rodape
        )

        # =========================================================
        # ÁREA PRINCIPAL COM NAVEGAÇÃO
        # =========================================================

        area_rolagem = QScrollArea()

        area_rolagem.setWidgetResizable(
            True
        )

        area_rolagem.setFrameShape(
            QFrame.NoFrame
        )

        area_rolagem.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        area_rolagem.setWidget(
            painel_conteudo
        )

        self.area_rolagem = area_rolagem

        layout_geral.addWidget(
            area_rolagem,
            1
        )

        

        # =========================================================
        # DIA INICIAL
        # =========================================================

        dias_uteis = [
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta"
        ]

        indice_dia = datetime.now().weekday()

        if indice_dia < 5:
            dia_inicial = dias_uteis[indice_dia]
        else:
            dia_inicial = "segunda"

        self.selecionar_dia_programacao(
            dia_inicial
        )

        # =========================================================
        # ESTILO VISUAL
        # =========================================================

        self.setStyleSheet("""
        /* =========================================================
        IDENTIDADE VISUAL - SIRENE AUTOMÁTICA
        ========================================================= */

        /* =========================================================
        JANELA PRINCIPAL
        ========================================================= */

        QMainWindow {
            background-color: #0b1220;
        }

        QWidget {
            font-family: "Segoe UI";
            color: #e6edf7;
        }

        QScrollArea {
            background-color: #0b1220;
            border: none;
        }

        QScrollArea > QWidget > QWidget {
            background-color: #0b1220;
        }


        /* =========================================================
        BARRA LATERAL
        ========================================================= */

        QFrame#painel_lateral {
            background-color: #111c2f;
            border: none;
        }

        QLabel#logo_lateral {
            background-color: transparent;
        }

        QLabel#titulo_lateral {
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
        }

        QLabel#subtitulo_lateral {
            color: #38bdf8;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        QLabel#escola_lateral {
            color: #91a4bd;
            font-size: 10px;
            font-weight: bold;
        }

        QFrame#linha_lateral {
            background-color: #263754;
            color: #263754;
            max-height: 1px;
        }

        QLabel#label_menu {
            color: #647892;
            font-size: 10px;
            font-weight: bold;
            padding-left: 7px;
            padding-bottom: 4px;
        }


        /* =========================================================
        MENU LATERAL
        ========================================================= */

        QPushButton#botao_menu {
            background-color: transparent;
            color: #a9b8cb;
            border: none;
            border-radius: 10px;
            text-align: left;
            padding-left: 16px;
            font-size: 12px;
            font-weight: bold;
        }

        QPushButton#botao_menu:hover {
            background-color: #1a2b45;
            color: #ffffff;
        }

        QPushButton#botao_menu:pressed {
            background-color: #203653;
        }

        QPushButton#botao_menu_ativo {
            background-color: #1d9bf0;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            text-align: left;
            padding-left: 16px;
            font-size: 12px;
            font-weight: bold;
        }


        /* =========================================================
        STATUS DA BARRA LATERAL
        ========================================================= */

        QFrame#status_lateral {
            background-color: #16263f;
            border: 1px solid #263c5b;
            border-radius: 12px;
        }

        QLabel#status_lateral_titulo {
            color: #687e99;
            font-size: 9px;
            font-weight: bold;
        }

        QLabel#status_lateral_ativo {
            color: #4ade80;
            font-size: 11px;
            font-weight: bold;
        }

        QLabel#versao_lateral {
            color: #50657f;
            font-size: 9px;
        }


        /* =========================================================
        ÁREA PRINCIPAL
        ========================================================= */

        QFrame#painel_conteudo {
            background-color: #0b1220;
            border: none;
        }


        /* =========================================================
        CABEÇALHO
        ========================================================= */

        QLabel#titulo_principal {
            color: #f8fafc;
            font-size: 26px;
            font-weight: bold;
        }

        QLabel#subtitulo_principal {
            color: #71849d;
            font-size: 12px;
        }

        QFrame#status_superior {
            background-color: #142238;
            border: 1px solid #263b58;
            border-radius: 16px;
        }

        QLabel#indicador_status {
            color: #4ade80;
            font-size: 11px;
        }

        QLabel#texto_status_superior {
            color: #4ade80;
            font-size: 11px;
            font-weight: bold;
        }


        /* =========================================================
        CARTÕES SUPERIORES
        ========================================================= */

        QFrame#cartao {
            background-color: #141f33;
            border: 1px solid #263750;
            border-radius: 16px;
        }

        QFrame#cartao:hover {
            border: 1px solid #385273;
        }

        QLabel#label_cartao {
            color: #7186a1;
            font-size: 10px;
            font-weight: bold;
        }

        QLabel#relogio {
            color: #38bdf8;
            font-size: 40px;
            font-weight: bold;
        }

        QLabel#data {
            color: #70839c;
            font-size: 12px;
        }

        QLabel#proximo {
            color: #ffffff;
            font-size: 40px;
            font-weight: bold;
        }

        QLabel#contagem {
            color: #38bdf8;
            font-size: 12px;
        }

        QLabel#status_ativo {
            color: #4ade80;
            font-size: 18px;
            font-weight: bold;
        }


        /* =========================================================
        PROGRAMAÇÃO DE HOJE
        ========================================================= */

        QFrame#painel_hoje {
            background-color: #141f33;
            border: 1px solid #263750;
            border-radius: 16px;
        }

        QLabel#titulo_hoje {
            color: #dce6f2;
            font-size: 12px;
            font-weight: bold;
        }

        QLabel#dia_hoje {
            color: #38bdf8;
            font-size: 10px;
            font-weight: bold;
        }

        QFrame#painel_horario_hoje {
            background-color: #101a2c;
            border: 1px solid #263750;
            border-radius: 12px;
        }

        QLabel#titulo_horario_hoje {
            color: #ffffff;
            font-size: 11px;
            font-weight: bold;
        }

        QLabel#texto_horario_hoje {
            color: #8fa3bc;
            font-size: 10px;
        }


        /* =========================================================
        PROGRAMAÇÃO SEMANAL
        ========================================================= */

        QFrame#painel_programacao {
            background-color: #141f33;
            border: 1px solid #263750;
            border-radius: 16px;
        }

        QLabel#titulo_secao {
            color: #dce6f2;
            font-size: 12px;
            font-weight: bold;
        }

        QLabel#info_secao {
            color: #647993;
            font-size: 10px;
        }


        /* =========================================================
        BOTÃO HORÁRIOS ESPECIAIS
        ========================================================= */

        QPushButton#botao_excecoes {
            background-color: #182943;
            color: #38bdf8;
            border: 1px solid #315070;
            border-radius: 9px;
            padding: 7px 13px;
            font-size: 10px;
            font-weight: bold;
        }

        QPushButton#botao_excecoes:hover {
            background-color: #1e3553;
            border: 1px solid #38bdf8;
            color: #ffffff;
        }

        QPushButton#botao_excecoes:pressed {
            background-color: #122238;
        }


        /* =========================================================
        DIAS DA SEMANA
        ========================================================= */

        QFrame#painel_dia {
            background-color: transparent;
            border: none;
        }

        QPushButton#botao_dia {
            background-color: #101a2c;
            color: #9db0c8;
            border: 1px solid #2a3e59;
            border-radius: 10px;
            padding: 6px;
            font-size: 10px;
            font-weight: bold;
        }

        QPushButton#botao_dia:hover {
            background-color: #182b45;
            color: #ffffff;
            border: 1px solid #3b5777;
        }

        QPushButton#botao_dia:checked {
            background-color: #1d9bf0;
            color: #ffffff;
            border: 1px solid #1d9bf0;
        }


        /* =========================================================
        CHECKBOX DOS DIAS
        ========================================================= */

        QCheckBox#checkbox_dia {
            color: #4ade80;
            font-size: 8px;
            font-weight: bold;
            spacing: 3px;
        }

        QCheckBox#checkbox_dia::indicator {
            width: 12px;
            height: 12px;
        }

        QCheckBox#checkbox_dia::indicator:unchecked {
            background-color: #111c2f;
            border: 1px solid #4b607a;
            border-radius: 3px;
        }

        QCheckBox#checkbox_dia::indicator:checked {
            background-color: #4ade80;
            border: 1px solid #4ade80;
            border-radius: 3px;
        }

        QCheckBox#checkbox_dia:checked {
            color: #4ade80;
        }


        /* =========================================================
        TURNOS
        ========================================================= */

        QFrame#painel_turno {
            background-color: #101a2c;
            border: 1px solid #263750;
            border-radius: 12px;
        }

        QLabel#titulo_turno {
            color: #ffffff;
            font-size: 11px;
            font-weight: bold;
        }

        QLabel#linha_horario {
            color: #8fa3bc;
            font-size: 10px;
        }


        /* =========================================================
        TESTE MANUAL
        ========================================================= */

        QFrame#painel_teste {
            background-color: #141f33;
            border: 1px solid #263750;
            border-radius: 16px;
        }

        QLabel#titulo_teste {
            color: #dce6f2;
            font-size: 11px;
            font-weight: bold;
        }

        QLabel#texto_teste {
            color: #7186a1;
            font-size: 11px;
        }

        QPushButton#botao_testar {
            background-color: #1d9bf0;
            color: #ffffff;
            border: none;
            border-radius: 11px;
            font-size: 13px;
            font-weight: bold;
            padding: 8px 20px;
        }

        QPushButton#botao_testar:hover {
            background-color: #38bdf8;
        }

        QPushButton#botao_testar:pressed {
            background-color: #1685cf;
        }


        /* =========================================================
        RODAPÉ
        ========================================================= */

        QLabel#rodape {
            color: #4f637c;
            font-size: 9px;
        }


        /* =========================================================
        BARRA DE ROLAGEM
        ========================================================= */

        QScrollBar:vertical {
            background-color: #0b1220;
            width: 8px;
            margin: 2px;
        }

        QScrollBar::handle:vertical {
            background-color: #2a405d;
            border-radius: 4px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #385878;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
        """)



    # =============================================================
    # ATUALIZAR PROGRAMAÇÃO DE HOJE
    # =============================================================

    def atualizar_programacao_hoje(self):

        agora = datetime.now()

        dias_semana = {
            0: "segunda",
            1: "terca",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sabado",
            6: "domingo"
        }

        nomes_dias = {
            "segunda": "SEGUNDA-FEIRA",
            "terca": "TERÇA-FEIRA",
            "quarta": "QUARTA-FEIRA",
            "quinta": "QUINTA-FEIRA",
            "sexta": "SEXTA-FEIRA",
            "sabado": "SÁBADO",
            "domingo": "DOMINGO"
        }

        dia_atual = dias_semana[
            agora.weekday()
        ]

        # Exibe a programação REAL da data atual.
        # Se houver exceção ativa, ela já foi aplicada em
        # self.programacao_dia sem alterar a programação semanal.
        programacao = self.programacao_dia

        # ---------------------------------------------------------
        # NOME DO DIA
        # ---------------------------------------------------------

        self.label_dia_hoje.setText(
            nomes_dias.get(
                dia_atual,
                dia_atual.upper()
            )
        )

        # ---------------------------------------------------------
        # VERIFICA SE O DIA ESTÁ ATIVO
        # ---------------------------------------------------------

        dia_ativo = programacao.get(
            "ativo",
            True
        )

        if not dia_ativo:

            self.label_hoje_matutino.setText(
                "Dia desativado"
            )

            self.label_hoje_vespertino.setText(
                "Dia desativado"
            )

            return

        # ---------------------------------------------------------
        # MATUTINO
        # ---------------------------------------------------------

        linhas_matutino = []

        for item in programacao.get(
            "matutino",
            []
        ):

            if item.get(
                "ativo",
                True
            ):

                linhas_matutino.append(
                    f"{item.get('horario', '--:--')}   "
                    f"{item.get('descricao', '')}"
                )

        if linhas_matutino:

            self.label_hoje_matutino.setText(
                "\n".join(linhas_matutino)
            )

        else:

            self.label_hoje_matutino.setText(
                "Sem programação"
            )

        # ---------------------------------------------------------
        # VESPERTINO
        # ---------------------------------------------------------

        linhas_vespertino = []

        for item in programacao.get(
            "vespertino",
            []
        ):

            if item.get(
                "ativo",
                True
            ):

                linhas_vespertino.append(
                    f"{item.get('horario', '--:--')}   "
                    f"{item.get('descricao', '')}"
                )

        if linhas_vespertino:

            self.label_hoje_vespertino.setText(
                "\n".join(linhas_vespertino)
            )

        else:

            self.label_hoje_vespertino.setText(
                "Sem programação"
            )

    
    # =============================================================
    # ALTERAR STATUS DO DIA
    # =============================================================

    def alterar_status_dia(self, dia, estado):

        ativo = estado == Qt.Checked.value

        # ---------------------------------------------------------
        # ATUALIZA A ESTRUTURA EM MEMÓRIA
        # ---------------------------------------------------------

        if dia not in self.programacao_semana:
            self.programacao_semana[dia] = {}

        # Garante que o dia seja um dicionário
        if not isinstance(self.programacao_semana[dia], dict):
            self.programacao_semana[dia] = {}

        self.programacao_semana[dia]["ativo"] = ativo

        # ---------------------------------------------------------
        # CAMINHO DO ARQUIVO
        # ---------------------------------------------------------

        caminho_horarios = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "horarios.json"
        )

        # ---------------------------------------------------------
        # SALVA NO JSON
        # ---------------------------------------------------------

        try:

            with open(
                caminho_horarios,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    self.programacao_semana,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

            print(
                f"Dia {dia}: "
                f"{'ATIVO' if ativo else 'DESATIVADO'}"
            )

            print(
                f"Arquivo salvo em: {caminho_horarios}"
            )

            # -----------------------------------------------------
            # SE FOR O DIA ATUAL,
            # ATUALIZA OS HORÁRIOS DA SIRENE
            # -----------------------------------------------------

            dias_semana = {
                0: "segunda",
                1: "terca",
                2: "quarta",
                3: "quinta",
                4: "sexta",
                5: "sabado",
                6: "domingo"
            }

            nome_dia_atual = dias_semana[
                datetime.now().weekday()
            ]

            if dia == nome_dia_atual:
            # ---------------------------------------------------------
            # CARREGAMENTO DA PROGRAMACAO
            # ---------------------------------------------------------

                self.horarios = self.carregar_horarios()
                self.excecoes = self.carregar_excecoes()

                self.ultimo_toque = None

        except Exception as erro:

            print(
                f"Erro ao salvar programação: {erro}"
            )


    def selecionar_dia_programacao(self, dia):

        for nome, botao in self.botoes_dias.items():

            botao.setChecked(nome == dia)

        programacao = self.programacao_semana.get(
            dia,
            {}
        )

        # ---------------------------------------------------------
        # ATUALIZA O CHECKBOX DO DIA
        # ---------------------------------------------------------

        dia_ativo = programacao.get(
            "ativo",
            True
        )

        checkbox = self.checkboxes_dias.get(dia)

        if checkbox is not None:

            checkbox.blockSignals(True)

            checkbox.setChecked(
                dia_ativo
            )

            checkbox.blockSignals(False)

        # O dia pode estar selecionado mesmo estando inativo.
        # A programação continua sendo exibida para configuração.

        # ---------------------------------------------------------
        # MATUTINO E VESPERTINO
        # ---------------------------------------------------------

        for turno, label in [
            ("matutino", self.label_programacao_matutino),
            ("vespertino", self.label_programacao_vespertino)
        ]:

            linhas = []

            for item in programacao.get(turno, []):

                if item.get("ativo", True):

                    linhas.append(
                        f"{item.get('horario', '--:--')}   "
                        f"{item.get('descricao', '')}"
                    )

            if linhas:

                label.setText("\n".join(linhas))

            else:

                label.setText("Sem programação")

    # =============================================================
    # ABRIR PROGRAMAÇÃO
    # =============================================================

    def abrir_programacao(self):

        dias_semana = {
            0: "segunda",
            1: "terca",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sabado",
            6: "domingo"
        }

        dia_atual = dias_semana[
            datetime.now().weekday()
        ]

        self.selecionar_dia_programacao(
            dia_atual
        )

        # ---------------------------------------------------------
        # NAVEGA ATÉ A PROGRAMAÇÃO
        # ---------------------------------------------------------

        self.area_rolagem.verticalScrollBar().setValue(
            self.painel_programacao.y()
        )

        # ---------------------------------------------------------
        # ATUALIZA O BOTÃO ATIVO
        # ---------------------------------------------------------

        self.botao_inicio.setObjectName(
            "botao_menu"
        )

        self.botao_programacao.setObjectName(
            "botao_menu_ativo"
        )

        self.botao_inicio.style().unpolish(
            self.botao_inicio
        )

        self.botao_inicio.style().polish(
            self.botao_inicio
        )

        self.botao_programacao.style().unpolish(
            self.botao_programacao
        )

        self.botao_programacao.style().polish(
            self.botao_programacao
        )


    # =============================================================
    # ABRIR INÍCIO
    # =============================================================

    def abrir_inicio(self):

        # ---------------------------------------------------------
        # VOLTA PARA O TOPO
        # ---------------------------------------------------------

        self.area_rolagem.verticalScrollBar().setValue(0)

        # ---------------------------------------------------------
        # ATUALIZA O BOTÃO ATIVO
        # ---------------------------------------------------------

        self.botao_inicio.setObjectName(
            "botao_menu_ativo"
        )

        self.botao_programacao.setObjectName(
            "botao_menu"
        )

        self.botao_inicio.style().unpolish(
            self.botao_inicio
        )

        self.botao_inicio.style().polish(
            self.botao_inicio
        )

        self.botao_programacao.style().unpolish(
            self.botao_programacao
        )

        self.botao_programacao.style().polish(
            self.botao_programacao
        )



    # =============================================================
    # HORÁRIOS ESPECIAIS
    # =============================================================

    def abrir_excecoes(self):

        self.excecoes = self.carregar_excecoes()

        janela = JanelaExcecoes(
            self,
            self.excecoes
        )

        resultado = janela.exec()

        if resultado != QDialog.Accepted:
            return

        # =========================================================
        # DATA DA EXCEÇÃO
        # =========================================================

        data = janela.data_excecao.date().toString(
            "yyyy-MM-dd"
        )


    














    

        # =========================================================
        # CONVERTE DURAÇÃO
        # =========================================================

        duracao_matutino = int(
            janela.duracao_matutino.currentText().split()[0]
        )

        duracao_vespertino = int(
            janela.duracao_vespertino.currentText().split()[0]
        )

        # =========================================================
        # MONTA A EXCEÇÃO
        # =========================================================

        excecao = {

            # A exceção fica ativa quando pelo menos
            # um dos turnos estiver ativo
            "ativo": (
                janela.matutino_ativo.isChecked()
                or janela.vespertino_ativo.isChecked()
            ),

            "matutino": {
                "ativo": janela.matutino_ativo.isChecked(),
                "duracao_aula": duracao_matutino,
                "recreio": janela.recreio_matutino.isChecked(),
                "quantidade_aulas": janela.aulas_matutino.value()
            },

            "vespertino": {
                "ativo": janela.vespertino_ativo.isChecked(),
                "duracao_aula": duracao_vespertino,
                "recreio": janela.recreio_vespertino.isChecked(),
                "quantidade_aulas": janela.aulas_vespertino.value()
            }
        }

        # =========================================================
        # CAMINHO DO ARQUIVO DE EXCEÇÕES
        # =========================================================

        caminho_excecoes = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "excecoes.json"
        )

        try:

            # -----------------------------------------------------
            # CARREGA EXCEÇÕES EXISTENTES
            # -----------------------------------------------------

            if os.path.exists(caminho_excecoes):

                with open(
                    caminho_excecoes,
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    excecoes = json.load(
                        arquivo
                    )

            else:

                excecoes = {}

            # -----------------------------------------------------
            # VERIFICA SE JÁ EXISTE UMA EXCEÇÃO PARA A DATA
            # -----------------------------------------------------

            if data in excecoes:

                mensagem = QMessageBox(
                    QMessageBox.Question,
                    "Horário especial",
                    f"Já existe uma configuração para {data}.\n\n"
                    "Deseja substituí-la?",
                    QMessageBox.Yes | QMessageBox.No,
                    self
                )

                mensagem.setStyleSheet("""
                    QMessageBox {
                        background-color: #0b1424;
                        color: #f2f5f9;
                        font-family: "Segoe UI";
                    }

                    QMessageBox QLabel {
                        color: #dbe4ef;
                        font-family: "Segoe UI";
                        font-size: 13px;
                        padding: 8px;
                    }

                    QMessageBox QPushButton {
                        min-width: 85px;
                        min-height: 34px;
                        padding: 0px 16px;
                        border-radius: 7px;
                        font-family: "Segoe UI";
                        font-size: 13px;
                        font-weight: 600;
                    }

                    QMessageBox QPushButton#botao_sim {
                    background-color: #0f1b2d;
                    color: #ffffff;
                    border: 2px solid #2196e0;
                    border-radius: 7px;
                    padding: 6px 18px;
                    min-width: 85px;
                    min-height: 34px;
                }

                QMessageBox QPushButton#botao_sim:hover {
                    background-color: #16243a;
                    border: 2px solid #29a3f0;
                }

                QMessageBox QPushButton#botao_sim:pressed {
                    background-color: #0b1424;
                }


                QMessageBox QPushButton#botao_nao {
                    background-color: #0f1b2d;
                    color: #ffffff;
                    border: 2px solid #e53935;
                    border-radius: 7px;
                    padding: 6px 18px;
                    min-width: 85px;
                    min-height: 34px;
                }

                QMessageBox QPushButton#botao_nao:hover {
                    background-color: #261719;
                    border: 2px solid #ff4b47;
                }

                QMessageBox QPushButton#botao_nao:pressed {
                    background-color: #0b1424;
                }
                """)

                botao_sim = mensagem.button(
                    QMessageBox.Yes
                )

                botao_sim.setText(
                    "SIM"
                )

                botao_sim.setFixedSize(
                    100,
                    36
                )

                botao_sim.setStyleSheet("""
                    QPushButton {
                        background-color: #0f1b2d;
                        color: #ffffff;
                        border: 2px solid #2196e0;
                        border-radius: 7px;
                        font-family: "Segoe UI";
                        font-size: 13px;
                        font-weight: 600;
                    }

                    QPushButton:hover {
                        background-color: #16243a;
                        border: 2px solid #29a3f0;
                    }

                    QPushButton:pressed {
                        background-color: #0b1424;
                    }
                """)


                botao_nao = mensagem.button(
                    QMessageBox.No
                )

                botao_nao.setText(
                    "NÃO"
                )

                botao_nao.setFixedSize(
                    100,
                    36
                )

                botao_nao.setStyleSheet("""
                    QPushButton {
                        background-color: #0f1b2d;
                        color: #ffffff;
                        border: 2px solid #e53935;
                        border-radius: 7px;
                        font-family: "Segoe UI";
                        font-size: 13px;
                        font-weight: 600;
                    }

                    QPushButton:hover {
                        background-color: #261719;
                        border: 2px solid #ff4b47;
                    }

                    QPushButton:pressed {
                        background-color: #0b1424;
                    }
                """)

                resposta = mensagem.exec()

                if resposta != QMessageBox.Yes:
                    return

            # -----------------------------------------------------
            # SALVA OU REMOVE A EXCEÇÃO
            # -----------------------------------------------------

            if excecao["ativo"]:

                # Existe pelo menos um turno ativo.
                # Salva a configuração especial.
                excecoes[data] = excecao

            else:

                # Nenhum turno está ativo.
                # Remove completamente a exceção da data.
                excecoes.pop(data, None)

            with open(
                caminho_excecoes,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    excecoes,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

            # -----------------------------------------------------
            # ATUALIZA A EXCEÇÃO NA MEMÓRIA
            # -----------------------------------------------------
            self.excecoes = excecoes

            # -----------------------------------------------------
            # SE A EXCEÇÃO FOR PARA HOJE,
            # ATUALIZA IMEDIATAMENTE OS HORÁRIOS DA SIRENE
            # -----------------------------------------------------
            data_hoje = datetime.now().strftime("%Y-%m-%d")

            if data == data_hoje:
                self.horarios = self.carregar_horarios()
                self.atualizar_programacao_hoje()
                self.ultimo_toque = None
                self.atualizar_interface()

                
            mensagem = QMessageBox(
                QMessageBox.Information,
                "Horário especial",
                f"Exceção para {data} salva com sucesso.",
                QMessageBox.Ok,
                self
            )

            mensagem.setStyleSheet("""
                QMessageBox {
                    background-color: #0b1424;
                    color: #f2f5f9;
                    border: 1px solid #2196e0;
                }

                QMessageBox QLabel {
                    color: #dbe4ef;
                    font-family: "Segoe UI";
                    font-size: 14px;
                    padding: 8px;
                }

                QMessageBox QPushButton {
                    background-color: #0f1b2d;
                    color: #ffffff;
                    border: 2px solid #2196e0;
                    border-radius: 6px;
                    min-width: 90px;
                    min-height: 32px;
                    padding: 0px 14px;
                    font-family: "Segoe UI";
                    font-size: 13px;
                    font-weight: 600;
                }

                QMessageBox QPushButton:hover {
                    background-color: #16243a;
                    border: 2px solid #29a3f0;
                }

                QMessageBox QPushButton:pressed {
                    background-color: #0b1424;
                }
            """)

            mensagem.exec()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível salvar a exceção:\n\n{erro}"
        )

     
    # =============================================================
    # ATUALIZAÇÃO DO RELÓGIO E PRÓXIMO TOQUE
    # =============================================================

    def atualizar_interface(self):

        agora = datetime.now()

        # ---------------------------------------------------------
        # DETECTA ALTERAÇÃO MANUAL DO RELÓGIO
        # ---------------------------------------------------------
        if agora < self.ultima_verificacao_relogio:
            self.ultimo_toque = None
            self.ultimo_aviso = None
            self.aviso_toques_restantes = 0

        self.ultima_verificacao_relogio = agora



        # Verifica se o dia mudou
        dia_atual = agora.strftime("%Y-%m-%d")

        if not hasattr(self, "dia_carregado") or self.dia_carregado != dia_atual:

            self.horarios = self.carregar_horarios()
            self.dia_carregado = dia_atual

            # Atualiza a programação exibida para hoje
            self.atualizar_programacao_hoje()

            # Permite os toques do novo dia
            self.ultimo_toque = None

        # Verifica se chegou o horário de algum toque
        self.verificar_toque(agora)

        # Atualiza relógio
        self.label_relogio.setText(
            agora.strftime("%H:%M:%S")
        )

        # Atualiza data
        self.label_data.setText(
            agora.strftime("%d/%m/%Y")
        )

        # Procura o próximo horário
        proximo = self.obter_proximo_horario(agora)

        if proximo is None:

            self.label_proximo.setText("AMANHÃ")
            self.label_contagem.setText(
                "Aguardando próximo dia de aula"
            )

        else:

            horario, momento = proximo

            self.label_proximo.setText(horario)

            diferenca = momento - agora

            total_segundos = int(
                diferenca.total_seconds()
            )

            if total_segundos < 0:
                total_segundos = 0

            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            segundos = total_segundos % 60

            if horas > 0:

                texto = (
                    f"Faltam "
                    f"{horas:02d}:"
                    f"{minutos:02d}:"
                    f"{segundos:02d}"
                )

            else:

                texto = (
                    f"Faltam "
                    f"{minutos:02d}:"
                    f"{segundos:02d}"
                )

            self.label_contagem.setText(texto)

   
    # =============================================================
    # VERIFICAR TOQUE PROGRAMADO
    # =============================================================

    # =============================================================
    # ATUALIZAR CONFIGURAÇÃO DO AVISO ANTECIPADO
    # =============================================================
    def atualizar_configuracao_aviso(self):

        if self.combo_tempo_aviso.currentText() == "3 minutos":
            self.tempo_aviso = 3
        else:
            self.tempo_aviso = 5

        if self.combo_quantidade_aviso.currentText() == "1 toque":
            self.quantidade_aviso = 1

        elif self.combo_quantidade_aviso.currentText() == "2 toques":
            self.quantidade_aviso = 2

        else:
            self.quantidade_aviso = 3


    def verificar_toque(self, agora):

        # ---------------------------------------------------------
        # AVISO ANTECIPADO
        # ---------------------------------------------------------

        proximo = self.obter_proximo_horario(
            agora
        )

        if proximo is not None:

            horario_proximo, momento_proximo = proximo

            diferenca_segundos = (
                momento_proximo - agora
            ).total_seconds()

            # -----------------------------------------------------
            # DESCOBRE A DESCRIÇÃO DO PRÓXIMO HORÁRIO
            # -----------------------------------------------------

            descricao_proximo = ""

            for turno in [
                "matutino",
                "vespertino"
            ]:

                for item in self.programacao_dia.get(
                    turno,
                    []
                ):

                    if item.get(
                        "horario"
                    ) == horario_proximo:

                        descricao_proximo = item.get(
                            "descricao",
                            ""
                        )

                        break

                if descricao_proximo:
                    break

            # -----------------------------------------------------
            # AVISO SOMENTE PARA:
            # ENTRADA OU RETORNO DO RECREIO
            #
            # 13:30 NÃO RECEBE AVISO
            # -----------------------------------------------------

            if (
                descricao_proximo in [
                    "Entrada / início das aulas",
                    "Retorno do Recreio"
                ]
                and 0 < diferenca_segundos <= (
                    self.tempo_aviso * 60
                )
            ):

                identificador_aviso = (
                    agora.strftime("%Y-%m-%d")
                    + " "
                    + horario_proximo
                )

                ultimo_aviso = getattr(
                    self,
                    "ultimo_aviso",
                    None
                )

                if ultimo_aviso != identificador_aviso:

                    self.ultimo_aviso = (
                        identificador_aviso
                    )

                    
                    # -------------------------------------------------
                    # ATUALIZA O STATUS DURANTE O AVISO
                    # -------------------------------------------------

                    self.label_status.setText(
                        " AVISO ANTECIPADO"
                    )

                    self.label_status.setStyleSheet(
                        "color: #b26a00; "
                        "font-size: 18px; "
                        "font-weight: bold;"
                    )

                    # -------------------------------------------------
                    # REPRODUZ O TOQUE LONGO DE AVISO
                    # -------------------------------------------------

                    

                    arquivo_som = os.path.join(
                        "dados",
                        "sons",
                        "longo_2_bips.wav"
                    )

                    # -------------------------------------------------
                    # REPRODUZ A QUANTIDADE CONFIGURADA
                    # DE TOQUES LONGOS DO AVISO
                    # -------------------------------------------------

                    self.executar_toque_aviso(
                        arquivo_som,
                        max(0, self.quantidade_aviso - 1)
                    )
        # ---------------------------------------------------------
        # VERIFICA O TOQUE OFICIAL
        # ---------------------------------------------------------

        horario_atual = agora.strftime(
            "%H:%M"
        )

        
        for horario in self.horarios:

            if horario == horario_atual:

                identificador_toque = (
                    agora.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )

                if self.ultimo_toque != identificador_toque:

                    # -------------------------------------------------
                    # SE O AVISO ANTECIPADO AINDA ESTIVER ATIVO,
                    # AGUARDA ANTES DE MARCAR O TOQUE OFICIAL.
                    # -------------------------------------------------
                    if (
                        getattr(
                            self,
                            "aviso_toques_restantes",
                            0
                        ) > 0
                    ):
                        break

                    self.ultimo_toque = (
                        identificador_toque
                    )

                    # -------------------------------------------------
                    # IDENTIFICA O TIPO DO TOQUE
                    # -------------------------------------------------

                    tipo_toque = (
                        self.obter_tipo_toque(
                            horario
                        )
                    )

                    # -------------------------------------------------
                    # EXECUTA O TOQUE
                    # -------------------------------------------------

                    self.simular_toque_programado(
                        horario,
                        tipo_toque
                    )

                break


    # =============================================================
    # EXECUTAR TOQUES DO AVISO ANTECIPADO
    # =============================================================
    def executar_toque_aviso(
        self,
        arquivo_som,
        quantidade
    ):

        self.aviso_arquivo_som = arquivo_som
        self.quantidade_aviso_antecipado = quantidade
        self.aviso_toques_restantes = quantidade
        self.tocar_proximo_aviso()

    # =============================================================
    # TOCAR PRÓXIMO AVISO
    # =============================================================
    def tocar_proximo_aviso(self):

        if self.aviso_toques_restantes <= 0:

            self.finalizar_aviso_antecipado()

            return

        # -------------------------------------------------
        # REPRODUZ O TOQUE ATUAL
        # -------------------------------------------------

        winsound.PlaySound(
            self.aviso_arquivo_som,
            winsound.SND_FILENAME |
            winsound.SND_ASYNC
        )
        

        # -------------------------------------------------
        # MOSTRA O TIPO DO ÁUDIO EXECUTADO
        # -------------------------------------------------
        self.label_teste.setText(
            "🔔 TOQUE PROGRAMADO — LONGO"
        )

        QTimer.singleShot(
            2000,
            lambda: self.label_teste.setText(
                "Use o botão ao lado para testar o funcionamento do sistema."
            )
        )

        # -------------------------------------------------
        # REGISTRA QUE UM TOQUE FOI EXECUTADO
        # -------------------------------------------------

        self.aviso_toques_restantes -= 1

        # -------------------------------------------------
        # MOSTRA NO STATUS QUAL TOQUE ESTÁ SENDO EXECUTADO
        # -------------------------------------------------

        self.label_status.setText(
            f" AVISO ANTECIPADO — "
            f"{self.quantidade_aviso_antecipado - self.aviso_toques_restantes}"
            f"/{self.quantidade_aviso}"
        )
        # -------------------------------------------------
        # CALCULA O INTERVALO ENTRE OS TOQUES
        # -------------------------------------------------

        if self.quantidade_aviso > 1:

            intervalo_aviso = (
                (self.tempo_aviso * 60)
                / (self.quantidade_aviso - 1)
            )

        else:

            intervalo_aviso = 0


        # -------------------------------------------------
        # AGUARDA O INTERVALO CALCULADO
        # ANTES DO PRÓXIMO TOQUE
        # -------------------------------------------------

        if self.aviso_toques_restantes > 0:

            QTimer.singleShot(
                int(intervalo_aviso * 1000),
                self.tocar_proximo_aviso
            )

        else:
            # -------------------------------------------------
            # AGUARDA A DURAÇÃO REAL DO ÁUDIO
            # ANTES DE REMOVER A IDENTIFICAÇÃO
            # -------------------------------------------------

            try:
                with wave.open(
                    self.aviso_arquivo_som,
                    "rb"
                ) as arquivo_wav:

                    frames = arquivo_wav.getnframes()
                    taxa = arquivo_wav.getframerate()

                    duracao_audio = (
                        frames / float(taxa)
                    )

            except Exception:
                # Segurança caso não seja possível ler o WAV
                duracao_audio = 1.6

            QTimer.singleShot(
                int((duracao_audio + 0.1) * 1000),
                self.finalizar_aviso_antecipado
            )

    # =============================================================
    # ENCONTRAR PRÓXIMO HORÁRIO
    # =============================================================

    def obter_proximo_horario(self, agora):

        # =========================================================
        # PROCURA UM HORÁRIO AINDA NÃO REALIZADO HOJE
        # =========================================================

        for horario in self.horarios:

            hora, minuto = map(
                int,
                horario.split(":")
            )

            momento = agora.replace(
                hour=hora,
                minute=minuto,
                second=0,
                microsecond=0
            )

            if momento > agora:

                return horario, momento

        # =========================================================
        # NÃO HÁ MAIS HORÁRIOS HOJE
        # PROCURA O PRÓXIMO DIA ATIVO
        # =========================================================

        proximo_dia = self.obter_proximo_dia_ativo(
            agora
        )

        if proximo_dia is None:

            return None

        nome_dia, horario = proximo_dia

        # =========================================================
        # DESCOBRE QUANTOS DIAS FALTAM
        # =========================================================

        dias_semana = [
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta",
            "sabado",
            "domingo"
        ]

        indice_atual = agora.weekday()

        indice_proximo = dias_semana.index(
            nome_dia
        )

        deslocamento = (
            indice_proximo - indice_atual
        ) % 7

        if deslocamento == 0:

            deslocamento = 7

        # =========================================================
        # MONTA A DATA DO PRÓXIMO DIA
        # =========================================================

        data_proximo_dia = (
            agora
            + timedelta(
                days=deslocamento
            )
        )

        # =========================================================
        # MONTA O HORÁRIO COMPLETO
        # =========================================================

        hora, minuto = map(
            int,
            horario.split(":")
        )

        momento = data_proximo_dia.replace(
            hour=hora,
            minute=minuto,
            second=0,
            microsecond=0
        )

        return horario, momento


    # =============================================================
    # ENCONTRAR PRÓXIMO DIA ATIVO
    # =============================================================

    def obter_proximo_dia_ativo(self, agora):

        dias_semana = [
            "segunda",
            "terca",
            "quarta",
            "quinta",
            "sexta",
            "sabado",
            "domingo"
        ]

        caminho_horarios = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "horarios.json"
        )

        try:

            with open(
                caminho_horarios,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados_horarios = json.load(arquivo)

        except Exception as erro:

            print(
                f"Erro ao carregar programação futura: {erro}"
            )

            return None

        caminho_excecoes = os.path.join(
            os.path.dirname(__file__),
            "dados",
            "excecoes.json"
        )

        try:

            if os.path.exists(caminho_excecoes):

                with open(
                    caminho_excecoes,
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    excecoes = json.load(arquivo)

            else:

                excecoes = {}

        except Exception as erro:

            print(
                f"Erro ao carregar exceções futuras: {erro}"
            )

            excecoes = {}

        # Procura os próximos 7 dias.
        for deslocamento in range(1, 8):

            data_candidata = (
                agora
                + timedelta(
                    days=deslocamento
                )
            )

            nome_dia = dias_semana[
                data_candidata.weekday()
            ]

            _, programacao = self.obter_programacao_para_data(
                data_candidata,
                dados_horarios=dados_horarios,
                excecoes=excecoes
            )

            if not programacao.get(
                "ativo",
                True
            ):

                continue

            horarios = []

            for turno in [
                "matutino",
                "vespertino"
            ]:

                for item in programacao.get(
                    turno,
                    []
                ):

                    if item.get(
                        "ativo",
                        True
                    ):

                        horario = item.get(
                            "horario"
                        )

                        if horario:
                            horarios.append(horario)

            if horarios:

                horarios.sort()

                return (
                    nome_dia,
                    horarios[0]
                )

        return None

       

    # =============================================================
    # IDENTIFICAR TIPO DO TOQUE
    # =============================================================

    def obter_tipo_toque(self, horario):

        for turno in [
            "matutino",
            "vespertino"
        ]:

            for item in self.programacao_dia.get(
                turno,
                []
            ):

                if item.get("horario") == horario:

                    descricao = item.get(
                        "descricao",
                        ""
                    )

                    # -------------------------------------------------
                    # ENTRADA
                    # -------------------------------------------------
                    if descricao == "Entrada / início das aulas":
                        return "longo"

                    # -------------------------------------------------
                    # TROCA DE AULA
                    # -------------------------------------------------
                    if descricao == "Troca de aula":
                        return "curto"

                    # -------------------------------------------------
                    # INÍCIO DO RECREIO
                    # -------------------------------------------------
                    if descricao == "Início do recreio":
                        return "longo"

                    # -------------------------------------------------
                    # RETORNO DO RECREIO
                    # -------------------------------------------------
                    if descricao == "Retorno do recreio":
                        return "longo"

                    # -------------------------------------------------
                    # ENCERRAMENTO
                    # -------------------------------------------------
                    if descricao == "Encerramento":
                        return "longo"

        # -------------------------------------------------------------
        # SEGURANÇA:
        # SE NÃO CONSEGUIR IDENTIFICAR,
        # USA TOQUE LONGO
        # -------------------------------------------------------------
        return "longo"


    # =============================================================
    # SIMULAÇÃO DE TOQUE PROGRAMADO
    # =============================================================

    def simular_toque_programado(
        self,
        horario,
        tipo_toque
    ):

        self.label_teste.setText(
            f"🔔 TOQUE PROGRAMADO — {tipo_toque.upper()} "
            f"({horario})"
        )

        self.label_status.setText(
            " TOQUE EM EXECUÇÃO"
        )

        self.label_status.setStyleSheet(
            "color: #b26a00; "
            "font-size: 18px; "
            "font-weight: bold;"
        )

        # ---------------------------------------------------------
        # DEFINE A DURAÇÃO DO TOQUE
        # ---------------------------------------------------------

        if tipo_toque == "curto":
            duracao_toque = 650
        else:
            duracao_toque = 1550

        # ---------------------------------------------------------
        # REPRODUZ O ÁUDIO SEM BLOQUEAR O PROGRAMA
        # ---------------------------------------------------------

        if tipo_toque == "curto":

            arquivo_som = os.path.join(
                "dados",
                "sons",
                "curto_1_bip.wav"
            )

        else:

            arquivo_som = os.path.join(
                "dados",
                "sons",
                "longo_2_bips.wav"
            )

        winsound.PlaySound(
            arquivo_som,
            winsound.SND_FILENAME |
            winsound.SND_ASYNC
        )

        # ---------------------------------------------------------
        # PARA O ÁUDIO APÓS A DURAÇÃO DEFINIDA
        # ---------------------------------------------------------

        QTimer.singleShot(
            duracao_toque,
            lambda: self.finalizar_toque_programado()
        )


    # =============================================================
    # FINALIZAR AVISO ANTECIPADO
    # =============================================================

    def finalizar_aviso_antecipado(self):
        # ---------------------------------------------------------
        # INTERROMPE O ÁUDIO DO AVISO
        # ---------------------------------------------------------
        winsound.PlaySound(
            None,
            0
        )

        

    def finalizar_toque_programado(self):
        # ---------------------------------------------------------
        # INTERROMPE O ÁUDIO ATUAL
        # ---------------------------------------------------------
        winsound.PlaySound(
            None,
            0
        )

        # ---------------------------------------------------------
        # RETORNA O STATUS AO NORMAL
        # ---------------------------------------------------------
        self.label_status.setText(
            " SISTEMA ATIVO"
        )
        self.label_status.setStyleSheet(
            "color: #238636; "
            "font-size: 18px; "
            "font-weight: bold;"
        )

        # ---------------------------------------------------------
        # REMOVE A IDENTIFICAÇÃO DO TOQUE EXECUTADO
        # ---------------------------------------------------------
        self.label_teste.setText(
            "Use o botão ao lado para testar o funcionamento do sistema."
        )

       

    # =============================================================
    # TESTE DA SIRENE
    # =============================================================

    def testar_sirene(self):

        horario = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.label_teste.setText(
            f"🔔 TESTE DE ACIONAMENTO — ÁUDIO ({horario})"
        )

        self.label_status.setText(
            " SIRENE EM TESTE"
        )

        self.label_status.setStyleSheet(
            "color: #b26a00; "
            "font-size: 18px; "
            "font-weight: bold;"
        )

        # Teste de reprodução de áudio WAV

        arquivo_som = os.path.join(
            "dados",
            "sons",
            "longo_2_bips.wav"
        )

        winsound.PlaySound(
            arquivo_som,
            winsound.SND_FILENAME
        )

        QTimer.singleShot(
            3000,
            self.finalizar_teste
        )


    # =============================================================
    # FINALIZAR TESTE
    # =============================================================

    def finalizar_teste(self):

        self.label_teste.setText(
            "Use este botão para testar o funcionamento do sistema."
        )

        self.label_status.setText(
            " SISTEMA ATIVO"
        )

        self.label_status.setStyleSheet(
            "color: #238636; "
            "font-size: 18px; "
            "font-weight: bold;"
        )

# =================================================================
# INÍCIO DO PROGRAMA
# =================================================================

def main():

    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
