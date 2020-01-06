import os, sys, re, shutil

if not os.geteuid() == 0:
    sys.exit("\nНеобходимы root права!\n")

sites = os.listdir("/etc/apache2/sites-available")
sites.remove("000-default.conf")
sites.remove("default-ssl.conf")

sites.sort()

print("Созданные сайты: \n")
for i, s in enumerate(sites):
	print(str(i+1) + ") " + s[:-5])

res = input("\nСоздать: 1; Удалить: 2 -")
if res == "1":
	name = input("Имя (site.com): ")

	if name+".conf" in sites:
		sys.exit("\nСайт уже существует!\n")

	os.mkdir("/var/www/" + name)

	f = open("/var/www/" + name + "/index.html", "w")
	f.write("<html style=\"background: black\"><center><h1 style=\"color: lime\">Success<br>"+name+" are Created!</h1></center></html>")
	f.close()

	f = open("/etc/apache2/sites-available/" + name + ".conf", "w")
	f.write(
'''
<VirtualHost *:80>
	ServerName ''' + name + '''
	ServerAlias www.''' + name + '''
	ServerAdmin admin@''' + name + '''
	DocumentRoot /var/www/''' + name + '''
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
''')
	f.close()

	os.system("chmod -R 777 /var/www/"+name)
	os.system("a2ensite "+name)
	os.system("systemctl reload apache2")

	f = open("/etc/hosts", "a")
	f.write("\n127.0.0.1	"+name)
	f.close()

	print("\nSuccess!")
elif res == "2":
	n = int(input("Номер сайта: "))
	if n > i and n < i:
		sys.exit("\nНеверный номер!\n")
	host = sites[n-1]
	
	shutil.rmtree("/var/www/" + host[:-5])
	os.remove("/etc/apache2/sites-available/" + host)

	os.system("a2dissite "+host[:-5])
	os.system("systemctl reload apache2")

	with open('/etc/hosts') as f:
		lines = f.readlines()
	str = '127.0.0.1	' + host[:-5]
	pattern = re.compile(re.escape(str))
	with open('/etc/hosts', 'w') as f:
		for line in lines:
			result = pattern.search(line)
			if result is None:
				f.write(line)
	print("\nSucess!")