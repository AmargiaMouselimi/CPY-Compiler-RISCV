def main_ex():
#{
    #int b,c,g
    def P1(x,y):
    #{
        y=y-1
        if x==1:
            return x
        else:
            return P1((x-1),y)
    #} 
    c=10
    b=5
    g=P1(c, b) 
#}

#def main
## call of main functions ##
main_ex()