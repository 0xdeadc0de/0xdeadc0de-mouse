from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys
app = QtWidgets.QApplication(sys.argv)

screen = app.primaryScreen()
print('Screen: %s' % screen.name())
size = screen.size()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))
w, h = rect.width(), rect.height()
ow, oh = rect.width() - size.width(), rect.height() - size.height()
class Panel(QtWidgets.QMainWindow):
    progress = QtCore.pyqtSignal()
    reset = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.progress.connect(self.draw)
        self.reset.connect(self.clear)
#        self.setGeometry(0, 0, w, h)

        self.canvas = QtGui.QPixmap(w, h)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.setWindowOpacity(0.5)

    def draw(self, x, y, ow, oh):
        self.clear()
        self.painter = QtGui.QPainter(self.label.pixmap())
        #self.painter.begin()
        self.painter.setPen(Qt.red)
        self.painter.drawLine(x[0]-ow, y[1]+oh, x[2]-ow, y[1]+oh)
        self.painter.drawLine(x[1]-ow, y[0]+oh, x[1]-ow, y[2]+oh)
        self.painter.end()
        self.update()
    
    def clear(self):
        self.canvas = None
        self.canvas = QtGui.QPixmap(w, h)
        self.label.setPixmap(self.canvas)
        self.update()

panel = Panel()

def draw(x, y):
    panel.draw(x, y, ow, oh)
def clear():
    global panel
    panel.reset.emit()

def hide():
    global panel
    global enabled
    enabled = False
    panel.hide()

def show():
    global panel
    global enabled
    enabled = True
    panel.showMaximized()

def toggle():
    global panel, enabled
    if enabled:
        panel.hide()
    else:
        panel.showMaximized()
    enabled = not enabled

def getboundries():
    global app
    global w, h
    rect = app.primaryScreen().availableGeometry()
    w, h = rect.width(), rect.height()
    return (w, h)
