#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  24 18:26:28 2021
@author: Laurenz Kruty
"""

import sys
from PyQt5 import QtWidgets, uic
import search
import multiprocessing
from PyQt5.QtWidgets import *


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("main_GUI.ui")


def show_about_dialog():
    text = "<center>" \
        "<h1>About: List Searcher</h1>" \
        "</center>" \
        "<p>Version v0.1.0<br/>" \
        "Copyright &copy; 2021 Laurenz Kruty.</p>"
    QMessageBox.about(window, "About List Searcher", text)


def show_help_dialog():
    text = "<h1>Help: List Searcher</h1>"\
        "<center>"\
        "<p>Further information:</p>"\
        "List can be in .txt or .csv format. For .txt each entry has to be in a new line. "\
        "See default_list.* for an example."
    QMessageBox.about(window, "Help", text)


def open_file_name_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(window, "QFileDialog.getOpenFileName()", "",
                                               "Text files (*.txt);;Comma separated values (*.csv);;All Files (*)",
                                               options=options)
    if file_name:
        print(file_name)
        window.label_ListPath.setText(file_name)
    return file_name


def search_now():
    search_string = window.SearchString.text()
    file_name = window.label_ListPath.text()
    if file_name == "List path:":  # If no List is selected and the initial label is present
        print("No list selected.")
        window.label_error.setText("Please select a list first.")
        return 1
    if search_string == '':
        print("No search string is entered.")
        window.label_error.setText("Please enter a search string first.")
        window.StartSearch.setDisabled(True)
        return 1
    n_cpus = multiprocessing.cpu_count()
    try:
        results = search.run(file_name, search_string, n_cpus)
        print(results)
    except Exception as ex:
        print(ex)
        window.label_error.setText("Error occurred. See Help for further information")
        return 1

    results = str(results)
    window.textBrowser.setText(results)
    return 0


def enable_search_button():
    window.StartSearch.setDisabled(False)


window.StartSearch.setDisabled(True)
window.SearchString.textChanged.connect(enable_search_button)
window.StartSearch.clicked.connect(search_now)
window.LoadList.clicked.connect(open_file_name_dialog)
# Actions
window.actionAbout.triggered.connect(show_about_dialog)
window.actionHelp.triggered.connect(show_help_dialog)
window.exit_button.clicked.connect(app.exit)
window.show()


if __name__ == '__main__':
    sys.exit(app.exec_())
