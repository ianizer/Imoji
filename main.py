import sys
from typing import cast
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *  # includes QPixmap


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

        # Image displays section.
        # Make custom widget later that does all this work on instantiation of the widget.

        images_layout = QVBoxLayout()
        images_layout.setSpacing(10)

        # Make an image-display widget.
        # Can use a customized label (better image support but harder to code) instead of a button.
        pic_test = QPixmap("Timestamper icon.png")
        pic_test = pic_test.scaled(
            50, 50, aspectMode=Qt.AspectRatioMode.KeepAspectRatio
        )

        image_widget = QPushButton()
        image_widget.setMinimumSize(70, 70)
        image_widget.setMaximumSize(70, 70)
        image_widget.setIcon(pic_test)
        image_widget.setIconSize(QSize(50, 50))

        image_widget.clicked.connect(self.image_clicked)

        images_layout.addWidget(image_widget)

        central_layout.addLayout(images_layout)

    def image_clicked(self):
        sender = cast(QPushButton, self.sender())

        btn_icon = sender.icon()
        btn_icon = btn_icon.pixmap(50, 50)

        QApplication.clipboard().setImage(btn_icon.toImage())


# This block only runs if the module/file is run directly, not imported.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Imoji()
    window.show()
    sys.exit(app.exec())
