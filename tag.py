from aqt.qt import *
class ClosableTag(QWidget):
    closed = pyqtSignal(str)

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(200)
        self.tag = text

        self.layout = QHBoxLayout()

        self.label = QLabel(text)
        self.close_button = QPushButton('x')
        self.close_button.setFixedWidth(20)
        self.close_button.clicked.connect(self.close_tag)
        self.close_button.setFlat(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(
            """
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                color: red;
            }
        """
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define background color and border color
        bg_color = QColor('#f0f0f0')
        border_color = QColor('#000000')

        # Define border pen
        pen = painter.pen()
        pen.setColor(border_color)
        pen.setWidth(1)
        painter.setPen(pen)

        # Draw background and border
        painter.setBrush(bg_color)
        painter.drawRoundedRect(self.rect(), 5, 5)

    def close_tag(self):
        self.setParent(None)
        self.closed.emit(self.tag)
        self.deleteLater()