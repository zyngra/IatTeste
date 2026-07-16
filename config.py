from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox,
    QMessageBox,
)
from qgis.core import QgsSettings
from .integracao_sheets import GerenciaSheets
from .teste_login import test_login


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.btn_login = QPushButton("Login no Google")
        self.btn_login.clicked.connect(self.login_google)
        layout.addWidget(self.btn_login)

        layout.addWidget(QLabel("ID da Planilha:"))
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Ex: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
        layout.addWidget(self.input_id)

        layout.addWidget(QLabel("Nome da Aba:"))
        self.input_aba = QLineEdit()
        self.input_aba.setPlaceholderText("Ex: Seu nome")
        layout.addWidget(self.input_aba)

        layout.addWidget(QLabel("Nome da coluna de status:"))
        self.input_coluna_status = QLineEdit()
        self.input_coluna_status.setPlaceholderText("Ex: nm_status_tramitacao")
        layout.addWidget(self.input_coluna_status)

        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar_dados)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

        self.carregar_dados()

    def login_google(self):
        try:
            credenciais = test_login()
            if credenciais and credenciais.valid:
                QMessageBox.information(
                    self, "Login bem-sucedido", "Login no Google realizado com sucesso!"
                )
            else:
                QMessageBox.warning(
                    self, "Erro de Login", "Não foi possível realizar o login no Google."
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Erro de Login", f"Ocorreu um erro durante o login: {str(e)}"
            )

    def carregar_dados(self):
        settings = QgsSettings()
        self.input_id.setText(settings.value("IatTeste/id_planilha", ""))
        self.input_aba.setText(settings.value("IatTeste/nome_aba", ""))
        self.input_coluna_status.setText(settings.value("IatTeste/coluna_status", ""))

    def salvar_dados(self) -> None:
        settings = QgsSettings()
        settings.setValue("IatTeste/id_planilha", self.input_id.text())
        settings.setValue("IatTeste/nome_aba", self.input_aba.text())
        settings.setValue("IatTeste/coluna_status", self.input_coluna_status.text())
        self.accept()
