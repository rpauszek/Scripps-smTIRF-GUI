# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
Single-Molecule TIRF Viewer App
"""
from PyQt5.QtWidgets import QApplication, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from collections import OrderedDict

from smtirf import gui

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
class SMTirfViewerApp(gui.SMTirfMainWindow):

    def __init__(self, **kwargs):
        super().__init__(title="smTIRF Analysis", **kwargs)
        self.setup_toolbar()
        self.switch_app("results")

    def setup_toolbar(self):
        toolbar = self.addToolBar("Main")
        gui.add_toolbar_button(toolbar, "microscope", "Viewer", lambda: self.switch_app("viewer"))
        gui.add_toolbar_button(toolbar, "polyline", "Results", lambda: self.switch_app("results"))
        gui.add_toolbar_button(toolbar, "settings", "Settings", None)
        gui.format_toolbar(toolbar)

    def switch_app(self, appType):
        # try:
        #     self.removeToolBar(self.pnl.toolbar)
        # except AttributeError:
        #     pass

        if appType == "viewer":
            self.pnl = TraceViewerSubApp(parent=self)
        elif appType == "results":
            self.pnl = ExperimentResultsSubApp(parent=self)
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
        gui.add_toolbar_button(toolbar, "merge", "Merge", None)
        toolbar.addSeparator()
        # ======================================================================
        gui.add_toolbar_button(toolbar, "open", "Open", None, shortcut="Ctrl+O")
        gui.add_toolbar_button(toolbar, "save", "Save", None, shortcut="Ctrl+S")
        toolbar.addSeparator()
        # ======================================================================
        gui.add_toolbar_button(toolbar, "ecg", "Baseline", None)
        toolbar.addSeparator()
        # ======================================================================
        actions = OrderedDict([("Index", None),
                               ("Selected", None),
                               ("Cluster", None),
                               ("Correlation", None)])
        gui.add_toolbar_menu(toolbar, "sort_alpha", "Sort", actions)
        actions = OrderedDict([("Select All", None),
                               ("Select None", None)])
        gui.add_toolbar_menu(toolbar, "check_all", "Select", actions)
        toolbar.addSeparator()
        # ======================================================================
        actions = OrderedDict([("Reset Offsets", None),
                               ("Reset Limits", None)])
        gui.add_toolbar_menu(toolbar, "ruler", "Attributes", actions)
        gui.format_toolbar(toolbar)
        self.parent().addToolBar(toolbar)

# ==============================================================================
# EXPERIMENT RESULTS
# ==============================================================================
class ExperimentResultsSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        toolbar = QtWidgets.QToolBar("Results", parent=self)
        gui.add_toolbar_button(toolbar, "histogram", "State Populations", None)
        gui.add_toolbar_button(toolbar, "tdp", "TDP", None)
        gui.add_toolbar_button(toolbar, "kinetics", "Kinetics", None)
        toolbar.addSeparator()
        gui.format_toolbar(toolbar)
        self.parent().addToolBar(toolbar)



# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = SMTirfViewerApp()
    win.show()
    sys.exit(app.exec_())
