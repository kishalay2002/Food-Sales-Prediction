import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from datetime import datetime

pd.options.mode.chained_assignment = None  # default='warn'


items_ordered=pd.read_json('items_ordered.json')
orders=pd.read_json('orders.json')
orders.rename(columns={'id':'order_id'},inplace=True)
new_dataframe=pd.merge(items_ordered,orders,on='order_id',how='inner')

#dropping unnecessary columns
new_dataframe.drop(['amount_paid','ordered_at_time','delivered_at','delivered_at_time','delivered_to'],axis=1,inplace=True)


#Converting string in dates to datetime objects
new_dataframe['ordered_at']=pd.to_datetime(new_dataframe['ordered_at'])
#print(new_dataframe.head(20))

#creating a dataframe for each item and sorting by order_id date
tikka_sandwich=new_dataframe.loc[new_dataframe['name']=='chicken-tikka-sandwich']
tikka_sandwich.sort_values(by='ordered_at',inplace=True)

cheese_sandwich=new_dataframe.loc[new_dataframe['name']=='grilled-cheese-sandwich']
cheese_sandwich.sort_values(by='ordered_at',inplace=True)

burger=new_dataframe.loc[new_dataframe['name']=='chicken-burger']
burger.sort_values(by='ordered_at',inplace=True)

almond_biscotti=new_dataframe.loc[new_dataframe['name']=='almond-choco-dip-biscotti']
almond_biscotti.sort_values(by='ordered_at',inplace=True)

soda=new_dataframe.loc[new_dataframe['name']=='soda']
soda.sort_values(by='ordered_at',inplace=True)

juice=new_dataframe.loc[new_dataframe['name']=='juice']
juice.sort_values(by='ordered_at',inplace=True)

cake=new_dataframe.loc[new_dataframe['name']=='cake']
cake.sort_values(by='ordered_at',inplace=True)

week_days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
m_days=[31,28,31,30,31,30,31,31,30,31,30,31]

#Much simplified as our dataset is within a year
def get_next_day(date_now)->():


	day_now=date_now.day
	month=date_now.month
	year=date_now.year

	new_day,new_month,new_year=(day_now+7)%m_days[month-1],0,2015

	if day_now+7<=m_days[month-1]:
		new_month=month

	elif day_now+7>m_days[month-1] and month<12:
		new_month=month+1

	else:
		print("Came Here")
		return (0,0,0)

	if new_day==0:
		new_day=m_days[month-1]
	return new_day,new_month,new_year

def calculate_regr(dataframe):

	start_date=dataframe.iloc[0]['ordered_at']
	end_date=dataframe.iloc[-1]['ordered_at']

	print(dataframe)

	start_week=start_date.weekday()

	count_loop=0
	while count_loop<7:
		sales=[]
		query_date=start_date
		dd,mm,yy=query_date.day,query_date.month,query_date.year

		print(f"\nFor {week_days[start_week]}\n")
		while yy>0 and query_date<=end_date:
			
			temp=len(dataframe.loc[dataframe['ordered_at']==query_date])
			if temp>0:
				sales.append(temp)
			else:
				sales.append(sum(sales)//len(sales))

			dd,mm,yy=get_next_day(query_date)
			query_date=datetime(yy,mm,dd)

		y=[i for i in range(1,len(sales)+1)]
		print(len(sales))
		sales_arr=np.array(sales).reshape(-1,1)
		y_arr=np.array(y).reshape(-1,1)

		try:

			X_train, X_test, y_train, y_test = train_test_split(sales_arr, y_arr, test_size = 0.4)
			regr = LinearRegression()
		 
			regr.fit(X_train, y_train)
			print(regr.score(X_test, y_test))

		except:
			print("Not Enough Data!! Could Not be calculated")

		count_loop+=1
		start_week=(start_week+1)%7


print("Press 1 to calculate for Chicken tikka sandwich")
print("Press 2 to calculate for grilled cheese sandwich")
print("Press 3 to calculate for Chicken burger")
print("Press 4 to calculate for Almond choco dip biscotti")
print("Press 5 to calculate for Soda")
print("Press 6 to calculate for Cake")
print("Press 7 to calculate for Juice")

choice=int(input("Enter your choice: "))

if choice==1:
	print("Regression score for Chicken tikka sandwich")
	calculate_regr(tikka_sandwich)
elif choice==2:
	print("Regression score for Grilled Cheese sandwich")
	calculate_regr(cheese_sandwich)
elif choice==3:
	print("Regression score for Chicken burger")
	calculate_regr(burger)
elif choice==4:
	print("Regression score for Almond choco dip biscotti")
	calculate_regr(almond_biscotti)
elif choice==5:
	print("Regression score for Soda")
	calculate_regr(soda)
elif choice==6:
	print("Regression score for Cake")
	calculate_regr(cake)
elif choice==7:
	print("Regression score for Juice")
	calculate_regr(juice)


#print(new_dataframe.name.value_counts())
#print(new_dataframe.name.unique())
#print(new_dataframe.loc[new_dataframe['order_id']==114])