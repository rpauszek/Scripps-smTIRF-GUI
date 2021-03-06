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

    def set_title(self, path):
        if path is None:
            path = "*"
        self.setWindowTitle(f"smTIRF Analysis ({path})")

    def switch_app(self, appType):
        try:
            self.pnl.unbind()
        except AttributeError:
            pass

        if appType == "viewer":
            self.pnl = TraceViewerSubApp(toolbarName="Experiment", parent=self)
            if self.controller.expt is not None:
                self.controller.experimentLoaded.emit(self.controller.expt)
                self.controller.update_index(self.controller.index)
        elif appType == "results":
            self.pnl = ExperimentResultsSubApp(toolbarName="Results", parent=self)
        self.setCentralWidget(self.pnl)

# ==============================================================================
# TRACE VIEWER
# ==============================================================================
class TraceViewerSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        gui.add_toolbar_button(self.toolbar, "download", "Import", self.controller.import_experiment_from_pma)
        gui.add_toolbar_button(self.toolbar, "merge", "Merge", self.controller.merge_experiments)
        gui.add_toolbar_button(self.toolbar, "open", "Open", self.controller.open_experiment, shortcut="Ctrl+O")
        gui.add_toolbar_button(self.toolbar, "save", "Save", self.controller.save_experiment, shortcut="Ctrl+S")
        self.toolbar.addSeparator()
        # ======================================================================
        gui.add_toolbar_button(self.toolbar, "ecg", "Baseline", self.controller.detect_baseline)
        gui.add_toolbar_button(self.toolbar, "process", "Train All", self.controller.train_all_traces)
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
        hboxTop = QtWidgets.QHBoxLayout()
        hboxTrace = QtWidgets.QHBoxLayout()
        hboxModel = QtWidgets.QHBoxLayout()
        hboxNav = QtWidgets.QHBoxLayout()

        hboxTrace.addWidget(gui.widgets.ExportTraceButton(self.controller))
        hboxTrace.addWidget(gui.widgets.TraceIdLabel(self.controller))
        hboxTrace.addWidget(gui.widgets.CorrelationLabel(self.controller))
        hboxTrace.addItem(QtWidgets.QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed))
        hboxTrace.addWidget(gui.widgets.CoordinateLabel(self.controller))
        hboxTrace.setContentsMargins(10,0,10,0)
        grpTrace = QtWidgets.QGroupBox("Trace")
        grpTrace.setLayout(hboxTrace)

        hboxModel.addWidget(gui.widgets.TrainModelButton(self.controller))
        hboxModel.setContentsMargins(0,0,0,0)
        grpModel = QtWidgets.QGroupBox("Model")
        grpModel.setLayout(hboxModel)

        hboxTop.addWidget(grpTrace)
        hboxTop.addWidget(grpModel)

        hboxNav.addWidget(gui.widgets.NavBar(self.controller), stretch=1)
        hboxNav.addWidget(gui.widgets.SelectedItemsCounter(self.controller))

        mainBox.addLayout(hboxTop)
        mainBox.addWidget(gui.plots.TraceViewerPlot(self.controller), stretch=1)
        mainBox.addLayout(hboxNav)

        self.setLayout(mainBox)

# ==============================================================================
# EXPERIMENT RESULTS
# ==============================================================================
class ExperimentResultsSubApp(gui.SMTirfPanel):

    def setup_toolbar(self):
        gui.add_toolbar_button(self.toolbar, "histogram", "State Populations", 
                               lambda: self.change_view("splithist"))
        gui.add_toolbar_button(self.toolbar, "tdp", "TDP", 
                               lambda: self.change_view("tdp"))
        gui.add_toolbar_button(self.toolbar, "kinetics", "Kinetics", 
                               lambda: self.change_view("kinetics"))
        self.toolbar.addSeparator()
        gui.format_toolbar(self.toolbar)
        self.parent().addToolBar(self.toolbar)

    def layout(self):
        mainBox = QtWidgets.QVBoxLayout()

        grpResults = QtWidgets.QGroupBox("Results")
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(gui.widgets.ExportHistogramButton(self.controller))
        # hbox.addWidget(gui.widgets.SaveHistogramImageButton(self.controller))
        hbox.addWidget(gui.widgets.ExportTdpButton(self.controller))
        # hbox.addWidget(gui.widgets.SaveTdpImageButton(self.controller))
        hbox.addItem(QtWidgets.QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed))
        hbox.addWidget(gui.widgets.UpdateResultsButton(self.controller))
        grpResults.setLayout(hbox)
        
        mainBox.addWidget(grpResults)
        mainBox.addWidget(gui.plots.ResultViewerPlot(self.controller), stretch=1)

        self.setLayout(mainBox)

    def change_view(self, view):
        self.controller.currentResultViewChanged.emit(view)



# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = SMTirfViewerApp()
    win.show()
    sys.exit(app.exec_())
