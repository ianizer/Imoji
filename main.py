import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


class Imoji(QMainWindow):
    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        # Make QWidget to be able to place other widgets on it.
        container_widget = QWidget()
        self.setCentralWidget(container_widget)

        # Apply layout to new QWidget.
        central_layout = QVBoxLayout()
        central_layout.setSpacing(30)
        container_widget.setLayout(central_layout)

        # Example sub-layout for widgets to be placed along central layout.

        # First, make sub-layout and set spacing as desired.
        # (5px spacing chosen for simple label-widget pairs.)
        example_sublayout = QVBoxLayout()
        example_sublayout.setSpacing(5)

        # Now create and place label & other widget (button) as normal.
        label = QLabel("<i>Test button label:</i>")
        example_sublayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignBottom)

        button = QPushButton("Test Button")
        example_sublayout.addWidget(button)

        # Then place the sub-layout on the main/central layout to make it appear.
        central_layout.addLayout(example_sublayout)


# This block only runs if the module/file is run directly, not imported.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Imoji()
    window.show()
    sys.exit(app.exec())
