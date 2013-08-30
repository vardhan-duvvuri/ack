class Node:
    def __init__(self):
        self.goto={}
        self.out=None
        self.fail=None
        self.output=None
def create_tree(patterns):
    root = Node()
    for pattern in patterns:
        node=root
        for symbol in pattern:
            node=node.goto.setdefault(symbol,Node())
        node.out=pattern
    return root

def create_keyword_tree(patterns):
    root=create_tree(patterns)
    queue=[]
    for node in root.goto.itervalues():
        queue.append(node)
        node.fail = root
    while len(queue) > 0:
        parentnode=queue.pop(0)
        for key,unode in parentnode.goto.iteritems():
            queue.append(unode)
            failnode=parentnode.fail
            while failnode != None and not failnode.goto.has_key(key):
                failnode=failnode.fail
            if failnode != None:
                unode.fail = failnode.goto[key]
            else:
                unode.fail = root
            if unode.fail.out!=None:
                unode.output=unode.fail
    return root

def search(s,root):
    node=root
    for i in range(len(s)):
        while node != None and not node.goto.has_key(s[i]):
            node=node.fail
        if node == None:
            node=root
            continue
        node=node.goto[s[i]]
        temp=node
        while node != None:
            if node.out:
                p=(i-len(node.out)+1)
                print "The pattern '%s' found from position %s to position %s" %(node.out,p,p+len(node.out)-1)
            node=node.output
        node=temp

if __name__ == '__main__':
    patterns=[]
    with open('abc.txt') as f:
        for lines in f:
            line=lines[:-1]
            patterns.append(line)

    root=create_keyword_tree(patterns)
    input=raw_input("Enter the string : ")
    search(input,root)
