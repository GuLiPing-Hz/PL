
import json

def TestJson():
	data1 = {'b':789,'c':456,'a':123} 
	d1 = json.dumps(data1,sort_keys=False,indent=0)
	print(d1,type(d1))

	try:
		with open("dataJson","r") as file:
			content = json.load(file)
			print(content,type(content))
	except FileNotFoundError:
		pass

	with open("dataJson","w") as file:
		json.dump(data1,file)

def ChangePosition(src_name,out_name):
	try:
		with open(src_name,"r") as file:
			routes = json.load(file)
			#print(routes,type(routes))

			route = routes[0]
			# print(route,type(route))
			# print(route["points"])
			for route in routes:
				for point in route["points"]:
					point["x"] -= 320
					point["y"] -= 180

			# print(routes[0],type(routes[0]))

			with open(out_name,"w") as file2:
				json.dump(routes,file2)

	except FileNotFoundError:
		print("not find file=",src_name)
		pass

if __name__ == '__main__':
	#TestJson()

	ChangePosition("../test/pfishRoutes.json","../test/pfishRoutes_new.json")

