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
        pnode=queue.pop(0)
        for key,unode in pnode.goto.iteritems():
            queue.append(unode)
            failnode=pnode.fail
            while failnode != None and not failnode.goto.has_key(key):
                failnode=failnode.fail
            if failnode != None:
                unode.fail = failnode.goto[key]
            else:
                unode.fail = root
    return root

def find(s,root):
    node=root
    for i in range(len(s)):
        while node != None and not node.goto.has_key(s[i]):
            node=node.fail
        if node == None:
            node=root
            continue
        node=node.goto[s[i]]
        for pattern in node.out:
            p=(i-len(pattern)+1)
            print "The pattern '%s' found from position %s to position %s" %(pattern,p,p+len(pattern)-1)
        for pattern in node.fail.out:
            p=(i-len(pattern)+1)
            print "The pattern '%s' found from position %s to position %s" %(pattern,p,p+len(pattern)-1)
    
if __name__ == '__main__':
    patterns=['at','cat','bat','hit','man']
    '''with open('abc.txt') as f:
        for lines in f:
            line=lines[:-1]
            patterns.append(line)'''

    root=create_keyword_tree(patterns)
    input=raw_input("Enter the string : ")
    find(input,root)
