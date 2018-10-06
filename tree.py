#arvore em que o que está à:
#direta do pai é o elemento que vai a seguir ao pai
#esquerda do pai são os dois elementos que vêm a seguir ao pai
#                   root
#             -                -
#            N                 Ne        
#       -         -           -   -  
#       e         eo        o      on
#     -   -      -  -      - -      .
#    o     on   n   .     n  .
#   -     .  .
# n  .
#

# =========================== TABELA PERIODICA ===========================

tp = { 
    'h': 1,
    'he': 2,
    'li': 2,
    'be': 2,
    'b': 1,
    'c': 1,
    'n': 1,
    'o': 1,
    'f': 1,
    'ne': 2,
    'na': 2,
    'mg': 2,
    'al': 2,
    'si': 2,
    'p': 1,
    's': 1,
    'cl': 2,
    'ar': 2,
    'k': 1,
    'ca': 2,
    'sc': 2,
    'ti': 2,
    'v': 1,
    'cr': 2,
    'mn': 2,
    'fe': 2,
    'co': 2,
    'ni': 2,
    'cu': 2,
    'zn': 2,
    'ga': 2,
    'ge': 2,
    'as': 2,
    'se': 2,
    'br': 2,
    'kr': 2,
    'rb': 2,
    'sr': 2,
    'y': 1,
    'zr': 2,
    'nb': 2,
    'mo': 2,
    'tc': 2,
    'ru': 2,
    'rh': 2,
    'pd': 2,
    'ag': 2,
    'cd': 2,
    'in': 2,
    'sn': 2,
    'sb': 2,
    'te': 2,
    'i': 1,
    'xe': 2,
    'cs': 2,
    'ba': 2,
    'la': 2,
    'ce': 2,
    'pr': 2,
    'nd': 2,
    'pm': 2,
    'sm': 2,
    'eu': 2,
    'gd': 2,
    'tb': 2,
    'dy': 2,
    'ho': 2,
    'er': 2,
    'tm': 2,
    'yb': 2,
    'lu': 2,
    'hf': 2,
    'ta': 2,
    'w': 1,
    're': 2,
    'os': 2,
    'ir': 2,
    'pt': 2,
    'au': 2,
    'hg': 2,
    'tl': 2,
    'pb': 2,
    'bi': 2,
    'po': 2,
    'at': 2,
    'rn': 2,
    'fr': 2,
    'ra': 2,
    'ac': 2,
    'th': 2,
    'pa': 2,
    'u': 1,
    'np': 2,
    'pu': 2,
    'am': 2,
    'cm': 2,
    'bk': 2,
    'cf': 2,
    'es': 2,
    'fm': 2,
    'md': 2,
    'no': 2,
    'lr': 2,
    'rf': 2,
    'db': 2,
    'sg': 2,
    'bh': 2,
    'hs': 2,
    'mt': 2,
    'ds': 2,
    'rg': 2,
    'cn': 2,
    'nh': 2,
    'fl': 2,
    'mc': 2,
    'lv': 2,
    'ts': 2,
    'og': 2
}

# =========================== ******* ===========================

str= "Neon"

class Node:

    def __init__(self, element, word):

        self.left = None #arvore da esquerda
        self.right = None #arvore da direita
        self.element = element #elemento quimico
        self.remainderWord = word #parte da string que falta adicionar a arvore a partir deste nodo

    def create(self, element,remainderWord):
# Função de create
            if self.left is None:
                self.left = Node(element, remainderWord)
                if remainderWord:
                    self.left.create(remainderWord[0],remainderWord[1:])
                else:
                    return
            if self.right is None:
                if remainderWord :
                    self.right = Node(element + remainderWord[0], remainderWord[1:])
                    if remainderWord[1:]:
                        self.right.create(remainderWord[1], remainderWord[2:])
                    else: 
                        return
                else :
                    return
            else:
                return

# Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.element),
        if self.right:
            self.right.PrintTree()

# Tree search
    def SearchTree(self, elements, aux1):
        if self is None:
            return None
        if self.left:
            self.left.SearchTreeAux(elements, aux1)
        print("estou no search")
        print(self.element)
        if self.right:
            self.right.SearchTreeAux(elements, aux1)

    def SearchTreeAux(self, elements, aux1):
        print(self.element)
        if tp.get(self.element) is not None:
            aux1.append(self.element)
            if self.left is not None:
                print("left")
                self.left.SearchTreeAux(elements, aux1)
            if self.right is not None:
                print("right")
                self.right.SearchTreeAux(elements, aux1)
        else: aux1 = []
        if self.left is None and self.right is None:
            for e in aux1:
                elements.append(e)
            aux1 = []
            return elements


#root = Node("root", str) # não me interessa o elemento da raiz chamei-lhe root
#root.create(str[0],str[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root

#print("ARVORE")
#root.PrintTree()