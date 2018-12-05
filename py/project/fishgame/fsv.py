import pandas #pip install pandas

def orderLog(fsv):
	print(fsv)
	csv = fsv.replace(".tsv",".csv")
	dir = fsv[:fsv.rfind("/")]

	all = []
	with open(fsv, "r+") as f:
		for line in f:
		    print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
		    words = line.split("	")
		    words[1] = "id-"+str(words[1])
		    words[2] = "id-"+str(words[2])
		    all.append(words)
		    # print(words)
		    # print(all)
		    # break
	df = pandas.DataFrame(all)
	df.to_csv(csv)

def almsLog(fsv):
	print(fsv)
	csv = fsv.replace(".tsv",".csv")
	dir = fsv[:fsv.rfind("/")]

	all = {}
	with open(fsv, "r+") as f:
		for line in f:
			# print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
			words = line.split("	")
			# words[1] = "id-"+str(words[1])
			# words[2] = "id-"+str(words[2])
			# all[words[2]] = {}

			dayName = words[2][:-1]
			print(dayName)
			day = {}
			uids = words[1].split(",")
			for i in range(len(uids)):
				uid = uids[i]
				if uid not in day:
					day[uid] = 1
				else:
					day[uid] = day[uid] + 1
			all[dayName] = day
			# print(words)
			# all.append(words)
			# print(words)
			# print(all)
			# break

	# df = pandas.DataFrame(all)
	# df.to_csv(csv)

	for k,v in all.items():
		for k1,v1 in v.items():
			# if(v1>3):
			print(k,k1,v1)




#把tsv转成csv，然后把里面的很大的数字数据转成 id-，文本的形式
if __name__ == '__main__':
	# orderLog("D:/glp/Github/fishing_server/sql/select___from_order_log_where__channel_2.tsv")
	almsLog("D:/glp/Github/fishing_server/sql/SELECT____COUNT________GROUP_CONCAT_uid_.tsv")

