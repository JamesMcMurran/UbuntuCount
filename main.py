import operator
import gzip

from ftplib import FTP

hostname = "ftp.us.debian.org"
path = "/debian/dists/stable/main/"

architecture = input("Architecture type (amd64, arm64, mips etc.): ")
filename = "Contents-" + str(architecture)+".gz"


# connect to the FTP server
ftp = FTP(hostname)
ftp.login()
ftp.cwd(path)
print("Dowloading "+filename)
ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
ftp.quit()


print("Extracting contents of "+filename)

packagescount = {}
f = gzip.open(filename, 'rb')

for line in f.readlines():
    # clean up the line and count them
    package = str(line).split(' ')[-1].replace("/", "_").replace("\\n", "")
    packagescount[package] = packagescount.get(package, 0) + 1
f.close()

# Order packages desc
sorted_packages = sorted(packagescount.items(),
                         key=operator.itemgetter(1), reverse=True)

i = 1
# 1. <package name 1> <number of files>
for key in sorted_packages:
    print("{:<1d}. {:<30s} {:>20d}".format(i, key[0], key[1]))
    i += 1
    if(i > 10):
        break
