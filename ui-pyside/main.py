import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLineEdit, QLabel
from backend.db.schema import init_db
from backend.db.repo import Repo
from backend.parsers.ebom_parser import parse_ebom
from backend.services.pipeline import process_file

DB_PATH = "data/app.db"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creo → Odoo Middleware (PoC)")
        init_db(DB_PATH)
        self.repo = Repo(DB_PATH)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Module (Photostation/Standard):"))
        self.module = QLineEdit("Photostation")
        layout.addWidget(self.module)

        self.btn = QPushButton("Open EBOM (txt/csv)")
        self.btn.clicked.connect(self.open_file)
        layout.addWidget(self.btn)

        self.out = QTextEdit()
        self.out.setReadOnly(True)
        layout.addWidget(self.out)

        self.setLayout(layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select EBOM file", "", "EBOM (*.csv *.txt)")
        if not path:
            return
        rows = parse_ebom(path)
        processed = process_file(self.repo, module=self.module.text().strip(), ebom_rows=rows)
        self.out.clear()
        for r in processed:
            self.out.append(f"{r.name} | {r.item_type} | {r.status} | ext={r.external_id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.resize(900, 500)
    w.show()
    sys.exit(app.exec())
