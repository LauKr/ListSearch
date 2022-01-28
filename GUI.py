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
        "Further information"
    QMessageBox.about(window, "Help", text)


def open_file_name_dialog():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getOpenFileName(window, "QFileDialog.getOpenFileName()", "",
                                               "Text files (*.txt);;All Files (*)", options=options)
    if file_name:
        print(file_name)
        window.label_ListPath.setText(file_name)
    return file_name


def search_now():
    search_string = window.SearchString.text()
    if search_string != '':
        # Fails without warning if wrong name is given
        n_cpus = multiprocessing.cpu_count()
        results = search.run('default_list.txt', search_string, n_cpus)
        print(results)
        results = str(results)
        window.textBrowser.setText(results)
    else:
        print('Please insert a search string first!')
        window.StartSearch.setDisabled(True)
        return 1
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
