import inputs
import keyboard
import asyncio
"""
def main():
	
	buttons = {'BTN_START': None, 'BTN_SELECT': 'play/pause', 'BTN_SOUTH': 'volume down', 'BTN_EAST': 'next track', 'BTN_NORTH': 'volume up', 'BTN_WEST': 'previous track'}
	flag = False

	while True:
		events = get_gamepad()
		for event in events:

			if event.code == 'BTN_START':
				flag = event.state
				continue
			if event.code in buttons.keys():
				if flag and event.state == 1:
					press_media_key(buttons[event.code])

def press_media_key(key):
	keyboard.send(key)
"""
class ControllerListener:

	def __init__(self):

		self.events = None
		self.event = None

		self.buttons = {'BTN_START': None,
						'BTN_SELECT': 'play/pause',
						'BTN_SOUTH': 'volume down',
						'BTN_NORTH': 'volume up',
						'BTN_WEST': 'previous track',
						'BTN_EAST': 'next track'}

		self.is_enabled = False

	async def __listen(self):
		self.events = self.gamepad
		for event in self.events:
			self.event = event

	async def __execute(self):
		await self.__enable_self()
		if await self.__check_prerequisites():
			await self.__press_media_key()

	async def __enable_self(self):
		if self.event.code == 'BTN_START':
			if self.event.state == 0:
				self.is_enabled = 0
				keyboard.send('alt+tab')
			if self.event.state == 1:
				self.is_enabled = 1
				keyboard.send('alt+tab')

	async def __check_prerequisites(self):
		if not self.is_enabled:
			return False
		if not self.event.state:
			return False
		if self.event.code not in self.buttons.keys():
			return False
		if self.event.code == 'BTN_START':
			return False
		else:
			return True

	async def __press_media_key(self):
		keyboard.send(self.buttons[self.event.code])

	@property
	def gamepad(self):
		return inputs.get_gamepad()
	
	async def __looper(self):
		while True:
			await self.__listen()
			await self.__execute()

	def run(self):
		loop = asyncio.get_event_loop()
		loop.create_task(self.__looper())
		loop.run_forever()

if __name__ == "__main__":
	listener = ControllerListener()
	listener.run()
