def file(img,myfile):
	destination = open(img, 'wb+')
	for i in myfile.chunks( ):
		destination.write(i)
	destination.close( )