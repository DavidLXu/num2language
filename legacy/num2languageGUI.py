# arabic numbers to german numbers
# TODO 反向转换，可以用穷举(提取单位，近似寻找)，或者使用NLP的相关算法？
de_nums = ['null','ein','zwei','drei','vier','fünf','sechs','sieben','acht','neun']
#de_nums_X = ['null','ein','zwei','drei','vier','fünf','sechs','sieb','acht','neun']
de_nums_1X = ['zehn','elf','zwölf']
de_nums_X0 = ['null','zehn','zwanzig','dreißig','vierzig','fünfzig','sechzig','siebzig','achtzig','neunzig']
de_commas = ['null','tausend','million','milliarde','billion']
ch_nums = ['零','一','二','三','四','五','六','七','八','九','十']

def ln(x):
    n = 1000000.0 
    return n * ((x ** (1/n)) - 1)

def log(x,y): #logarithm of y on the base of x
    return ln(y)/ln(x)

def num2de_XXX(i): # zero not included
	text = ''
	
	if i//100!=0:
		text += de_nums[i//100]+'hundert'
		i%=100
	if 0<i<10:
		if i ==1:
			text += 'ein'
		else:
			text += de_nums[i]
	elif 10<=i<20:
		if 10<=i<13:
			text += de_nums_1X[i-10]
		elif i == 16:
			text += 'sechzehn'
		elif i == 17:
			text += 'siebzehn'
		else:
			text += de_nums[i-10]+'zehn'
	elif 20<=i<100:
		if i%10 == 0:
			text += de_nums_X0[i//10]
		else:
			text += de_nums[i%10]+'und'+de_nums_X0[i//10]
	return text
def num2de(i):
	text = ''
	if i == 0:
		text = 'null'
	elif i == 1:
		text = 'eins'
	else:
		comma = int(log(1000,i))
		if comma == 4:
			if i//1000**4 == 0:
				i %= 1000**4
				comma-=1
			else:
				text += num2de_XXX(i//1000**4)+de_commas[comma]
				i %= 1000**4
				comma-=1

		if comma == 3:
			if i//1000**3 == 0:
				i %= 1000**3
				comma-=1
			else:
				text += num2de_XXX(i//1000**3)+de_commas[comma]
				i %= 1000**3
				comma-=1

		if comma == 2:
			if i//1000**2 == 0:
				i %= 1000**2
				comma-=1
			else:
				text += num2de_XXX(i//1000**2)+de_commas[comma]
				i %= 1000**2
				comma-=1
		if comma == 1:
			if i//1000**1 == 0:
				i %= 1000**1
				comma-=1
			else:
				text += num2de_XXX(i//1000**1)+de_commas[comma]
				i %= 1000**1
				comma-=1
		if comma == 0:
			text += num2de_XXX(i)
	return text
def de2num(text):# 有待优化，从text中读取单位
	i = 0
	while(num2de(i)!=text):
		i+=1
	return i





ch_nums = ['零','一','二','三','四','五','六','七','八','九','十']
ch_nums_special = ['〇','一','两','三','四','五','六','七','八','九','十']
ch_units = ['个','十','百','千','万','十万','百万','千万','亿']
# 中国古代有万亿为兆，万兆为京的说法；也有亿亿为兆的说法；建国后，兆改为百万，不再有比亿大的单位，大数字就是亿的累加
"""
注：中国现代计数方法，四个一小组，八个一大组，大组以亿的幂次为计
亿^0
个		十		百		千
万		十万		百万		千万

亿^1
亿		十亿		百亿		千亿
万亿		十万亿	百万亿	千万亿

亿^2
亿亿		十亿亿	百亿亿	千亿亿
万亿亿	十万亿亿	百万亿亿	千万亿亿

给编程的启示：每完成八次十进，字符串末尾添加‘亿’

"""

def num2ch(i):
	if 0<=i<=10:
		text = ch_nums[i]
	elif 10<i<20:
		text = '十'+ch_nums[i%10] 
	elif i%10==0:
		text = ch_nums[i//10]+'十'
	else:
		text = ch_nums[i//10]+'十'+ch_nums[i%10]
	return text	

def ch_XXXX(i,special_wan = False,after_wan = False):
	text = ''
	zero_flag = False # 照顾到1001，1011 一千零一，一千零一十一这种情况
	flag_1000 = False
	flag_100 = False
	flag_10 = False
	#i = 0 在最后的总函数里单独讨论
	if i//1000 !=0:
		text += ch_nums_special[i//1000]+ch_units[int(log(10,i))]
		flag_1000 = True
		i %= 1000
	if after_wan == True and flag_1000 == False and i != 0:
		text+='零'
	if i//100 !=0:
		text += ch_nums[i//100]+ch_units[int(log(10,i))]
		flag_100 = True
		i %= 100
	else:
		zero_flag = True

	if i//10 !=0:
		flag_10 = True
		if (flag_100 or flag_1000) == False:
			if i//10 != 1 or after_wan == True:
				text += ch_nums[i//10]+ch_units[int(log(10,i))]
			else:
				
				text +=ch_units[int(log(10,i))]

		else:
			if zero_flag == True:
				text += '零'+ch_nums[i//10]+ch_units[int(log(10,i))]
				zero_flag = False
			else:
				text += ch_nums[i//10]+ch_units[int(log(10,i))]
			
		i %= 10
	else:
		zero_flag = True

	if i !=0:
		if zero_flag == True and (flag_100 or flag_1000) == True:
			text += '零'+ch_nums[i]
		else:
			if special_wan == True and (flag_1000 or flag_100 or flag_10)==False:
				text += ch_nums_special[i]
			else:
				text += ch_nums[i]
	return text
def ch_XXXXX(i):
	a = i // 10000
	b = i % 10000
	text = ''
	if a != 0:
		text+=ch_XXXX(a,special_wan = True)+'万'+ch_XXXX(b,after_wan = True)
	else:
		text+=ch_XXXX(b)
	return text
def num2ch(i):
	if i == 0:
		return "零"
	else:
		digits = int(log(10,i))
		yi_digits = int(digits/8)  # yi = log(100000000,i)
		text = ''
		while(yi_digits>=0):
			text+=ch_XXXXX(i//(100000000**yi_digits))
			
			for j in range(yi_digits):
				text+='亿'
			
			i%=100000000**yi_digits
			yi_digits-=1
			
		return text



en_nums = ["zero",'one','two','three','four','five','six','seven','eight','nine','ten']
en_nums_1X = ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
en_nums_X0 = ['zero','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
en_units = ['one','thousand','million','billion','trillion','zillion']
def en_XX(i):
	text = ''
	if 1<=i<10:
		text+=en_nums[i]
	elif 10<=i<20:
		text+=en_nums_1X[i-10]
	elif 20<=i<=99:
		if i%10!=0:
			text+=en_nums_X0[i//10]+'-'+en_nums[i%10]
		else:
			text+=en_nums_X0[i//10]

	return text
def en_XXX(i):
	text = ''
	if i//100 ==0:
		text+=en_XX(i)
	else:
		if i%100==0:
			text+=en_nums[i//100]+' '+'hundred'
		else:
			text+=en_nums[i//100]+' '+'hundred and'+' '+en_XX(i%100)
	return text
def num2en(i):
	text = ''
	

	if i == 0:
		text = 'zero'
	
	else:
		comma = int(log(1000,i))
		if comma == 5:
			if i//1000**5 == 0:
				i %= 1000**5
				comma-=1
			else:
				text += en_XXX(i//1000**5)+" "+en_units[comma]+' '
				i %= 1000**5
				comma-=1
		if comma == 4:
			if i//1000**4 == 0:
				i %= 1000**4
				comma-=1
			else:
				text += en_XXX(i//1000**4)+" "+en_units[comma]+' '
				i %= 1000**4
				comma-=1

		if comma == 3:
			if i//1000**3 == 0:
				i %= 1000**3
				comma-=1
			else:
				text += en_XXX(i//1000**3)+" "+en_units[comma]+' '
				i %= 1000**3
				comma-=1

		if comma == 2:
			if i//1000**2 == 0:
				i %= 1000**2
				comma-=1
			else:
				text += en_XXX(i//1000**2)+" "+en_units[comma]+' '
				i %= 1000**2
				comma-=1
		if comma == 1:
			if i//1000**1 == 0:
				i %= 1000**1
				comma-=1
			else:
				text += en_XXX(i//1000**1)+" "+en_units[comma]+' '
				i %= 1000**1
				comma-=1
		if comma == 0:
			text += en_XXX(i)+' '
	return text


import random
import time,sys

def printentry():
	num = int(var_num.get())
	var_de.set(num2de(num))
	var_en.set(num2en(num))
	var_ch.set(num2ch(num))
def generaterandom():
	num = int(random.uniform(0,999999))
	var_num.set(num)
	var_de.set(num2de(num))
	var_en.set(num2en(num))
	var_ch.set(num2ch(num))
def quit():
	var_de.set("Tschüs!")
	var_en.set("Bye!")
	var_ch.set("再见!")
	print("执行退出程序")

	
	exit()
from tkinter import *

root=Tk()
root.title("Number to Languages (by DavidLXu)") 
var_num=StringVar()
var_num.set(12345)
var_de=StringVar()
var_en=StringVar()
var_ch=StringVar()
var_de.set('Das ist Deutsch')
var_en.set('This is English')
var_ch.set('这是中文')
frame_num = Frame(root)
frame_num.pack(side= TOP,fill = BOTH)
Entry(frame_num,textvariable=var_num).pack(fill = BOTH) #设置输入框对应的文本变量为var

frame_button = Frame(root)
frame_button.pack(side= TOP,fill = Y,expand = YES)
Button(frame_button,text="convert",command=printentry,fg="blue").pack(side = LEFT,fill=Y)
Button(frame_button,text="random",command=generaterandom,fg = "blue").pack(side = LEFT,fill=Y)
Button(frame_button,text="quit",command=quit,fg = "blue").pack(side = RIGHT, fill=Y)

frame_entry = Frame(root)
frame_entry.pack(side= BOTTOM,fill = X,expand = YES)
Entry(frame_entry,textvariable=var_de,width = 55).pack(side = TOP,fill = BOTH)
Entry(frame_entry,textvariable=var_en,width = 55).pack(side = TOP,fill = BOTH)
Entry(frame_entry,textvariable=var_ch,width = 55).pack(side = BOTTOM,fill = BOTH)
root.mainloop()
#print(i,text)
'''
if __name__ == '__main__':	
	for i in range(10000):
		print(i,num2de(i))

#print(de2num(t))
'''