import pywinauto
import time

class WindowCloserProcess(object):

	def __init__(self, *, title, retries=3, sleep_interval=1):

		self.title = title
		self.retries = retries
		self.sleep_interval = sleep_interval

		self.run()

	def run(self):
		for retry in range(self.retries):
			try:
				self.app = pywinauto.application.Application().connect(title=self.title)
				self.app.kill()
				break
			except pywinauto.findwindows.ElementNotFoundError as e:
				print(f'pywinauto.findwindows.ElementNotFoundError: {e}')
				time.sleep(self.sleep_interval)
				continue

title = input('Title: ')
WindowCloserProcess(title=title)