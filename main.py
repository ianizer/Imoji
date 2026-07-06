import sys
import pathlib
from typing import cast
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *  # includes QPixmap
from PIL import Image  # To check if valid images.


class ImageCopier(QWidget):
    def __init__(self, image_path: pathlib.Path):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Can use a customized label (better image support but harder to code) instead of a button.
        image = QPixmap(image_path)
        image = image.scaled(50, 50, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)

        image_widget = QPushButton()
        image_widget.setMinimumSize(70, 70)
        image_widget.setMaximumSize(70, 70)
        image_widget.setIcon(image)
        image_widget.setIconSize(QSize(50, 50))

        image_widget.clicked.connect(self.image_clicked)

        main_layout.addWidget(image_widget)

    def image_clicked(self):
        # Casted so autocomplete works properly.
        sender = cast(QPushButton, self.sender())

        btn_icon = sender.icon()
        btn_icon = btn_icon.pixmap(50, 50)

        QApplication.clipboard().setImage(btn_icon.toImage())


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

        images_layout = QGridLayout()
        images_layout.setSpacing(10)

        # Add directory & file selection logic later. For now we use script's dir.
        example_dir = pathlib.Path(__file__).resolve()

        IMAGES_PER_ROW = 4
        images_added = 0
        row, column = 0, 0

        for file in example_dir.parent.iterdir():
            if self.is_image(file):
                new_image_widget = ImageCopier(file)

                images_layout.addWidget(
                    new_image_widget,
                    row,
                    column,
                )

                images_added += 1
                column = (column + 1) % IMAGES_PER_ROW
                if images_added % IMAGES_PER_ROW == 0:
                    row += 1

        central_layout.addLayout(images_layout)

    def is_image(self, file: pathlib.Path) -> bool:
        try:
            with Image.open(file) as image:
                image.verify()
            return True
        except:
            return False


# This block only runs if the module/file is run directly, not imported.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Imoji()
    window.show()
    sys.exit(app.exec())


# IDEAS:
# 1. Make a file dialog button for selecting both folders and individual images.
# 2. Save the individual image paths and folders to a file for reading later ("settings.json" or something).
#    Automatically load this settings file on launch.  If deleted, load default settings.
# 3. For each selected image file, and for each image file in the selected folder, place a custom image widget (make a seperate class for these image widgets).
#    Image widgets copy the image displayed. Perhaps as a square, fixed-size image.
#    Number of image widgets per row, and size of them, TBD by experimentation.
