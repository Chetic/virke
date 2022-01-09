#!/usr/bin/python3.7
import matplotlib.pyplot as plt
import matplotlib.dates as md
import sqlite3
import time

db = sqlite3.connect('virke.db')
cursor = db.cursor()
cursor.execute('select distinct SKU from Prices')
skus = cursor.fetchall()
objs = []
for sku_entries in skus:
    sku = sku_entries[0]
    cursor.execute('select * from Prices where SKU = "'+sku+'"')
    data = cursor.fetchall()
    name = data[0][3]
    times = []
    prices = []
    for entry in data:
        times.append(entry[2])
        prices.append(entry[4])
    plt.plot(times,prices,label = name)
#plt.legend()
plt.show()
