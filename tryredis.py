import redis
import datetime
from ast import literal_eval
from collections import deque
r=redis.Redis(host='localhost',port=6379,db=0)

class AhoCorasickTreeBuilder:

    
    def __init__(self,n,a):
        self._n     = n
        self._a     = a
        self._root_node_id  = self.getNewNodeID()
        print self._root_node_id
        r.hset('pubs',a,self._root_node_id)


    def getNewNodeID(self):
            d = datetime.datetime.today()
            return '%s:%s:%d' %(self._n, self._a,d.microsecond)
                                        

    def getRootNode(self):
        return self._root_node_id
    

    def _addKeyword(self,kwd):
        if kwd == None or len(kwd) == 0:
            return
        current_node_id = self._root_node_id
        if r.hget(current_node_id,'f') == None:
            p=None
            c='.'
            f=self._root_node_id
            o=list()
            t=dict()
            de=0
            r.hmset(current_node_id,{'p':p,'c':c,'f':f,'o':o,'t':t,'de':de})
            print current_node_id,"and",r.hmget(current_node_id,'p','c','f','o','t','de')
        for char in range(len(kwd)):
            currChar=kwd[char].lower()
            print currChar
            if literal_eval(r.hget(current_node_id,'t')).get(currChar, None) != None:
                current_node_id = literal_eval(r.hget(current_node_id,'t'))[currChar]
            else:
                new_node_id = self.getNewNodeID()
                p=current_node_id
                c=currChar
                f=self._root_node_id
                o=list()
                t=dict()
                de=int(r.hget(current_node_id,'de'))+1
                if char == len(kwd)-1:
                    o.append(de)
                r.hmset(new_node_id,{'p':p,'c':c,'f':f,'o':o,'t':t,'de':de})
                print new_node_id,"and",r.hmget(new_node_id,'p','c','f','o','t','de')
                pl=r.hget(current_node_id,'t')
                dt=literal_eval(pl)
                dt[kwd[char]]=new_node_id
                r.hset(current_node_id,'t',dt)
                print current_node_id,"and",r.hmget(current_node_id,'p','c','f','o','t','de')
                current_node_id=new_node_id

                
    def _buildTree(self):
        curr_node_id=self.getRootNode()
        nodes_to_explore = deque()
        for level1_node in literal_eval(r.hget(curr_node_id,'t')).values():
            print level1_node
            nodes_to_explore.extendleft(literal_eval(r.hget(level1_node,'t')).values())
        print nodes_to_explore
        while len(nodes_to_explore) > 0:
            current_node_id = nodes_to_explore.pop()
            print current_node_id
            print literal_eval(r.hget(current_node_id,'t')).values()
            nodes_to_explore.extendleft(literal_eval(r.hget(current_node_id,'t')).values())
            parent_failure_node = r.hget(r.hget(current_node_id,'p'),'f')
            print parent_failure_node
            curr_char = r.hget(current_node_id,'c')
            print curr_char
            while parent_failure_node != self._root_node_id and literal_eval(r.hget(parent_failure_node,'t')).get(curr_char, None) == None:
                parent_failure_node = r.hget(parent_failure_node,'f')
            print literal_eval(r.hget(parent_failure_node,'t'))
            if literal_eval(r.hget(parent_failure_node,'t')).get(curr_char, None) != None:
                final_failure_node_id = literal_eval(r.hget(parent_failure_node,'t'))[curr_char]
                print final_failure_node_id
                r.hset(current_node_id,'f', final_failure_node_id)
                l1=literal_eval(r.hget(final_failure_node_id,'o'))
                l2=literal_eval(r.hget(current_node_id,'o'))
                for outputLen in l1:
                    l2.append(outputLen)
                    r.hset(current_node_id,'o',l2)
            else:
                r.hset(current_node_id,'f',self._root_node_id)
            print current_node_id,"--and--",r.hmget(current_node_id,'p','c','f','o','t','de')
        r.bgsave()


def search(txt,root):
    curr_node=root
    for i in range(len(txt)):
        curr_char = txt[i].lower()
        while curr_node != root and not literal_eval(r.hget(curr_node,'t')).has_key(curr_char):
            curr_node = r.hget(curr_node,'f')
        if literal_eval(r.hget(curr_node,'t')).has_key(curr_char):
            curr_node=literal_eval(r.hget(curr_node,'t'))[curr_char]
        else:
            curr_node=root
        for word in literal_eval(r.hget(curr_node,'o')):
            p=(i-word+1)
            print "The pattern '%s' found from position %s to position %s" %(txt[p:p+word],p,p+word-1)
                
            

if __name__ == '__main__':
    #ack = AhoCorasickTreeBuilder('N','a2')
    #ack._addKeyword('age')
    #ack._addKeyword('ago')
    #ack._addKeyword('cage')
    #ack._buildTree()
    #root=ack.getRootNode()
    pub=raw_input("Enter Publisher : ")
    root=r.hget('pubs',pub)
    text=raw_input("Enter text : ")
    search(text,root)
