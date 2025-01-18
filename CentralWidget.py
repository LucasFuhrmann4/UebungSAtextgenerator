from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton

# Die CentralWidget-Klasse ist ein benutzerdefiniertes Widget, das eine Textbearbeitungsoberfläche bereitstellt.
class CentralWidget(QWidget):
    def __init__(self, parent=None):
        # Der Konstruktor der Klasse. Er initialisiert das Widget und dessen Layout.
        super(CentralWidget, self).__init__(parent)

        # Ein horizontaler Layout-Container für die Schaltflächen "Bold", "Italic" und "Underline".
        bar_layout = QHBoxLayout()

        # Erstellen von drei Schaltflächen für verschiedene Textformatierungen.
        self.__pushbutton_bold = QPushButton('Bold')
        self.__pushbutton_italic = QPushButton('Italic')
        self.__pushbutton_underline = QPushButton('Underline')

        # Verbinden der Schaltflächen mit den entsprechenden Methoden, die ihre Funktionalität ausführen.
        self.__pushbutton_bold.pressed.connect(self.__bold)
        self.__pushbutton_italic.pressed.connect(self.__italic)
        self.__pushbutton_underline.pressed.connect(self.__underline)

        # Hinzufügen der Schaltflächen zum horizontalen Layout.
        bar_layout.addWidget(self.__pushbutton_bold)
        bar_layout.addWidget(self.__pushbutton_italic)
        bar_layout.addWidget(self.__pushbutton_underline)

        # Erstellen eines Texteditors, in dem der Benutzer Text eingeben und bearbeiten kann.
        self.__text_edit = QTextEdit()

        # Ein vertikales Layout, das das gesamte Widget strukturiert.
        layout = QVBoxLayout()

        # Hinzufügen des horizontalen Layouts (mit den Schaltflächen) und des Texteditors zum vertikalen Layout.
        layout.addLayout(bar_layout)
        layout.addWidget(self.__text_edit)

        # Anwenden des Layouts auf das Hauptwidget.
        self.setLayout(layout)

    # Methode, um Text im Texteditor zu setzen.
    @pyqtSlot(str)
    def set_text(self, text):
        self.__text_edit.setText(text)

    # Methode, um den aktuellen Text aus dem Texteditor abzurufen.
    def get_text(self):
        return self.__text_edit.toPlainText()

    # Methode, um die Schriftart des Texteditors zu setzen.
    @pyqtSlot(QFont)
    def set_font(self, font):
        self.__text_edit.setFont(font)

    # Private Methode, die die "Bold"-Funktionalität umsetzt.
    @pyqtSlot()
    def __bold(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Textcursor im Texteditor.
        format = cursor.charFormat()  # Holt das aktuelle Format der Zeichen, auf die der Cursor zeigt.

        font = self.__pushbutton_bold.font()  # Holt die Schriftart der "Bold"-Schaltfläche.

        # Überprüfen, ob der Text bereits fett ist. Wenn ja, wird er normal, andernfalls fett.
        if self.__pushbutton_bold.font().bold():
            format.setFontWeight(QFont.Weight.Normal)
            font.setBold(False)
        else:
            format.setFontWeight(QFont.Weight.Bold)
            font.setBold(True)

        # Anwenden des neuen Formats auf den Text und Aktualisieren des Cursors.
        cursor.setCharFormat(format)
        self.__text_edit.setTextCursor(cursor)

        # Aktualisieren der Schriftart der Schaltfläche, um den Status anzuzeigen.
        self.__pushbutton_bold.setFont(font)

    # Private Methode, die die "Italic"-Funktionalität umsetzt.
    @pyqtSlot()
    def __italic(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Textcursor im Texteditor.
        format = cursor.charFormat()  # Holt das aktuelle Format der Zeichen, auf die der Cursor zeigt.

        font = self.__pushbutton_italic.font()  # Holt die Schriftart der "Italic"-Schaltfläche.

        # Überprüfen, ob der Text bereits kursiv ist. Wenn ja, wird er normal, andernfalls kursiv.
        if self.__pushbutton_italic.font().italic():
            format.setFontItalic(False)
            font.setItalic(False)
        else:
            format.setFontItalic(True)
            font.setItalic(True)

        # Anwenden des neuen Formats auf den Text und Aktualisieren des Cursors.
        cursor.setCharFormat(format)
        self.__text_edit.setTextCursor(cursor)

        # Aktualisieren der Schriftart der Schaltfläche, um den Status anzuzeigen.
        self.__pushbutton_italic.setFont(font)

    # Private Methode, die die "Underline"-Funktionalität umsetzt.
    @pyqtSlot()
    def __underline(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Textcursor im Texteditor.
        format = cursor.charFormat()  # Holt das aktuelle Format der Zeichen, auf die der Cursor zeigt.

        font = self.__pushbutton_underline.font()  # Holt die Schriftart der "Underline"-Schaltfläche.

        # Überprüfen, ob der Text bereits unterstrichen ist. Wenn ja, wird er normal, andernfalls unterstrichen.
        if self.__pushbutton_underline.font().underline():
            format.setFontUnderline(False)
            font.setUnderline(False)
        else:
            format.setFontUnderline(True)
            font.setUnderline(True)

        # Anwenden des neuen Formats auf den Text und Aktualisieren des Cursors.
        cursor.setCharFormat(format)
        self.__text_edit.setTextCursor(cursor)

        # Aktualisieren der Schriftart der Schaltfläche, um den Status anzuzeigen.
        self.__pushbutton_underline.setFont(font)
