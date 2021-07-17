import matplotlib.pyplot as plt
import random
import time
import requests
import time


def get_bondage():
    request = requests.get("https://api.cryptonator.com/api/ticker/btc-rub", headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
    
    print(type(request.json()["ticker"]["price"]), float(request.json()["ticker"]["price"]))
    return float(request.json()["ticker"]["price"])


x = [0]
T = [72]
Ch = [90]
B = [get_bondage()]

def generate_info(Tugric=T, Chervonec=Ch, Bondage=B):
    for i in range(1, 100):
        x.append(i)
        rand1 = random.randint(-500, 500) / 100
        rand2 = random.randint(-500, 500) / 100
        rand3 = random.randint(-500, 500) / 100
        
        if Tugric[i - 1] - rand1 >= 0:
            Tugric.append(Tugric[i - 1] + rand1)
        else:
            Tugric.append(Tugric[i - 1] + abs(rand1))
            
        if Tugric[i - 1] - rand2 >= 0:
            Chervonec.append(Chervonec[i - 1] + rand2)
        else:
            Chervonec.append(Chervonec[i - 1] + abs(rand2))
            
        if Bondage[i - 1] - rand3 >= 0:
            Bondage.append(Bondage[i - 1] + rand3)
        else:
            Bondage.append(Bondage[i - 1] + abs(rand3))
    print(x)
    return [Tugric, Chervonec, Bondage]


def update_info(Tugric, Chervonec, Bondage):
    del Tugric[0]
    del Chervonec[0]
    del Bondage[0]
    Tugric.append(Tugric[-1] + random.randint(-500, 500) / 100)
    Chervonec.append(Chervonec[-1] + random.randint(-500, 500) / 100)
    Bondage.append(get_bondage())
    


def make_b_graf(filename, data):
    x = [0]
    for i in range(1, 100):
        x.append(i)
    
    ax = plt.axes(in_layout=False)
    fig = plt.subplots()
    fig[0].subplots_adjust(left=0, right=0.93, bottom=0, top=0.95, wspace=1, hspace=1)
    
    plt.tick_params(right=True, labelright=True, left=False, labelleft=False, bottom=False, labelbottom=False, length=6, width=2)
    plt.plot(x, data, color="#B22222", label="Bondage (BTC)", linewidth=2)

    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.close()

def make_currency_graf(filename, data1=None, data2=None, name1="Червонцы", name2="Тугрики"):
    x = [0]
    for i in range(1, 100):
        x.append(i)
    
    ax = plt.axes(in_layout=False)
    fig = plt.subplots()
    fig[0].subplots_adjust(left=0, right=0.93, bottom=0, top=0.95, wspace=0, hspace=0)
    
    plt.tick_params(right=True, labelright=True, left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.plot(x, data1, color="#68f768", label=name1, linewidth=2)
    if data2 is not None:
        plt.plot(x, data2, color="#4c94e0", label=name2, linewidth=2)

    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.close()
