from PyQt5 import QtCore, QtGui, QtWidgets
import traceback

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(388, 61)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.checkbox_ctrl = QtWidgets.QCheckBox(self.centralwidget)
		self.checkbox_ctrl.setObjectName("checkbox_ctrl")
		self.horizontalLayout.addWidget(self.checkbox_ctrl)
		self.checkbox_shift = QtWidgets.QCheckBox(self.centralwidget)
		self.checkbox_shift.setObjectName("checkbox_shift")
		self.horizontalLayout.addWidget(self.checkbox_shift)
		self.checkbox_alt = QtWidgets.QCheckBox(self.centralwidget)
		self.checkbox_alt.setObjectName("checkbox_alt")
		self.horizontalLayout.addWidget(self.checkbox_alt)
		self.dropdown_letters = QtWidgets.QComboBox(self.centralwidget)
		self.dropdown_letters.setObjectName("dropdown_letters")
		self.horizontalLayout.addWidget(self.dropdown_letters)
		self.button_viewcode = QtWidgets.QPushButton(self.centralwidget)
		self.button_viewcode.setObjectName("button_viewcode")
		self.horizontalLayout.addWidget(self.button_viewcode)
		self.button_set = QtWidgets.QPushButton(self.centralwidget)
		self.button_set.setObjectName("button_set")
		self.horizontalLayout.addWidget(self.button_set)
		MainWindow.setCentralWidget(self.centralwidget)
		self.status_bar = QtWidgets.QStatusBar(MainWindow)
		self.status_bar.setObjectName("status_bar")
		MainWindow.setStatusBar(self.status_bar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.main()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Hotkey"))
		self.checkbox_ctrl.setText(_translate("MainWindow", "Ctrl"))
		self.checkbox_shift.setText(_translate("MainWindow", "Shift"))
		self.checkbox_alt.setText(_translate("MainWindow", "Alt"))
		self.button_viewcode.setText(_translate("MainWindow", "View Code"))
		self.button_set.setText(_translate("MainWindow", "Set"))

	def main(self):
		self.sequence = KeySequence()

		self.initialize_dropdown()

		self.checkbox_handler()
		self.dropdown_handler()
		self.button_handler()

		self.sb_print('OK')

	def initialize_dropdown(self):
		self.dropdown_letters.addItems(map(chr, range(65, 91)))

	def initialize_dialog(self):
		self.dialog = QtWidgets.QDialog()
		self.dialog_ui = Ui_Dialog()
		self.dialog_ui.setupUi(self.dialog)

	def close_dialog(self):
		self.dialog.close()
		self.dialog = None

	def sb_print(self, message):
		self.status_bar.showMessage(str(message))

	def checkbox_handler(self):

		def edit_sequence():
			self.sequence.ctrl = self.checkbox_ctrl.isChecked()
			self.sequence.shift = self.checkbox_shift.isChecked()
			self.sequence.alt = self.checkbox_alt.isChecked()
			self.sequence.is_set = False

			#self.sb_print(f'{self.sequence.ctrl} {self.sequence.shift} {self.sequence.alt}')

		self.checkbox_ctrl.toggled.connect(edit_sequence)
		self.checkbox_shift.toggled.connect(edit_sequence)
		self.checkbox_alt.toggled.connect(edit_sequence)

	def dropdown_handler(self):

		def edit_sequence():
			self.sequence.letter = self.dropdown_letters.currentText()
			self.sequence.is_set = False

			#self.sb_print(f'{self.sequence.letter}')

		self.dropdown_letters.activated.connect(edit_sequence)

	def button_handler(self):

		def edit_sequence():
			self.sequence.is_set = True
			self.sb_print('Hotkey set')

		def show_dialog():
			self.initialize_dialog()
			self.dialog.show()

		self.button_set.clicked.connect(edit_sequence)
		self.button_viewcode.clicked.connect(show_dialog)

class KeySequence(object):

	def __init__(self):
		self.ctrl = False
		self.alt = False
		self.shift = False
		self.letter = None
		self.code = None

		self.is_set = False

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(400, 300)
		self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
		self.verticalLayout.setObjectName("verticalLayout")
		self.field_code = QtWidgets.QPlainTextEdit(Dialog)
		self.field_code.setObjectName("field_code")
		self.verticalLayout.addWidget(self.field_code)
		self.field_terminal = QtWidgets.QPlainTextEdit(Dialog)
		self.field_terminal.setObjectName("field_terminal")
		self.verticalLayout.addWidget(self.field_terminal)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.button_run = QtWidgets.QPushButton(Dialog)
		self.button_run.setObjectName("button_run")
		self.horizontalLayout_2.addWidget(self.button_run)
		self.button_ok = QtWidgets.QPushButton(Dialog)
		self.button_ok.setObjectName("button_ok")
		self.horizontalLayout_2.addWidget(self.button_ok)
		self.button_cancel = QtWidgets.QPushButton(Dialog)
		self.button_cancel.setObjectName("button_cancel")
		self.horizontalLayout_2.addWidget(self.button_cancel)
		self.verticalLayout.addLayout(self.horizontalLayout_2)

		self.field_terminal.setReadOnly(True)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		self.main()

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Terminal"))
		self.button_run.setText(_translate("Dialog", "Run"))
		self.button_ok.setText(_translate("Dialog", "OK"))
		self.button_cancel.setText(_translate("Dialog", "Cancel"))

	def main(self):
		self.initialize_window()

		self.button_handler()

	def initialize_window(self):
		if ui.sequence.code is None:
			self.field_code.setPlainText('')
		else:
			self.field_code.setPlainText(str(ui.sequence.code))

	def button_handler(self):
		
		def save_changes():
			ui.sequence.code = self.field_code.toPlainText()
			ui.sb_print('Changes saved')
			ui.close_dialog()

		def discard_changes():
			ui.sb_print('Changes discarded')
			ui.close_dialog()

		def execute_code():
			try:
				exec(self.field_code.toPlainText())
				self.field_terminal.clear()
			except Exception as e:
				self.field_terminal.setPlainText(repr(e))

		self.button_ok.clicked.connect(save_changes)
		self.button_cancel.clicked.connect(discard_changes)
		self.button_run.clicked.connect(execute_code)



if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

