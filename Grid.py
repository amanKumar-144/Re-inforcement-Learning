import numpy as np
import random
class RL:
    def __init__(self,m,n):
        self.m=m;
        self.n=n;
        self.grid=[];
        self.denominator=[];
        self.numerator=[];
        self.vScores=[];
        self.policy=[];
        self.iter=1000;
        self.discountFactor=0.98;
        
        self.restricted=[];
    
        for i in range(m):
            l=[];
            for j in range(n):
                l.append(-1);
            self.policy.append(l);
            
        
        for i in range(m):
            l1=np.zeros(n);
            l2=np.ones(n);
            self.grid.append(l1.copy());
            self.numerator.append(l1.copy());
            self.vScores.append(l1.copy());
            
        for i in range(m):
            l1=[]
            if(i==0 or i==m-1):
                for j in range(n):
                    if(j==0 or j==n-1):
                        l1.append(2);
                    else:
                        l1.append(3);
            else:
                for j in range(n):
                    if(j==0 or j==n-1):
                        l1.append(3);
                    else:
                        l1.append(4);
            self.denominator.append(l1);
                    
    def inverseMapping(self):
        for i in range(self.m):
            for j in range(self.n):
                if(self.policy[i][j]==0):
                    self.policy[i][j]='W'; 
                if(self.policy[i][j]==1):
                    self.policy[i][j]='E'; 
                if(self.policy[i][j]==2):
                    self.policy[i][j]='N'; 
                if(self.policy[i][j]==3):
                    self.policy[i][j]='S';    
                        
    def changeNum(self,maxIndex,x,y):
        if(maxIndex==0):
            self.numerator[x][y-1]+=1;
        elif(maxIndex==1):
            self.numerator[x][y+1]+=1;
        elif(maxIndex==2):
            self.numerator[x-1][y]+=1;
        elif(maxIndex==3):
            self.numerator[x+1][y]+=1;
           
    def printDetails(self):
        print("The rows are columns are ",self.m," ",self.n);
        print("The grid is :-");
        '''for rows in self.grid:
            print(rows);
            
        print("The denominators are ");
        for rows in self.denominator:
            print(rows);
            
        print("The numerators are ");
        for rows in self.numerator:
            print(rows);'''
            
        print("The scores are ");
        for rows in self.vScores:
            print(rows);
            
        print("The policy matrix is ");
        for rows in self.policy:
            print(rows);
            
            
    def initializeGrid(self,inp):
        #inp is number of inputs we want to give;
        for i in range(self.m):
            for j in range(self.n):
                self.grid[i][j]=-0.02;
        '''
        for i in range(inp):
            x=int(input("Enter X:"));
            y=int(input("Enter Y:"));
            reward=int(input("Enter Reward:"));
            self.grid[x][y]=reward;'''
        self.grid[0][0]=0;
        self.grid[0][1]=10;
        self.grid[4][3]=10000;
        self.grid[1][3]=-100;
        self.grid[3][2]=-50;
        self.restricted.append([0,0]);
        self.restricted.append([0,1]);
        self.restricted.append([4,3]);
        self.restricted.append([1,3]);
        self.restricted.append([3,2]);
                
    
      
    #90% According to transition probability and 10% according to random jumping
    def compute(self):
        prevV=self.vScores;
        for iter in range(self.iter):
            for i in range(self.m):
                for j in range(self.n):
                    
                    if [i,j] in self.restricted:
                        continue;
                    
                    rNumber=random.randint(1, 10);
                    useRandom=0;
                    #VERY Important to use this
                    if(rNumber<=1):
                        useRandom=1;
                        
                    x=i;
                    y=j;
                    scores=[-1000,-1000,-1000,-1000];#W(0) E(1) N(2) S(3)
                    sel=[-1,-1,-1,-1];#USE When we use random
                    
                    if(y-1>=0):
                        num=self.numerator[x][y-1];
                        den=self.denominator[x][y-1];
                        prob=num/den;
                        scores[0]=prob*self.grid[x][y-1]+self.discountFactor*prob*prevV[x][y-1];
                        self.denominator[x][y-1]+=1;
                        sel[0]=1;
                        
                            
                    if(y+1<self.n):
                        num=self.numerator[x][y+1];
                        den=self.denominator[x][y+1];
                        prob=num/den;
                        scores[1]=prob*self.grid[x][y+1]+self.discountFactor*prob*prevV[x][y+1];
                        self.denominator[x][y+1]+=1;
                        sel[1]=1;
                        
                        
                    if(x-1>=0):
                        num=self.numerator[x-1][y];
                        den=self.denominator[x-1][y];
                        prob=num/den;
                        scores[2]=prob*self.grid[x-1][y]+self.discountFactor*prob*prevV[x-1][y];
                        self.denominator[x-1][y]+=1;
                        sel[2]=1;
                        
                        
                    if(x+1<self.m):
                        num=self.numerator[x+1][y];
                        den=self.denominator[x+1][y];
                        prob=num/den;
                        scores[3]=prob*self.grid[x+1][y]+self.discountFactor*prob*prevV[x+1][y];
                        self.denominator[x+1][y]+=1;
                        sel[3]=1;
                       
                        
                    maxIndex=0;
                    maxScore=-1001;
                    for k in range(4):
                        if(scores[k]>maxScore):
                            maxScore=scores[k];
                            maxIndex=k;
                            
                    if(useRandom==0):      
                        self.vScores[x][y]=scores[maxIndex];
                        self.policy[x][y]=maxIndex;
                        self.changeNum(maxIndex,x,y);
                        
                    else:
                        l=[];
                        for k in range(4):
                            if(sel[k]==1):
                                l.append(k);
                        index=random.choice(l);
                        self.vScores[x][y]=scores[index];
                        self.policy[x][y]=index;
                        self.changeNum(index,x,y);
                    
                        
        
        
        
      
if __name__=='__main__':        
    obj=RL(5,4);
    obj.initializeGrid(4);
    obj.printDetails();
    obj.compute();
    obj.inverseMapping();
    obj.printDetails()

        
    