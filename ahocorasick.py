class Node:
    def __init__(self):
        self.goto={}
        self.out=[]
        self.fail=None
def create_tree(patterns):
    root = Node()
    for pattern in patterns:
        node=root
        for symbol in pattern:
            node=node.goto.setdefault(symbol,Node())
        node.out.append(pattern)
    return root

def create_keyword_tree(patterns):
    root=create_tree(patterns)
    queue=[]
    for node in root.goto.itervalues():
        queue.append(node)
        node.fail = root
    while len(queue) > 0:
        rnode=queue.pop(0)
        for key,unode in rnode.goto.iteritems():
            queue.append(unode)
            fnode=rnode.fail
            while fnode !=None and not fnode.goto.has_key(key):
                fnode=fnode.fail
            unode.fail=fnode.goto[key] if fnode else root
            unode.out+=unode.fail.out
    return root

def find(s,root):
    node=root
    for i in xrange(len(s)):
        while node != None and not node.goto.has_key(s[i]):
            node=node.fail
        if node == None:
            node=root
            continue
        node=node.goto[s[i]]
        for pattern in node.out:
            print "At position %s keyword %s found." %((i-len(pattern)+1),pattern)
if __name__ == '__main__':
    patterns=[]
    with open('abc.txt') as f:
        for lines in f:
            line=lines[:-1]
            patterns.append(line)

    root=create_keyword_tree(patterns)
    s=raw_input("Enter the string : ")
    find(s,root)
