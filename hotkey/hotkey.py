import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
import keyboard

import ui

class Ui_MainWindow(ui.Ui_MainWindow):

	def __init__(self):
		self.threadpool = QtCore.QThreadPool()

	def setupUi(self, MainWindow:object):
		super(Ui_MainWindow, self).setupUi(MainWindow)

		self.main()

	def main(self):
		self.sequence = KeySequence()

		self.initialize_dropdown()

		self.checkbox_handler()
		self.dropdown_handler()
		self.button_handler()

		self.enable_ui(True)
		self.enable_sequence(False)

		self.sb_print('OK')

	def initialize_dropdown(self):
		self.dropdown_letters.addItems(map(chr, range(65, 91)))

	def initialize_dialog(self):
		self.dialog = QtWidgets.QDialog()
		self.dialog_ui = Ui_Dialog(self.dialog)

	def close_dialog(self):
		self.dialog.close()
		self.dialog = None

	def sb_print(self, message:str):
		self.status_bar.showMessage(message)

	def run_script(self):
		self.process = HotkeyProcess()
		
		self.enable_ui(False)
		self.sb_print('Running')

		self.process.signals.keypress.connect(self.on_keypress_signal)
		self.process.signals.terminate.connect(self.on_terminate_signal)

		self.threadpool.start(self.process)

	def enable_ui(self, enable:bool):
		self.checkbox_ctrl.setEnabled(enable)
		self.checkbox_alt.setEnabled(enable)
		self.checkbox_shift.setEnabled(enable)
		self.dropdown_letters.setEnabled(enable)
		self.button_viewcode.setEnabled(enable)
		self.button_set.setEnabled(enable)
		self.button_start.setEnabled(enable)
		self.button_stop.setEnabled(not enable)

	def enable_sequence(self, enable:bool):
		self.checkbox_ctrl.setEnabled(not enable)
		self.checkbox_alt.setEnabled(not enable)
		self.checkbox_shift.setEnabled(not enable)
		self.dropdown_letters.setEnabled(not enable)
		self.button_start.setEnabled(enable)
		self.sequence.is_set = enable
		if enable:
			self.button_set.setText(QtCore.QCoreApplication.translate('MainWindow', 'Delete'))
		else:
			self.button_set.setText(QtCore.QCoreApplication.translate('MainWindow', 'Set'))

	def on_keypress_signal(self):
		self.sb_print('Keypress detected')
		exec(self.sequence.code)

	def on_terminate_signal(self):
		self.process = None
		self.enable_ui(True)
		keyboard.unhook_all_hotkeys()
		self.sb_print('Terminated')

	def checkbox_handler(self):

		def edit_sequence():
			self.sequence.ctrl = self.checkbox_ctrl.isChecked()
			self.sequence.shift = self.checkbox_shift.isChecked()
			self.sequence.alt = self.checkbox_alt.isChecked()
			self.sequence.is_set = False

		self.checkbox_ctrl.toggled.connect(edit_sequence)
		self.checkbox_shift.toggled.connect(edit_sequence)
		self.checkbox_alt.toggled.connect(edit_sequence)

	def dropdown_handler(self):

		def edit_sequence():
			self.sequence.letter = self.dropdown_letters.currentText()
			self.sequence.is_set = False

		self.dropdown_letters.activated.connect(edit_sequence)

	def button_handler(self):

		def edit_sequence():
			if self.sequence.is_set:
				self.enable_sequence(False)
			else:
				if self.sequence.has_modifier():
					self.enable_sequence(True)
					self.sb_print('Hotkey set')
				else:
					self.sb_print('Please set a modifier key')

		def show_dialog():
			self.initialize_dialog()
			self.dialog.show()

		def start_script():
			if self.sequence.has_modifier():
				title = 'Information'
				message = f'You are about to run your script with the hotkey {self.sequence.keys}.\nOnce you press OK, this window will close.\nYou can terminate the script at any time with Ctrl+Alt+Shift+Q.'
				key = QtWidgets.QMessageBox.information(MainWindow, title, message)
				if key == 1024:
					self.run_script()
			else:
				self.sb_print('Please set a hotkey first')

		def stop_script():
			self.on_terminate_signal()

		self.button_set.clicked.connect(edit_sequence)
		self.button_viewcode.clicked.connect(show_dialog)
		self.button_start.clicked.connect(start_script)
		self.button_stop.clicked.connect(stop_script)


class Ui_Dialog(ui.Ui_Dialog):

	def __init__(self, Dialog):
		super(Ui_Dialog, self).setupUi(Dialog)

		self.main()

	def main(self):
		self.initialize_window()

		self.button_handler()

	def initialize_window(self):
		if mainwindow.sequence.has_code():
			self.field_code.setPlainText(str(mainwindow.sequence.code))
		else:
			self.field_code.setPlainText('')

	def button_handler(self):
		
		def save_changes():
			mainwindow.sequence.code = self.field_code.toPlainText()
			mainwindow.sb_print('Changes saved')
			mainwindow.close_dialog()

		def discard_changes():
			mainwindow.sb_print('Changes discarded')
			mainwindow.close_dialog()

		def execute_code():
			try:
				exec(self.field_code.toPlainText())
				self.field_terminal.clear()
			except Exception as e:
				self.field_terminal.setPlainText(repr(e))

		self.button_ok.clicked.connect(save_changes)
		self.button_cancel.clicked.connect(discard_changes)
		self.button_start.clicked.connect(execute_code)

class KeySequence(object):

	def __init__(self):
		self.ctrl = False
		self.alt = False
		self.shift = False
		self.letter = 'A'
		self.code = None

		self.is_set = False

	def has_modifier(self)->bool:
		if self.ctrl or self.alt or self.shift:
			return True
		else:
			return False

	def has_code(self)->bool:
		if self.code:
			return True
		else:
			return False

	@property
	def keys(self)->str:
		keys = []

		if self.ctrl:
			keys.append('Ctrl')
		if self.alt:
			keys.append('Alt')
		if self.shift:
			keys.append('Shift')
		keys.append(self.letter)
		return '+'.join(keys)

class HotkeyProcess(QtCore.QRunnable):

	def __init__(self):
		super(HotkeyProcess, self).__init__()

		self.signals = HotkeySignals()

	@QtCore.pyqtSlot()
	def run(self):
		keyboard.add_hotkey(mainwindow.sequence.keys.lower(), self.signal_press)
		keyboard.add_hotkey('ctrl+alt+shift+q', self.signal_terminate)

	def signal_press(self):
		self.signals.keypress.emit(True)

	def signal_terminate(self):
		self.signals.terminate.emit(False)

class HotkeySignals(QtCore.QObject):
	keypress = QtCore.pyqtSignal(bool)
	terminate = QtCore.pyqtSignal(bool)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	mainwindow = Ui_MainWindow()
	mainwindow.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())