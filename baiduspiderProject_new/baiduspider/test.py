import json
import datetime
#https://www.wszgw.net/forum.php?mod=viewthread&tid=90426&extra=page%3D1%26filter%3Dtypeid%26typeid%3D11
str = "https://www.wszgw.net/forum.php?mod=viewthread&tid=90426&extra=page%3D1%26filter%3Dtypeid%26typeid%3D11"
id = str.split('&')[1]
num = id.split('=')[1]
print(num)
time = datetime.datetime(2017,12,20)
deltatime = (datetime.datetime.now() - time).days



print(deltatime)