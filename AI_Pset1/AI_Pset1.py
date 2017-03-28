import time
import my_functions
from graph import Graph,Vertex

f_glob_pr = my_functions.get_global_perc
f_pred_w = my_functions.get_predicted_weight
f_file = my_functions.read_file

#f_loc='C:/Users/Filippos/Desktop/Artificial Intelligence/PSet1/AI_Dataset1.txt'
f_loc='C:/Users/Filippos/Desktop/Artificial Intelligence/PSet1/sampleGraph3.txt'

graph, predictions, actual, graph_num = f_file(f_loc)

start_time=time.clock()




costs={}
pr_num=1

days=1
g=Graph()

g.add_vertex(graph['Source'])
g.add_vertex(graph['Dest'])
for gr in range (1,graph_num):
    if (graph[str(gr)+","+"Name"]!=''):
        g.add_vertex(graph[str(gr)+","+'V1'])


road_names=[]
#road_edges=[[]for i in range(2)]
road_from=[]
road_to=[]
road_weights=[]

for gr in range (1,graph_num):
    if (graph[str(gr)+","+'Name']!=KeyError and graph[str(gr)+","+'V1'] !=KeyError ):
        road_from.append(graph[str(gr)+","+'V1'])
        road_to.append(graph[str(gr)+","+'V2'])
        road_names.append(graph[str(gr)+","+'Name'])
        road_weights.append(int(graph[str(gr)+","+'Weight']))
        g.add_edge(graph[str(gr)+","+'V1'],graph[str(gr)+","+'V2'],int(graph[str(gr)+","+'Weight']))
       
# Set 1 to print 0 to not print, Used for Debuggimg Purposes
if (1):
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print '( %s , %s, %3d, %f )'  % ( vid, wid, v.get_weight(w),v.get_cost_so_far() )

    for v in g:
        print 'g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()])

#
#   Here are implemented the probability recalculations, for each day, looking ahead 
#   is not permitted 
#

p_c=0.6
p_e=0.2
w_a=0
days+=1

w, h = days, len(road_names);
predicted_m = [[0 for x in range(w)] for y in range(h)] 
w, h = days-1, len(road_names);
actual_m  = [[0 for x in range(w)] for y in range(h)] 

for k in range (0,len(road_names)):
    for l in range (0,days):
        predicted_m[k][l]=predictions[str(k+1)+','+str(l+1)+','+ 'Pre']


#g.set_cost_so_far('A',23.2)

for k in range (0,len(road_names)):
    for l in range (0,days-1):
        actual_m[k][l]=actual[str(k+1)+','+str(l+1)+','+ 'Act']



filled_list_time=time.clock()

print "\n\nTime to fill the lists:"
print filled_list_time-start_time




# Call functions to get probabilities and adj weigths

pr_star= f_glob_pr(road_names,predicted_m,actual_m)

adjusted_w=f_pred_w(road_names,road_weights,predicted_m,p_c,p_e,w_a)

print "Road ----  From | To"
for i in range (0,len(road_names)):
    print road_names[i] + '  '+ road_from[i] +'  '+ road_to[i]


print "\nPrediction Correct Probability: " + str(pr_star)
print "Weigth comparisson"
print road_weights
print adjusted_w

##########

cur_day=1

##########

#find the probabilities of global_Correct, global_{H,M,L}, per_raod_{H,M,L}
###

#Set the adj weigth for the first day 

#koitwntas tous geitones xekinwntas apo ton arxiko, kanw set tha adj weights
#
# 
frontier=[0.0 for i in range (0,len(road_names))]
tmp_graph_name=graph['Source']

print tmp_graph_name
neighbours=str (g.vert_dict[tmp_graph_name])
print "Neighbours" + neighbours

for i in range (0,len(road_names)):
    print road_names[i],road_to[i]
    if neighbours in road_to[i]:
        frontier[i]=adjusted_w[i]

print "Current Frontier"
print frontier


#road_names[i]

############################
#Depth-First Search

#fringe := [make_node(start_state, null, null)]
fringe=[]
fringe.append(graph['Source'],0,0)
#reached_limit := false
limit=3
reached_limit = False

while not fringe:
    n = fringe.pop(3)

    #if n.state is a goal state: return n.actionListFromRoot()
    if n[1]==graph['Dest']:
        #here I should return the action list
        break
        

    if n.depth == limit:

        reached_limit = True

    else:

        #for each action a applicable to n.state
        for j in range (1,len(n)):
            if road_from==n[j]:
                fringe.append(road_from[j],road_to[j])
                fringe.append(make_node(succ(n.state, a), a, n))

#return reached_limit ? cutoff : failure
    if (reached_limit):
    #how to 
        break 

"""
for i in range (455):
    run DLS to level i
    if found a goal at level i, return it immediately

"""

