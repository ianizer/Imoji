import sys
import pathlib
from typing import cast
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *  # includes QPixmap

DEFAULT_ICON_SIZE = QSize(100, 100)
DEFAULT_COPIED_IMAGE_SIZE = QSize(100, 100)
IMAGE_BUTTON_BORDER_SIZE = QSize(20, 20)


class ImageCopier(QWidget):
    def __init__(self, image_path: pathlib.Path):
        super().__init__()

        self.image_path = image_path

        icon_pixmap: QPixmap = QPixmap(image_path).scaled(
            DEFAULT_ICON_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.render_image(DEFAULT_COPIED_IMAGE_SIZE)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        image_widget = QPushButton()
        image_widget.setMinimumSize(DEFAULT_ICON_SIZE + IMAGE_BUTTON_BORDER_SIZE)
        image_widget.setMaximumSize(DEFAULT_ICON_SIZE + IMAGE_BUTTON_BORDER_SIZE)
        image_widget.setIcon(icon_pixmap)
        image_widget.setIconSize(DEFAULT_ICON_SIZE)

        image_widget.clicked.connect(self.image_clicked)

        main_layout.addWidget(image_widget)

    def render_image(self, new_image_size: QSize):
        """Renders the image to be copied to clipboard when image_clicked() runs.

        Specifically, places the scaled image from the image file into a transparent new_image_size-sized blank canvas for pleasant pasting.

        Stores final rendered image in self.rendered_image.
        """

        scaled_image_pixmap = QPixmap(self.image_path).scaled(
            new_image_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Make a transparent pixmap to place our scaled image inside.

        self.pixmap_render = QPixmap(new_image_size)
        self.pixmap_render.fill(Qt.GlobalColor.transparent)

        # Make a QPainter object so we can place the scaled image in the blank_pixmap.
        image_painter = QPainter(self.pixmap_render)

        # Calculate coords to center the scaled image in the blank canvas.
        # Explanation: new_image_size.width() gives total blank space (on x-axis).
        # scaled_image_pixmap.width() gives space to be occupied (x-axis).
        # Subtracting them gives the space left empty after scaled image is placed.
        # Divide by 2 for equal blank space on left & right.
        # Final result is: (center_x + image_width + center_x) == new_image_size.width()
        center_x = (new_image_size.width() - scaled_image_pixmap.width()) // 2
        center_y = (new_image_size.height() - scaled_image_pixmap.height()) // 2

        image_painter.drawPixmap(center_x, center_y, scaled_image_pixmap)
        image_painter.end()

        self.rendered_image = self.pixmap_render.toImage()

    def image_clicked(self):
        QApplication.clipboard().setImage(self.rendered_image)


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

        # TODO: Maybe make IMAGES_PER_ROW scale with window size.
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
        image_format = QImageReader.imageFormat(str(file))

        # image_format is an empty string if invalid.
        return image_format != ""


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
# 3. Support Animated GIFs?
# 4. Support custom image backgrounds or perhaps
