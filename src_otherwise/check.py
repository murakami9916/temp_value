import pandas as pd

def check(fname, target):
	data = pd.read_csv(fname, encoding = "utf8")
	#numNULL = data.isnull().sum()
	#print(numNULL)
	ch = data[data["url"] == target[2]]

	if(ch.shape[0] == 0):
		print('NOT FOUND [{0}]'.format(target))
		new = pd.Series(target, index = data.columns, name = data.shape[0])
		data = data.append(new)
		print("")
		print(data.tail())
		data.to_csv('data.csv', encoding='utf-8', index = False)
		return 1, new

	else:
		print('FOUND')
		print(ch)
		empty = pd.Series(['None','None','None'], index = data.columns, name = data.shape[0])
		return 0, empty

if __name__ == '__main__':
	name = "data.csv"
	title = "hello"
	image = "hello"
	url = "http://sukai9682.jp/fn_image/ff_2940496_full.jpg"
	#url = "http://sukai9682.jp/fn_image/ff_2795221_full.jpg"
	checkData = [title, image, url]
	isChecked, info = check(name, checkData)
	print("isChecked = {0}".format(isChecked))
	print(info)
