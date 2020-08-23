# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
Single-Molecule TIRF Viewer App
"""
from PyQt5.QtWidgets import QApplication, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from smtirf import gui

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
class SMTirfViewerApp(gui.SMTirfMainWindow):

    def __init__(self, **kwargs):
        super().__init__(title="smTIRF Analysis", **kwargs)
        self.setup_toolbar()
        self.switch_app("viewer")

    def setup_toolbar(self):
        toolbar = self.addToolBar("Main")
        gui.add_toolbar_button(toolbar, "microscope", "Viewer", None)
        gui.add_toolbar_button(toolbar, "polyline", "Results", None)
        gui.add_toolbar_button(toolbar, "settings", "Settings", None)
        gui.format_toolbar(toolbar)

    def switch_app(self, appType):
        # try:
        #     self.removeToolBar(self.pnl.toolbar)
        # except AttributeError:
        #     pass

        if appType == "viewer":
            self.pnl = TraceViewerSubApp(parent=self)
            # if self.controller.expt is not None:
            #     self.controller.experimentLoaded.emit(self.controller.expt)
        # elif appType == "analysis":
        #     self.pnl = ExperimentAnalysisSubApp(parent=self)
        self.setCentralWidget(self.pnl)

# ==============================================================================
# TRACE VIEWER
# ==============================================================================
class TraceViewerSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        toolbar = QtWidgets.QToolBar("Experiment", parent=self)
        gui.add_toolbar_button(toolbar, "download", "Import", None)
        gui.format_toolbar(toolbar)
        self.parent().addToolBar(toolbar)



# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = SMTirfViewerApp()
    win.show()
    sys.exit(app.exec_())
