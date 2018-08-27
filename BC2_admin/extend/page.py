from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def test (USer_data, page=1):
	paginator = Paginator(USer_data, 10)
	
	"""
	获取 用户数据 然后使用 Paginator分页器 每页10条数据

	paginator.page(page) 获取总共的数据

	page_number = list(range(max(number - 2, 5), number)) + list(range(number, min(number + 2, paginator.num_pages) +
	1))
	 获取获取页码的 前两页和后两页  使用max 和 min 在用list 变成列表 在列表拼接 传过前台

	"""
	
	contacts = paginator.page(page)
	
	number = contacts.number
	page_number = list(range(max(number - 2, 5), number)) + list(
		range(number, min(number + 2, paginator.num_pages) + 1))
	contacts1 = { }
	contacts1 ['page_number'] = page_number
	contacts1 ['contacts'] = contacts
	return contacts1