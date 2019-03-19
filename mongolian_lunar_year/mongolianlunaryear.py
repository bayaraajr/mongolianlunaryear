import math
from datetime import *
from dateutil.relativedelta import relativedelta
MZERO = 3
EPOCH = 1747
YMIN = 1
IXX = 46
BETASTAR = 10
BETA = 172
CNST = {
    "m0":2359237+2603/2828,
	"m1":167025/5656,
	"m2":11135/11312,
	"s0":397/402,
	"s1":65/804,
	"s2":13/4824,
	"a0":1523/1764,
	"a1":253/3528,
	"a2":1/28 //+1/105840
}
CAL_TYPE = 2
def get(year=datetime.today() , to = datetime.today()):
    '''
    Parameters
    ----------
    year : datetime
        Starting date
    to   : datetime
        Ending date     
    '''
    start= year.year
    end = to.year
    lunar_years_first_days = []

    for y in range(start , end):
        print(y)
        julian = new_year_jd(y)
        g = jd2g(julian)
        tmp = datetime(g["year"] , g["month"] , g["day"] , 0 ,0)
        lunar_years_first_days.append(tmp)

    return lunar_years_first_days

def new_year_jd(year):
    if CAL_TYPE <= 2:
        return julian_day(year - 1  , 12 , 0 , 30) + 1
    else:
        dat = {}
        prev_month(year , 1 , 0 , dat)
        return julian_day(dat["y"] , dat["m"] , dat["l"] , 30 ) + 1

def julian_day(y , m ,  l , d):
    n = true_month(y , m, l)
    t = true_date(d , n)
    return math.floor(t)

def jd2g(jd):
    date = {}
    gg = math.floor(math.floor((jd-4479.5)/36524.25)*0.75+0.5) - 37
    n = gg + jd
    date["year"] = math.floor(n/365.25) - 4712
    dd = math.floor((n-59.25)%365.25)
    date["month"] = (math.floor((dd+0.5)/30.6)+2)%12+1
    date["day"]= math.floor((dd+0.5)%30.6)+1
    return date



def true_month(y , m , l):
    p =  67*mstar(y , m)  + BETASTAR
    ix = (67*mstar(y , m)  + BETASTAR) % 65
    if ix < 0:
        ix+=65
    pp = (p-ix) /65
    
    if l or ix < IXX:
        return pp
    return pp + 1

def true_date(d , n):
    mean_date = n * CNST["m1"] + d*CNST["m2"] + CNST["m0"]
    mean_sun = n * CNST["s1"] + d*CNST["s2"] + CNST["s0"]
    anomaly_moon = n * CNST["a1"] + d*CNST["a2"] + CNST["a0"] 
    moon_equ = moon_tab(28*anomaly_moon)
    anomaly_sun = mean_sun - .25
    sun_equ = sun_tab(12*anomaly_sun)
    t = mean_date + moon_equ/60 - sun_equ/60
    return t
def mstar(y , m):
    return 12 * (y - EPOCH) + m - MZERO

def moon_tab(i):
    i = i % 28
    if i < 0 :
        i+=28
    s = 1
    if i>=14:
        i-=14
        s=-1
    if i > 7:
        i = 14 - i
    a = math.floor(i)
    b = math.ceil(i)

    v = [0 , 5 , 10 , 15 ,19 , 22 ,24 ,25]

    print("%s" % a)
    if a == b:
        return s*v[a]
    return s*((b-i)*v[a] + (i-a)*v[b])/(b-a)

def sun_tab(i):
    i = i % 12
    if i < 0:
        i += 12
    s = 1
    if i>=6:
        i-=6
        s = -1
    if i > 3:
        i = 6 - i
    a = math.floor(i)
    b = math.ceil(i)

    v = [0 , 6 , 10 , 11]
    if a==b:
        return s*v[a]
    return s*((b-i)*v[a]+(i-a)*v[b])/(b-a)

def prev_month(y , m , l , dat):
    dat["y"] = y
    dat["m"] = m
    dat["l"] = l
    if leap_month(y , m):
        if l:
            dat["l"] = 0
            dat["m"]-=1
        else:
            dat["l"] = 1
    else:
        dat["m"]-=1
    
    if dat["m"]<=0:
        dat["m"] = 12
        dat["y"]-=1

    #TODO: check if it is necessary to return 'dat'
    return dat

def next_month():
    pass

def leap_month(y , m):
    t = (24*(y-EPOCH)+2*m-BETA)%65
    if t < 0:
        t+=65
    return t==0 or t==1

def leap_year(y):
    t=(24*(y-EPOCH)-BETA)%65

    if t < 0:
        t+=65
    return 1 + math.floor((64-t)/2)