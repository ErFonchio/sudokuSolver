literal = '198'
s1 = [('+198', '-p7')]
s2 = [('-198', '-998'), ('-128', '-198'), ('-198', '-498'), ('-194', '-198'), 
      ('-198', '-598'), ('-168', '-198'), ('-198', '-398'), ('-197', '-198'), 
      ('-138', '-198'), ('-198', '-388'), ('-198', '-698'), ('-198', '-898'), 
      ('-148', '-198'), ('-193', '-198'), ('-118', '-198'), ('-198', '-298'), 
      ('-198', '-199'), ('-198', '-378'), ('-196', '-198'), ('-198', '-798'), 
      ('-198', '-288'), ('-195', '-198'), ('-188', '-198'), ('-191', '-198'), 
      ('-158', '-198'), ('-178', '-198'), ('-192', '-198'), ('-198', '-278'),]

def applyInference(clause1, clause2, literal):
        clause3 = set()
        for literal1 in clause1:
            if literal1[1:] != literal[1:]:
                clause3.add(literal1)
        for literal2 in clause2:
            if literal2[1:] != literal[1:]:
                clause3.add(literal2)
        return clause3

ret = []
for first in s1:
    for second in s2:
        check = applyInference(first, second, str("-")+literal)
        if len(check) == 1:
            print("Trovato il boss: ", first, second)