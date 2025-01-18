from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar, QMessageBox
from CentralWidget import CentralWidget  # Import der benutzerdefinierten Klasse "CentralWidget"

# Die Hauptklasse des Programms, die das Hauptfenster der Anwendung definiert.
class MainWindow(QMainWindow):
    # Benutzerdefinierte Signale:
    # "write_text" wird verwendet, um Text an das zentrale Widget zu senden.
    # "write_font" wird verwendet, um die Schriftart an das zentrale Widget zu senden.
    write_text = pyqtSignal(str)
    write_font = pyqtSignal(QFont)

    # Konstruktor der Klasse. Er wird aufgerufen, wenn ein Objekt von MainWindow erstellt wird.
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # Aufruf des Konstruktors der Basisklasse QMainWindow

        # Initialisieren der Schriftart und der Datei-Dialog-Filter
        self.__font = QFont()  # Standard-Schriftart
        self.__initial_filter = "Default files (*.txt)"  # Filter: Zeige nur .txt-Dateien
        self.__filter = self.__initial_filter + ";;All files (*)"  # Option: Zeige alle Dateien
        self.__directory = ""  # Arbeitsverzeichnis (leer am Anfang)

        # Erstellen des zentralen Widgets (Textanzeige) und Verbinden der Signale
        self.__central_widget = CentralWidget(self)  # Das zentrale Widget
        self.write_text.connect(self.__central_widget.set_text)  # Verbindung: Text an Widget senden
        self.write_font.connect(self.__central_widget.set_font)  # Verbindung: Schriftart an Widget senden

        # Fenster-Titel setzen
        self.setWindowTitle("Mein Texteditor")

        # Statusleiste erstellen (am unteren Rand des Fensters)
        self.setStatusBar(QStatusBar(self))

        # Menüleiste erstellen
        menu_bar = QMenuBar(self)  # Die Menüleiste des Fensters

        # "Files"-Menü erstellen
        files = QMenu("Files", menu_bar)  # Menü "Files"

        # Aktion "Open ..." hinzufügen und mit der Methode "file_open" verbinden
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)

        # Aktion "Save ..." hinzufügen und mit der Methode "file_save" verbinden
        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)

        # Aktion "Copy ..." hinzufügen und mit der Methode "file_copy" verbinden
        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)

        # Aktion "Move ..." hinzufügen und mit der Methode "file_move" verbinden
        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)

        # "Files"-Menü zur Menüleiste hinzufügen
        menu_bar.addMenu(files)

        # "Font"-Menü erstellen
        font = QMenu("Font", menu_bar)  # Menü "Font"

        # Aktion "Font" hinzufügen und mit der Methode "font" verbinden
        action_font = font.addAction("Font")
        action_font.triggered.connect(self.font)

        # "Font"-Menü zur Menüleiste hinzufügen
        menu_bar.addMenu(font)

        # Menüleiste dem Fenster hinzufügen
        self.setMenuBar(menu_bar)

        # Das zentrale Widget als Hauptanzeige des Fensters setzen
        self.setCentralWidget(self.__central_widget)

    # Methode, um eine Datei zu öffnen
    @pyqtSlot()
    def file_open(self):
        # Dialog anzeigen, um eine Datei auszuwählen
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(
            self, "Open File", self.__directory, self.__filter, self.__initial_filter
        )

        # Wenn ein Pfad ausgewählt wurde
        if path:
            self.__directory = path[:path.rfind("/")]  # Verzeichnis aktualisieren
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])  # Statusleiste aktualisieren

            file = QFile(path)  # Datei öffnen

            # Prüfen, ob die Datei im Lesemodus geöffnet werden kann
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                QMessageBox.information(self, "Unable to open file", file.errorString())  # Fehlerdialog
                return

            stream = QTextStream(file)  # Dateiinhalt lesen
            text_in_file = stream.readAll()  # Gesamten Text lesen

            self.write_text.emit(text_in_file)  # Text an das zentrale Widget senden

            file.close()  # Datei schließen

    # Methode, um eine Datei zu speichern
    @pyqtSlot()
    def file_save(self):
        # Dialog anzeigen, um einen Speicherort auszuwählen
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(
            self, "Save File", self.__directory, self.__filter, self.__initial_filter
        )

        # Wenn ein Pfad ausgewählt wurde
        if path:
            self.__directory = path[:path.rfind("/")]  # Verzeichnis aktualisieren
            self.statusBar().showMessage("File saved: " + path[path.rfind("/") + 1:])  # Statusleiste aktualisieren

            file = QFile(path)  # Datei öffnen

            # Prüfen, ob die Datei im Schreibmodus geöffnet werden kann
            if not file.open(QIODevice.OpenModeFlag.WriteOnly):
                QMessageBox.information(self, "Unable to save file", file.errorString())  # Fehlerdialog
                return

            stream = QTextStream(file)  # Dateiinhalt schreiben
            stream << self.__central_widget.get_text()  # Text aus dem zentralen Widget schreiben

            stream.flush()  # Sicherstellen, dass alles geschrieben wurde
            file.close()  # Datei schließen

    # Platzhalter für die Funktion "Kopieren"
    @pyqtSlot()
    def file_copy(self):
        pass

    # Platzhalter für die Funktion "Verschieben"
    @pyqtSlot()
    def file_move(self):
        pass

    # Methode, um die Schriftart zu ändern
    @pyqtSlot()
    def font(self):
        # Dialog anzeigen, um eine Schriftart auszuwählen
        [changed_font, changed] = QFontDialog.getFont(self.__font, self, "Select your font")

        # Wenn die Schriftart geändert wurde
        if changed:
            self.__font = changed_font  # Neue Schriftart speichern
            self.write_font.emit(self.__font)  # Schriftart an das zentrale Widget senden
