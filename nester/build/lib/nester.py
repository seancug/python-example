"""print list function, all of the deatil"""
def print_list(the_list):
	"""the_list is the list"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_list(each_item)
		else:
			print(each_item)
