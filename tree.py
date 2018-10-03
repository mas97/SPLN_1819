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

root = Node("root", str) # não me interessa o elemento da raiz chamei-lhe root
root.create(str[0],str[1:]) # chama a função create que vai construir recursivamente a arvore a partir do nodo raiz root

print("ARVORE")
root.PrintTree()