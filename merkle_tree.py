import hashlib
class merkle_tree:
	def __init__ (self,transac):
		self.root = Make_tree(transac)
def Make_tree(transactions):
	convert = []
	for transac in transactions:
		convert.append(str(transac))
	root = merge(convert)
	return root

def merge(transactions):
	if len(transactions) == 1:
		return transactions[0]
	to_return = []
	index = 0
	while index < len(transactions):
		left = transactions[index]
		index += 1
		right = ""
		if index < len(transactions):
			right = transactions[index]
		index += 1
		to_return.append(hashlib.sha256((left+right).encode()).hexdigest())
	return merge(to_return)

if __name__ == '__main__':
	text = ['1',1454,'wevd','sdvgv','efeg']
	a = merkle_tree(text)
	print(a.root)