import random
import math
import time
import matplotlib.pyplot as plt
import pygame

points = [] #array of x-y points
n = random.randint(5,12) #select a random number of points
#n = 10
lower_bound = -1000000 #lower bound for the coordinate values 
upper_bound = 1000000 #upper bound for the coordinate values 

def getKey(item): #useful for sorting wrt distance 
    return item[2]

def getKey2(item): #useful for sorting wrt angle 
    return item[3]

def comp(list1, list2): #comparing two lists with 4 items each 
    if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3]:
        return True
    return False

def check_points_convex(x1, y1, x2, y2, x, y):
    value = ((x2 - x1)*(y - y1)) - ((y2 - y1)*(x - x1))
    if value > 0:
        return False
    return True

    

class Node:
    #Constructor to create a node of the linked list
    def __init__(self, x, y, distance, angle):
        self.x = x
        self.y = y
        self.distance = distance
        self.angle = angle
        self.next = None
 
class CircularLinkedList:
    # Constructor to create a empty circular linked list
    def __init__(self):
        self.head = None
 
    # Function to insert a node at the beginning of a
    # circular linked list
    def push(self, x, y, distance, angle):
        ptr1 = Node(x, y, distance, angle)
        temp = self.head
         
        ptr1.next = self.head
 
        # If linked list is not None then set the next of
        # last node
        if self.head is not None:
            while(temp.next != self.head):
                temp = temp.next
            temp.next = ptr1
 
        else:
            ptr1.next = ptr1 # For the first node
 
        self.head = ptr1

    def delete(self,prev,latter):
        self.next = latter
        
    # Function to print nodes in a given circular linked list
    def printList(self):
        temp = self.head
        if self.head is not None:
            while(True):
                print(temp.x, temp.y, temp.distance, temp.angle),
                temp = temp.next
                if (temp == self.head):
                    break

    def print_h(self):
        temp = self.head
        count=1
        if self.head is not None:
            while(True):
                count+=1
                temp = temp.next
                if (temp == self.head):
                    break
        print("\n\nThe value for h is " + str(count))



for i in range(0,n):
    x = [random.randint(lower_bound, upper_bound),random.randint(lower_bound, upper_bound)]
    points.append(x)
##n = 12
##points = [[-18, 59], [-95, -73],[-34, -72],[81, -79],[42, 34],[6, -67],[-58, 63],[-25, -13],[-97, -90],[33, -63],[-95, -29],[86, 43]]
##for i in range (0,n):
##    print(str(points[i][0]) + " " + str(points[i][1]) + "\n")

meanx = 0 #mean of the x coordinates 
meany = 0 #mean of the y coordinates 

for i in range (0,n):
    meanx = meanx + points[i][0]
    meany = meany + points[i][1]

meanx = (1.0*meanx)/n
meany = (1.0*meany)/n

max_index = 0 #max_index is the index with the maximum x coordinate
min_index = 0

for i in range (1,n):
    if points[max_index][0] < points[i][0]: #in case of tie it chooses the first occurence of that x coordinate 
        max_index = i
    if points[min_index][0] > points[i][0]:
        min_index = i



Q1 = [] #first quadrant 
Q2 = [] #second quadrant 
Q3 = [] #third quadrant 
Q4 = [] #fourth quadrant 


for i in range(0,n):
    distance = math.sqrt( (points[i][0] - meanx)**2 + (points[i][1] - meany)**2 ) #distance 

    angle1 = math.degrees( math.atan2( points[i][1]-meany , points[i][0]-meanx ) )
    angle2 = math.degrees( math.atan2( points[max_index][1]-meany , points[max_index][0]-meanx ) )

    angle = (angle1 - angle2) #polar angle

    if angle<0:
        angle = angle + 360

    if i != max_index and i != min_index:
        if points[i][0] > meanx and points[i][1] >= meany:
            Q1.append([points[i][0], points[i][1], distance, angle])
        elif points[i][0] <= meanx and points[i][1] > meany:
            Q2.append([points[i][0], points[i][1], distance, angle])
        elif points[i][0] < meanx and points[i][1] <= meany:
            Q3.append([points[i][0], points[i][1], distance, angle])
        elif points[i][0] >= meanx and points[i][1] < meany:
            Q4.append([points[i][0], points[i][1], distance, angle])
        

    elif i == max_index:
        max_data = Node(points[max_index][0],points[max_index][1],distance,angle)

    elif i == min_index:
        min_data = Node(points[min_index][0],points[min_index][1],distance,angle)

        


