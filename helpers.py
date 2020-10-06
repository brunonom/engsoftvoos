import pandas
def empt(date):
	if len(date) >= 10:
		return False
	return True
def minutesDiff(date1, date2):
	if type(date1) is not str or type(date2) is not str or empt(date1) or empt(date2):
		return 0
	#date1 = pandas.to_datetime(date1)
	#date2 = pandas.to_datetime(date2)
	#delay = date1 - date2
	#seconds = delay.total_seconds()
	#if seconds < 0:
	#		return 0
	#return seconds / 60
	a = date1[11:16]
	b = date2[11:16]
	n = [int(a[0:2]), int(a[3:5])]
	m = [int(b[0:2]), int(b[3:5])]
	res = 0
	if n[0] != m[0]:
		if n[0] < m[0]:
			res += (m[0] - n[0]) * 60;
		else:
			res += (24 - n[0] + m[0]) * 60
	if n[1] < m[1]:
		res += m[1] - n[1]
	else:
		res -= n[1] - m[1]
	if res < 0:
		return 0
	return res
