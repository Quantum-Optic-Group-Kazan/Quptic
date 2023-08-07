# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QupticakLTMD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.10
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore

from QLed import QLed as KLed


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 791, 591))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_4.addWidget(self.tabWidget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_2.addWidget(self.radioButton_2)

        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_9 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.verticalLayout_2.addWidget(self.radioButton_9)

        self.radioButton_10 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_10.setObjectName(u"radioButton_10")

        self.verticalLayout_2.addWidget(self.radioButton_10)

        self.radioButton_8 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.verticalLayout_2.addWidget(self.radioButton_8)

        self.radioButton_7 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.verticalLayout_2.addWidget(self.radioButton_7)

        self.radioButton_6 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.verticalLayout_2.addWidget(self.radioButton_6)

        self.radioButton_5 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.verticalLayout_2.addWidget(self.radioButton_5)

        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_2.addWidget(self.radioButton_3)

        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_2.addWidget(self.radioButton)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)
        self.kled = KLed(self.verticalLayoutWidget)
        self.kled.setObjectName(u"kled")
        self.kled.setOnColour(self.kled.Green)
        self.kled.setOffColour(self.kled.Red)

        self.horizontalLayout_5.addWidget(self.kled)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Quptic", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_10.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_8.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

