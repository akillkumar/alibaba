from datetime import datetime, time

encoding = 'utf-8'

class COLORS:
	clear = '\033[0m'
	blue  = '\033[94m'
	green = '\033[92m'
	cyan  = '\033[96m'
	red   = '\033[91m'
	yell  = '\033[93m'
	mag   = '\033[35m'


quiz_start = time (14, 50, 0)
quiz_end   = time (16, 20, 0)

server_addr = ('127.0.0.1', 9000)