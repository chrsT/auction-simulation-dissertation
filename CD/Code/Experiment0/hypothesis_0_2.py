D = 0.7
M = 0.4
print("H	|	P")
H = 0.0
while H <= 1.05:
	P = 0.0
	P += H**2 * (1-M)
	P += (1-H)**2 * M
	P += 2*H * (1-H) * (D + M - 2 * D * M)
	print("{}	|	{}".format(round(H,2),round(P,3)))
	H += 0.05
