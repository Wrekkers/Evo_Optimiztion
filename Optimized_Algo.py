# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:25:39 2017

@author: BHANU
"""

import math
import random


def init_pop(n_var,n_pop,rang):
    pop = []
    for i in range (n_pop):
        contry = []
        for j in range (n_var):
            new_val = rang[j][0] + random.random()*(rang[j][1] - rang[j][0])
            contry.extend([new_val])
        pop.append(contry)
    return pop

def init_range(n_var):
    rang = []
    for i in range(n_var):
        low = 0
        high = 10
        rang.append([low,high])
    return rang
            
def func1(contry,min_max):
    val = contry[0]*math.sin(contry[0]*4) + 1.1*contry[1]*math.sin(2*contry[1])
    if (min_max == 1):
        return (1/(1+val))
    else:
        return val

def evaluate(pop,min_max):
    vals = []
    for cont in pop:
        vals.extend([func1(cont,min_max)])
    return vals

    

def ranking(eval_val,n_imp):
    top = []
    ac_max = max(eval_val)
    for i in range(n_imp+1):
        max_v = ac_max
        curr_ind = 0
        for j in range(len(eval_val)):
            if (j in top):
                continue
            else:
                if (eval_val[j]<max_v):
                    curr_ind = j
                    max_v = eval_val[j]
        top.extend([curr_ind])
    return top

    
def n_cost(eval_val,n_imp,top):
    cost = []
    for i in range(n_imp+1):
        cost.extend([eval_val[top[i]]])
    max1 = max(cost)
    new_cost = []
    for i in range(n_imp+1):
        new_cost.extend([abs(eval_val[top[i]]-max1)])
    prob = []
    sum1 = sum(new_cost)
    for i in range(n_imp):
        if (i==0):
            prob.extend([(new_cost[i])/sum1])
        else:
            prob.extend([((new_cost[i])/sum1)+prob[i-1]])
    return prob


def col_div(prob,top,n_pop,n_imp):
    col = []
    for i in range (n_pop):
        if (i in top):
            col.extend([i])
        else:
            rand = random.random()
            for j in range(n_imp):
                if (rand<prob[j]):
                    col.extend([top[j]])
                    break
                
    col_sort = []
    for i in top:
        new_emp = []
        for j in range(n_pop):
            if (j in top):
                continue
            else:
                if (col[j]==i):
                    new_emp.extend([j])
        col_sort.append(new_emp)
    return col_sort

def update_emp(pop,n_var,n_imp,beta,col_emp,imp,min_max,rang):
    i = 0
    for col in col_emp:
        k=0
        new_imp_ind = imp[i]
        temp = k
        for cont in col:
            new_cont = []
            j=0
            for var in pop[cont]:
                t_val = (var + random.random()*beta*(pop[imp[i]][j]-var))
                if (t_val>rang[j][1]):
                    t_val = rang[j][1]
                if (t_val<rang[j][0]):
                    t_val = rang[j][0]
                new_cont.extend([t_val])
                j+=1
            pop[cont] = new_cont
            if(func1(pop[cont],min_max) < func1(pop[new_imp_ind],min_max)):
                new_imp_ind = cont
                temp = k
            k += 1
        if (new_imp_ind != imp[i]):
            temp1 = imp[i]
            imp[i] = new_imp_ind
            col[temp] = temp1
        i += 1
    
    return pop
    
def cost_emp(pop,imp,col_emp,eta,min_max):
    i=0
    t_cost = []
    for col in col_emp:
        cost_col =0
        for cont in col:
            cost_col += func1(pop[cont],min_max)
        t_cost.extend([func1(pop[imp[i]],min_max) + eta*cost_col])
        i += 1
    
    return t_cost


def pro_emp(t_cost,n_imp):
    max1 = max(t_cost)
    new_cost = []
    for c in t_cost:
        new_cost.extend([abs(c - max1)])
    
    sum1 = sum(new_cost)
    prob = []
    
    for i in range(n_imp):
        if (i==0):
            prob.extend([(new_cost[i])/sum1])
        else:
            prob.extend([((new_cost[i])/sum1)+prob[i-1]])
    
    return prob


# Initial variables

max_iter = 1000
N_pop = 50
N_imp = 5
N_var = 2
beta = 1.5
eta = 0.1
min_max = 0

var_range = init_range(N_var)
emp_pop = init_pop(N_var,N_pop,var_range)

vals  = evaluate(emp_pop,min_max)

imps = ranking(vals,N_imp)

imp_pro = n_cost(vals, N_imp, imps)

del imps[-1]

colonies = col_div(imp_pro,imps,N_pop, N_imp)


w_emp = 0
b_emp = 0

for it in range(max_iter):
    if(N_imp == 1):
        break
    emp_pop = update_emp(emp_pop, N_var, N_imp, beta, colonies, imps, min_max, var_range)
    cost_emps = cost_emp(emp_pop, imps, colonies, eta, min_max)
    t1 = max(cost_emps)
    t2 = min(cost_emps)
    c2 = 0
    for c1 in cost_emps:
        if t1 == c1:
            w_emp = c2
        if t2 == c1:
            b_emp = c2
        c2 += 1
        
    pros_emps = pro_emp(cost_emps,N_imp)
    del1 = 0
    
    if (len(colonies[w_emp])==1):
        temp_cont = colonies[w_emp][0]
        colonies.pop(w_emp)
        del1 = 1
        
    else:    
        #print("w_emp = ",w_emp)
        lst_cont = func1(emp_pop[colonies[w_emp][0]], min_max)
        l_ind = 0
        d_ind = 0
        for col in colonies[w_emp]:
            if (lst_cont > func1(emp_pop[col], min_max)):
                l_ind = d_ind
                lst_cont = func1(emp_pop[col], min_max)
            d_ind += 1
    
        temp_cont = colonies[w_emp][l_ind]
        colonies[w_emp].pop(l_ind)
        
    
    rand1 = random.random()
    
    p_ind = 0
    for p in pros_emps:
        if (rand1<p):
            colonies[p_ind].extend([temp_cont])
            break
        p_ind += 1
    
    if (del1 == 1):
        N_imp -= 1
        temp_cont = imps[w_emp]
        imps.pop(w_emp)
        p_ind = 0
        for p in pros_emps:
            if (rand1<p):
                colonies[p_ind].extend([temp_cont])
                break
            p_ind += 1
    #print(pros_emps)

print(emp_pop[imps[b_emp]])
print(func1(emp_pop[imps[b_emp]],min_max))

