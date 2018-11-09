
from node import Node
import math


def ID3(examples, default=0):
    
    if examples ==[]:
        
        new_node = Node()
        new_node.label=default
        new_node.isleaf=True
   
        return new_node
    
    if len(categories(examples,'Class')) == 1:
        new_node = Node()
        new_node.label=mode(examples)
        new_node.mode_perc=mode_perc(examples)
        new_node.isleaf=True

     
        return new_node
    
    else :
        var  = best_splitting_attribute(examples)
        categories_temp = categories(examples,var)
        tree = Node()
        tree.label=var
        tree.mode = mode(examples) 
        tree.mode_perc=mode_perc(examples)
        tree.isleaf=False
        tree.categories = categories_temp
   
  
        
        for value in tree.categories:
            tempk = [ temp for temp in examples if temp[var] == value ]
            
            subtree = ID3(tempk,mode(tempk))
            
            tree.children[value] = subtree
         
            
    return tree


def prune(node, examples):
    prev_accuracy =0
    after_accuracy =1
    
    list1 = traversal(node)
    nodes_level_order_leaf =  [x for x in list1 if x.isleaf == False]
    
    nodes_with_leaf=[]

    for i in nodes_level_order_leaf:
        
        is_chidren_leaf=False
        
        for j in i.categories:
            if i.children[j].isleaf ==True:
                is_chidren_leaf=True
                break
        
        if is_chidren_leaf==True:
            nodes_with_leaf.append(i)
    
    
        prev_accuracy = test(node,examples) 
        
        
        
        for j in nodes_with_leaf:
            node_del = j
            
            for i in node_del.categories:
                if node_del.children[i].isleaf == True:
                    temp_label = node_del.children[i].label
                    node_del.children[i].label = node_del.mode
                    
                    after_accuracy =test(node,examples)
                    
                    if after_accuracy < prev_accuracy:
                        node_del.children[i].label = temp_label
                        
                    
                    
    
    #node_del.label = label_temp
    #node_del.chidren = children_dict_temp
    
    #print(" the preserved lable {} and dict are {}".format(label_temp,children_dict_temp))
    
  
    
def traversal(node):
 
    Q=[node]
    level_order_list =[]
    count = 0
    while Q:
        
        count +=1
        
        current=Q.pop(0)
        level_order_list.append(current)
        
        for key,child in current.children.items():
            Q.append(child)
    return level_order_list
    

def test(node, examples):
    length =len(examples)
    correct = 0
    wrong = 0
    
    for i in examples:
        temp = evaluate(node,i)
        if temp==i['Class']:
            correct+=1
        else:
            wrong+=1
            
    return (correct/ (wrong+correct))
    

def evaluate(node, example):
    
    temp =node
    
    while temp.children !={}:
        
        if  example[temp.label] not in temp.children:
            return temp.mode
        else:
            temp = temp.children[example[temp.label]]
    
    return temp.label

def best_splitting_attribute(examples):
    
    info_gain={}

    for i in examples[0].keys():
        if i !='Class':
            info_gain[i]= entropy(examples) - weighted_entropy(examples,i)

    max=0
    
    for k,v in info_gain.items():
        if v>max:
            max=v
            key_max=k
    return key_max


def categories(examples,column):
    list_attribute=[]
    
    for i in examples:
        if i[column] not in list_attribute:
            list_attribute.append(i[column])
    
    return list_attribute



def entropy(examples):
    freq_dict={}
    for i in examples:
        if i['Class'] not in freq_dict:
            freq_dict[i['Class']] =1 
        else:
            freq_dict[i['Class']] +=1
    
    total =0
    entropy = 0
    
    for i in freq_dict:
        total += freq_dict[i]
    
    for i in freq_dict:
        var = freq_dict[i]/total
        
        if var !=0 :
            entropy += var * math.log2(var)
    
    entropy = entropy * -1
    
    return entropy


def weighted_entropy(examples,column):
    
    freq_dict={}
    for i in examples:
        if i[column] not in freq_dict:
            freq_dict[i[column]] =1 
        else:
            freq_dict[i[column]] +=1
    
    #print(freq_dict)

    total =0

    for i in freq_dict:
        total += freq_dict[i]
    #print(total)
    
    weighted_entropy = 0
    
             
    for k in freq_dict:
        weighted_entropy += (freq_dict[k]/total) * entropy([ temp for temp in examples if temp[column] == k ])

    return weighted_entropy

def mode(examples):

    freq_dict={}
    max_count=-1
    for i in examples:
        if i['Class'] not in freq_dict:
            freq_dict[i['Class']] =1 
        else:
            freq_dict[i['Class']] +=1
            
        if freq_dict[i['Class']]>max_count:
            max_count = freq_dict[i['Class']]
            max_item = i['Class']
        
    return max_item

def mode_perc(examples):

    freq_dict={}
    max_count=-1
    for i in examples:
        if i['Class'] not in freq_dict:
            freq_dict[i['Class']] =1 
        else:
            freq_dict[i['Class']] +=1
            
        if freq_dict[i['Class']]>max_count:
            max_count = freq_dict[i['Class']]
            max_item = i['Class']
            
    mode_perc = max_count/ sum(freq_dict.values())
    return mode_perc

"""
data = [dict(a=0, b=1, c=1, d=0, Class=1), dict(a=0, b=0, c=1, d=0, Class=0), dict(a=0, b=1, c=0, d=0, Class=1), dict(a=1, b=0, c=1, d=0, Class=0), dict(a=1, b=1, c=0, d=0, Class=0), dict(a=1, b=1, c=0, d=1, Class=0), dict(a=1, b=1, c=1, d=0, Class=0)]
validationData = [dict(a=0, b=0, c=1, d=0, Class=1), dict(a=1, b=1, c=1, d=1, Class = 0)]

tree = ID3(data)
ans = test(tree, validationData)

prune(tree,validationData)

#print("the final is {}".format(test(tree, validationData)))
"""







