#greedy algorithm is used for activity ,job frequency,knap sack,coin change,djiksatras algortihm,hoffman coding,

def mincoins(coins, amount):
    coins.sort(reverse=True)
    res=0
    for x in coins:
        if x<=amount:
            c=amount//x
            res+=c
            amount-=c*x
    if amount==0:
        return res
 
coins=[5,10,2,1]
amount=57
print(mincoins(coins,amount))
#knapsack problem
def knapsack(weights,values,capacity):  
    arr=[]  
    for i in range(len(weights)):  
        arr.append([values[i]/weights[i],weights[i],values[i]])  
    arr.sort(reverse=True)  
    total_value=0  
    for ratio,weight,value in arr:  
        if capacity-weight>=0:  
            capacity-=weight  
            total_value+=value  
        else:  
            total_value+=ratio*capacity  
            break  
    return total_value