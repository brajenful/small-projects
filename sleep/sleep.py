import asyncio

lstin = []
lstout = []

async def sort(num):
	await asyncio.sleep(num)
	lstout.append(num)
	print(lstout)

lstin = [int(x) for x in input('lstin: ').split()]
loop = asyncio.get_event_loop()
group = [sort(num) for num in lstin]
loop.run_until_complete(asyncio.gather(*group))
print('Done.')
<<<<<<< HEAD
input()
=======
input()
>>>>>>> eea846ab1133d04ea5d36feb27f91f6e8fb78df7
