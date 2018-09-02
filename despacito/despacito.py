import psutil
import asyncio
import webbrowser

class Watcher(object):

	def __init__(self):
		self.process_name = input('Process name: ')
		self.check_interval = int(input('Check interval: '))
		self.refresh_process_list()

		self.despacito = 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'

	def begin(self):
		loop = asyncio.get_event_loop()
		future = asyncio.ensure_future(self.check_for_process())
		loop.run_until_complete(future)

	async def check_for_process(self):
		while True:
			for process in self.processes:
				print('Checking process')
				try:
					psutil.Process(process['pid'])
					print('Process found')
				except psutil._exceptions.NoSuchProcess:
					webbrowser.open(self.despacito)
					print('Despacito')
				self.refresh_process_list()
				await asyncio.sleep(self.check_interval)

	def refresh_process_list(self):
		self.processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if self.process_name in p.info['name']]

watcher = Watcher().begin()