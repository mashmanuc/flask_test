mas1=[1,2,3,4,5,6,7,8]
mas2=[[1,2,1],[2,2,1],[6,2,1],[7,2,1],]
mas=[ ( m[0],m[1 ])  for m in mas2]
print(mas[0][0])
for num , din  in enumerate(mas2):
    print(din)
