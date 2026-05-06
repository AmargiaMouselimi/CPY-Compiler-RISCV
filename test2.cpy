def main_quadratic():
#{
  #int a, b, c, d

  def square(x):
  #{
    return x * x
  #}

  def root(x):
  #{
    #int i
    i = 1
    while i*i < x:
    #{
      i = i + 1
      return i
    #}
  #}

  a = int(input())
  b = int(input())
  c = int(input())

  d = square(b) - 4 * a * c

  print(square(b))
  print(root(a))
#}

#def main
main_quadratic()
