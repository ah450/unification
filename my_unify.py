import my_types as mt

def unify(E1, E2):
    subs = unify1(mt.listify(E1), mt.listify(E2), [])
    if type(subs) == list:
        for s in subs:
            s.value = mt.delistify(s.value)
    return subs

def unifyVar(x, e, subs):

    print('unify var ' + str(x) + ' '+ str(e)+ ' subs '+str(subs))
    prev= None
    for y in subs:
        if y.name == x:
            print('prev subst exists')
            prev = y
            break
    if prev != None:
        t = prev.value
        print('use prev subst' + str(t))
        return unify1(t, e, subs)
    print('before subs applied ' + str(e)) 
    t = mt.subst(subs, e)
    print('after subs applied ' + str(t))
    if mt.exists(x, t):
        print('x exists in t')
        return None
    sub = mt.Sub(x, t)
    print('add sub '+ str(sub))
    for s in subs:
        s.value = mt.subst1(sub, s.value)
    print('after apply new sub on old sub', subs)
    subs.append(sub)
    return subs


def unify1(E1, E2, sub):
    print("unifying " + str(E1) +" "+ str(E2) )
    if sub == None:
        print("fail")
        return None
    if E1 == E2:
        print("equal")
        return sub
    if type(E1) == mt.Expr and E1.type == mt.ET.var:
        print("var first")
        z= unifyVar(E1, E2, sub)
        return z
    if type(E2) == mt.Expr and E2.type == mt.ET.var:
        print("var second")
        return unifyVar(E2, E1, sub)
    if type(E1) == mt.Expr and type(E2) == mt.Expr:
        if E1.type == mt.ET.atm or  E2.type == mt.ET.atm:
            print("either is atom")
            return None
    if len(E1) != len(E2):
        print("different length")
        return None
    return unify1(E1[1:], E2[1:], unify1(E1[0], E2[0], sub))

