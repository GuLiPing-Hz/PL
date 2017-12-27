
import json

def TestJson():
	data1 = {'b':789,'c':456,'a':123} 
	d1 = json.dumps(data1,indent=0,sort_keys=False)
	print(d1,type(d1))
	print(data1)

	try:
		with open("dataJson","r") as file:
			content = json.load(file)
			print(content,type(content))
	except FileNotFoundError:
		pass

	with open("dataJson","w") as file:
		json.dump(data1,file)

if __name__ == '__main__':
	TestJson()

