import sys
import random

filesize = int(input('File size in bits: '))
filepath = input('File path: ')

def create_random_data(filesize:int, filepath:str):
	print(f'Writing {filesize} bits of random data to {filepath}.')
	with open(filepath, 'w+') as file:
		for bit in range(filesize):
			file.write(str(random.randint(0, 1)))
			if bit is not 0:
				print(f'\r{round(bit/filesize*100, 1)}%', end='', flush=True)
				if bit == filesize-1:
					print('\nDone.')

create_random_data(filesize, filepath)
input()