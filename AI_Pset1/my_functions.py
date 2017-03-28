import re

def get_global_perc(road_names,predicted_m,actual_m):
    predicted_right=0.0
    predicted_wrong=0.0
    pr_star=0.0
    tot=0
    day_pr=0
    for k in range (0,len(road_names)):
        if(predicted_m[k][0]==actual_m[k][0]):
            predicted_right+=1
        else:   
            predicted_wrong+=1
        tot+=1
        pr_star=predicted_right/len(road_names)
    return pr_star
    

def get_predicted_weight(road_names,road_weights,predicted_m,p_c,p_e,w_a):
    
    adjusted_w=[0.0 for i in range (0,len(road_names))]
    for k in range (0,len(road_names)):
        traffic=predicted_m[k][0]
        #print "taffic" + traffic
        w_a=road_weights[k]
        w_p=0.0
        if (traffic=='low'):
            w_p=p_c*(w_a-w_a*0.1)+p_e*(w_a)+p_e*(w_a+w_a*0.25)
        elif(traffic=='normal'):
            w_p=p_e*(w_a-w_a*0.1)+p_c*(w_a)+p_e*(w_a+w_a*0.25)
        elif(traffic=='heavy'):
            w_p=p_e*(w_a-w_a*0.1)+p_e*(w_a)+p_c*(w_a+w_a*0.25)
    
        adjusted_w[k]=w_p

    return adjusted_w


def read_file(f_loc): 

    graph={}
    predictions={}
    actual={}
    day=1
    graph_num=1
    pr_num=1
    flag_pr='OFF'
    flag_ac='OFF'
    k=1

    f = open(f_loc, 'r')

    for line in f:
        #print line
        buff=re.sub("\n", "", line)
        buff=re.sub(" ", "", buff)
    
        #print "Buff: "+buff
        if (buff == "<Source>"):
            flag='s'
        elif (buff == "</Source>"):
            flag='/s'
        elif (buff == "<Destination>"):
            flag='d'
        elif (buff == "</Destination>"):
            flag='/d'
        elif (buff == "<Roads>"):
            flag='r'
        elif (buff == "</Roads>"):
            flag='/r'
        elif (buff == "<ActualTrafficPerDay>"):
            flag='a'
            flag_ac='ON'
            day=1
            k=1
        elif (buff == "</ActualTrafficPerDay>"):
            flag='/a'
            flag_ac='OFF'
        elif (buff == "<Predictions>"):
            #print "****Prediction Found******"
            flag='p'
            flag_pr='ON'
            #day=1
        elif (buff == "</Predictions>"):
            flag='/p'
            flag_pr='OFF'
        elif (buff == "<Day>"):
            flag='da'
        elif (buff == "</Day>"):
            flag='/da'
        
        

        if (flag=='s' and buff != "<Source>" and flag !='/s') :
            graph['Source']=buff
        elif (flag=='d' and buff != "<Destination>" and flag !='/d') :
            graph['Dest']=buff
        elif (flag=='r' and buff != "<Roads>" and flag !='/r') :
            tmp = buff.split(';')
            graph[str(graph_num)+','+'Name']=tmp[0]
            graph[str(graph_num)+','+'V1']=tmp[1]
            graph[str(graph_num)+','+'V2']=tmp[2]
            graph[str(graph_num)+','+'Weight']=tmp[3]
            graph_num+=1

        elif(flag_pr=='ON' and buff != "<Predictions>" ) :
            #print "****Prediction LOOP******"
        
            if (buff=="<Day>"):
                k=1
            if (buff=="</Day>"):
                day+=1
                k=1
            elif( buff!="<Day>" and buff!="</Day>"):
               # print "In prediction Loop"+ buff +"    k: "+ str(k)
                tmp1 = buff.split(";")
                #print "In day: "+tmp1[0]
                predictions[str(k)+','+str(day)+','+'Name']=tmp1[0]
                predictions[str(k)+','+str(day)+','+'Pre']=tmp1[1]
                k+=1

        elif(flag_ac=='ON' and buff != "<ActualTrafficPerDay>" ) :
            #print "****Prediction LOOP******"
        
        
            if (buff=="</Day>"):
                day+=1
                k=1
            elif( day!=0 and buff!="<Day>" and buff!="</Day>"):
                #print "In prediction Loop"+buff
                tmp1 = buff.split(";")
                #print "In day: "+tmp1[0]
                actual[str(k)+','+str(day)+','+'Name']=tmp1[0]
                actual[str(k)+','+str(day)+','+'Act']=tmp1[1]
                k+=1

        

    return graph, predictions, actual, graph_num

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths