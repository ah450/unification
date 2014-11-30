import my_types as mt
import my_unify as mu

#example a
# vars
a = mt.Expr(mt.ET.var, 'a')
u = mt.Expr(mt.ET.var, 'u')
x = mt.Expr(mt.ET.var, 'x')
v = mt.Expr(mt.ET.var, 'v')
y = mt.Expr(mt.ET.var, 'y')
z = mt.Expr(mt.ET.var, 'z')
# preds
fa = mt.Expr(mt.ET.prd, 'f', [a])
fu = mt.Expr(mt.ET.prd, 'f', [u])
fy = mt.Expr(mt.ET.prd, 'f', [y])
gx = mt.Expr(mt.ET.prd, 'g', [x])
gu = mt.Expr(mt.ET.prd, 'g', [u])
gz = mt.Expr(mt.ET.prd, 'g', [z])
ggz = mt.Expr(mt.ET.prd, 'g', [gz])
gfa =  mt.Expr(mt.ET.prd, 'g', [fa])

# top level
p1 = mt.Expr(mt.ET.prd, 'P', [x, gx, gfa])
p2 = mt.Expr(mt.ET.prd, 'P', [fu, v, v])

#print(mu.unify(p1, p2))
# simple
#print(mu.unify(x,a))
#print(mu.unify(fx,fa))
#print(mu.unify(gfa, gx))
#p3 = mt.Expr(mt.ET.prd, 'P', [x, gx])
#p4 = mt.Expr(mt.ET.prd, 'P', [fu, v])
#print(mu.unify(p3, p4))

# example b
p1 = mt.Expr(mt.ET.prd, 'P', [a, y, fy])
p2 = mt.Expr(mt.ET.prd, 'P', [z, z, u])

#print(mu.unify(p1, p2))

# example c

p1 = mt.Expr(mt.ET.prd, 'P', [x, gx, x])
p2 = mt.Expr(mt.ET.prd, 'P', [gu, ggz, z])
print(mu.unify(p1, p2,True))