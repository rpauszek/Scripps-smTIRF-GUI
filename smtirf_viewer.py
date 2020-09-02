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
        self.switch_app("viewer")

    def setup_toolbar(self):
        toolbar = self.addToolBar("Main")
        gui.add_toolbar_button(toolbar, "microscope", "Viewer", lambda: self.switch_app("viewer"))
        gui.add_toolbar_button(toolbar, "polyline", "Results", lambda: self.switch_app("results"))
        gui.add_toolbar_button(toolbar, "settings", "Settings", None)
        gui.format_toolbar(toolbar)

    def switch_app(self, appType):
        try:
            self.pnl.unbind()
        except AttributeError:
            pass

        if appType == "viewer":
            self.pnl = TraceViewerSubApp(toolbarName="Experiment", parent=self)
            # if self.controller.expt is not None:
            #     self.controller.experimentLoaded.emit(self.controller.expt)
        elif appType == "results":
            self.pnl = ExperimentResultsSubApp(toolbarName="Results", parent=self)
        self.setCentralWidget(self.pnl)

# ==============================================================================
# TRACE VIEWER
# ==============================================================================
class TraceViewerSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        gui.add_toolbar_button(self.toolbar, "download", "Import", self.controller.import_experiment_from_pma)
        gui.add_toolbar_button(self.toolbar, "merge", "Merge", None)
        self.toolbar.addSeparator()
        # ======================================================================
        gui.add_toolbar_button(self.toolbar, "open", "Open", self.controller.open_experiment, shortcut="Ctrl+O")
        gui.add_toolbar_button(self.toolbar, "save", "Save", None, shortcut="Ctrl+S")
        self.toolbar.addSeparator()
        # ======================================================================
        gui.add_toolbar_button(self.toolbar, "ecg", "Baseline", None)
        self.toolbar.addSeparator()
        # ======================================================================
        actions = OrderedDict([("Index", self.controller.sort_by_index),
                               ("Selected", self.controller.sort_by_selected),
                               ("Cluster", self.controller.sort_by_cluster),
                               ("Correlation", self.controller.sort_by_correlation)])
        gui.add_toolbar_menu(self.toolbar, "sort_alpha", "Sort", actions)
        actions = OrderedDict([("Select All", self.controller.select_all),
                               ("Select None", self.controller.select_none)])
        gui.add_toolbar_menu(self.toolbar, "check_all", "Select", actions)
        self.toolbar.addSeparator()
        # ======================================================================
        actions = OrderedDict([("Reset Offsets", None),
                               ("Reset Limits", None)])
        gui.add_toolbar_menu(self.toolbar, "ruler", "Attributes", actions)
        gui.format_toolbar(self.toolbar)
        self.parent().addToolBar(self.toolbar)
        self.toolbar.addAction(gui.widgets.ToggleSelectionAction(self.toolbar))

    def layout(self):
        mainBox = QtWidgets.QVBoxLayout()
        hboxTrace = QtWidgets.QHBoxLayout()
        hboxNav = QtWidgets.QHBoxLayout()

        hboxTrace.addWidget(gui.widgets.TraceIdLabel(self.controller))
        hboxTrace.addWidget(gui.widgets.CorrelationLabel(self.controller))
        hboxTrace.addItem(QtWidgets.QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed))
        hboxTrace.addWidget(gui.widgets.CoordinateLabel(self.controller))
        grpTrace = QtWidgets.QGroupBox("Trace")
        grpTrace.setLayout(hboxTrace)

        hboxNav.addWidget(gui.widgets.NavBar(self.controller), stretch=1)
        hboxNav.addWidget(gui.widgets.SelectedItemsCounter(self.controller))

        mainBox.addWidget(grpTrace)
        mainBox.addWidget(gui.plots.TraceViewerPlot(self.controller), stretch=1)
        mainBox.addLayout(hboxNav)

        self.setLayout(mainBox)

# ==============================================================================
# EXPERIMENT RESULTS
# ==============================================================================
class ExperimentResultsSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        gui.add_toolbar_button(self.toolbar, "histogram", "State Populations", None)
        gui.add_toolbar_button(self.toolbar, "tdp", "TDP", None)
        gui.add_toolbar_button(self.toolbar, "kinetics", "Kinetics", None)
        self.toolbar.addSeparator()
        gui.format_toolbar(self.toolbar)
        self.parent().addToolBar(self.toolbar)



# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = SMTirfViewerApp()
    win.show()
    sys.exit(app.exec_())