#sort the point in the four lists according to the distance from mean point

Q1.sort(key=getKey)
Q2.sort(key=getKey)
Q3.sort(key=getKey)
Q4.sort(key=getKey)


q1 = len(Q1)
q2 = len(Q2)
q3 = len(Q3)
q4 = len(Q4)

convex_hull = CircularLinkedList()
#pushing the max xcoordinate and the min x coordinate points separately into the linked list
convex_hull.push(min_data.x, min_data.y, min_data.distance, min_data.angle)
convex_hull.push(max_data.x, max_data.y, max_data.distance, max_data.angle)



while q1 > 0 or q2 > 0 or q3 > 0 or q4 > 0:
    A = [0,0,0,0]
    B = [0,0,0,0]
    C = [0,0,0,0]
    D = [0,0,0,0]
    X = [0,0,0,0]
    
    if q1 > 0:
        A = Q1[q1-1]
        del Q1[-1] #delete the last element of Q1
        q1 = q1 - 1
    else:
        A = Q1

    if q2 > 0:
        B = Q2[q2-1]
        del Q2[-1]
        q2 = q2 - 1
    else:
        B = Q2

    if q3 > 0:
        C = Q3[q3-1]
        del Q3[-1]
        q3 = q3 - 1
    else:
        C = Q3

    if q4 > 0:
        D = Q4[q4-1]
        del Q4[-1]
        q4 = q4 - 1
    else:
        D = Q4

    temp_list = []
    if A and not comp(A, X):
        temp_list.append(A)
    if B and not comp(B, X):
        temp_list.append(B)
    if C and not comp(C, X):
        temp_list.append(C)
    if D and not comp(D, X):
        temp_list.append(D)


    if temp_list:        
        temp_list.sort(key=getKey2)

        length = len(temp_list) #length has to be less than or equal to 4
        
        for i in range(0, length): #this for loop helps to insert a node in sorted order in our linked list 
            curr = convex_hull.head
            nxt = curr.next

            while nxt != convex_hull.head:
                if temp_list[i][3] > curr.angle and temp_list[i][3] < nxt.angle:
                    new_node = Node(temp_list[i][0], temp_list[i][1], temp_list[i][2], temp_list[i][3])
                    curr.next = new_node
                    new_node.next = nxt
                    break
                    
                curr = curr.next
                nxt = nxt.next
                

            if nxt == convex_hull.head:
                new_node = Node(temp_list[i][0], temp_list[i][1], temp_list[i][2], temp_list[i][3])
                curr.next = new_node
                new_node.next = convex_hull.head
                


        prev = convex_hull.head
        curr = prev.next
        nxt = curr.next
        
        while True: 
            if curr == convex_hull.head:
                break

            if not check_points_convex(prev.x, prev.y, nxt.x, nxt.y, curr.x, curr.y): #delete the point curr 
                curr = nxt
                nxt = nxt.next
                prev.next = curr
                #change made here
                #assume that prev = 1, curr = 2, and nxt = 3 and then we have 4 and 5 initially, if curr was deleted, prev was set to 3
                #curr was set to 4 and nxt was set to 5. now if curr is deleted, prev stays at 1, curr is set to 3 amd nxt is 4.
                #in any one iteration, we remove all points that give errors instead of going around twice. 

            else:
                prev = prev.next
                curr = curr.next
                nxt = nxt.next
                


print("\n\nThe final convex hull is:\n\n")
convex_hull.printList()

convex_hull.print_h()


#plotting the convex hull


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('n = ' + str(n))

for i in range(0,n):
    ax.scatter(points[i][0], points[i][1])

ax.scatter(meanx, meany, color='red')

curr = convex_hull.head
nxt = curr.next	

while(True):
    ax.scatter(curr.x,curr.y,color='green')
    curr = curr.next
    nxt = nxt.next
    if (nxt == convex_hull.head.next):
        break


curr = convex_hull.head
nxt = curr.next	

#vert line
ax.axvline(x=meanx,color='black',ls='dashed')
#horiz line
ax.axhline(y=meany,color='black',ls='dashed')

while(True):
    ax.plot([curr.x,nxt.x],[curr.y,nxt.y],color='black')
    curr = curr.next
    nxt = nxt.next
    if (nxt == convex_hull.head.next):
        break


plt.show()
