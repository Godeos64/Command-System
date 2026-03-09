import sys
from typing import cast # Required for the strict type fix
import keyboard
from PyQt5 import QtCore, QtWidgets, QtGui

# --- LOGIC IMPORTS ---
from Logic.Parser import parse_request
from Logic.Command_Checker import load_commands, execute_command

class SearchBar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # --- Configuration ---
        self.setWindowTitle("Floating Search Bar")
        self.resize(500, 50)
        
        # FIX: Use 'cast' to tell Pylance that the result of '|' is indeed WindowFlags
        self.setWindowFlags(
            cast(
                QtCore.Qt.WindowFlags,
                QtCore.Qt.WindowType.FramelessWindowHint | 
                QtCore.Qt.WindowType.WindowStaysOnTopHint | 
                QtCore.Qt.WindowType.Tool
            )
        )
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # --- Theme Setup ---
        self.themes = {
            "Red":     {"accent": "#FF0000", "bg": "#1A0000"},
            "Green":   {"accent": "#00FF00", "bg": "#001A00"},
            "Blue":    {"accent": "#0078D7", "bg": "#001A33"},
            "Purple":  {"accent": "#9B59B6", "bg": "#1A001A"},
            "Orange":  {"accent": "#FF8C00", "bg": "#1A0F00"},
            "Yellow":  {"accent": "#F1C40F", "bg": "#1A1800"},
            "Cyan":    {"accent": "#00FFFF", "bg": "#001A1A"},
            "Magenta": {"accent": "#FF00FF", "bg": "#1A001A"},
            "Lime":    {"accent": "#32CD32", "bg": "#0A1A0A"},
            "Pink":    {"accent": "#FFC0CB", "bg": "#1A0A10"},
            "Teal":    {"accent": "#008080", "bg": "#001010"},
            "Indigo":  {"accent": "#4B0082", "bg": "#0D001A"},
            "Coral":   {"accent": "#FF7F50", "bg": "#1A0D0A"},
            "Sky":     {"accent": "#87CEEB", "bg": "#0A1520"},
            "Gold":    {"accent": "#FFD700", "bg": "#1A1600"},
            "Grey":    {"accent": "#A9A9A9", "bg": "#1A1A1A"},
        }
        
        self.current_theme_index = 1 # Default to Blue
        self.theme_keys = list(self.themes.keys())
        
        self.init_ui()
        self.apply_theme()

        # --- Global Hotkey (Toggle Visibility) ---
        keyboard.add_hotkey('ctrl+shift+f', self.toggle_visibility)
        
        self.center()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # The Search Input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("🔍 Type to search... (Ctrl+Shift+F to hide)")
        self.search_input.returnPressed.connect(self.perform_search)
        
        # Context Menu
        self.search_input.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        change_theme_action = QtWidgets.QAction("Next Theme (Right Click)", self)
        change_theme_action.triggered.connect(self.next_theme)
        self.search_input.addAction(change_theme_action)
        
        layout.addWidget(self.search_input)
        self.setLayout(layout)

    def apply_theme(self):
        theme_name = self.theme_keys[self.current_theme_index]
        colors = self.themes[theme_name]
        
        style = f"""
            QLineEdit {{
                background-color: rgba(30, 30, 30, 230);
                color: #FFFFFF;
                border: 2px solid {colors['accent']};
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 16px;
                font-family: Segoe UI;
            }}
            QLineEdit:focus {{
                border: 2px solid white;
                background-color: rgba(40, 40, 40, 240);
            }}
        """
        self.search_input.setStyleSheet(style)
        print(f"Theme changed to: {theme_name}")

    def next_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_keys)
        self.apply_theme()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            print("Search bar hidden")
        else:
            self.show()
            self.search_input.setFocus()
            self.search_input.selectAll()
            print("Search bar visible")

    def perform_search(self):
        # --- INTEGRATED LOGIC ---
        query = self.search_input.text()
        if query:
            parsed_request = parse_request(query)
            execute_command(parsed_request)

    def center(self):
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            qr = self.frameGeometry()
            qr.moveCenter(screen_geometry.center())
            self.move(qr.topLeft())

    # --- Draggable Logic ---
    def mousePressEvent(self, a0):
        if a0 is not None:
            self.oldPos = a0.globalPos()

    def mouseMoveEvent(self, a0):
        if a0 is not None:
            delta = QtCore.QPoint(a0.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = a0.globalPos()

if __name__ == "__main__":
    # --- LOAD COMMANDS ON STARTUP ---
    load_commands()
    
    app = QtWidgets.QApplication(sys.argv)
    
    # Dark Palette
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.GlobalColor.white)
    app.setPalette(dark_palette)
    
    window = SearchBar()
    window.show()
    
    sys.exit(app.exec_())