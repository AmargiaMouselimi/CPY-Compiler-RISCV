#int x
def p1(x,y):
#{
    #int a,b,c

    def f1(x):
    #{
        #int a
        b = a
        a = x
        c = f1(x)
        return c
    #}
    def f2(x):
    #{
        c = f1(x)
        return c
    #}
    y = x
#}

#def main
##print(f1(1))##
##print(f2(2))##
print(p1(a,b))
