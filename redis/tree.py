import redis
import datetime
from ast import literal_eval
from collections import deque
r=redis.Redis(host='localhost',port=6379,db=1)

class AhoCorasickTreeBuilder:

    
    def __init__(self,n,a):
        self._n     = n
        self._a     = a
        self._root_node_id  = self.getNewNodeID()


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
        for char in range(len(kwd)):
            currChar=kwd[char].lower()
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
                pl=r.hget(current_node_id,'t')
                dt=literal_eval(pl)
                dt[kwd[char]]=new_node_id
                r.hset(current_node_id,'t',dt)
                current_node_id=new_node_id

                
    def _buildTree(self):
        curr_node_id=self._root_node_id
        nodes_to_explore = deque()
        for level1_node in literal_eval(r.hget(curr_node_id,'t')).values():
            nodes_to_explore.extendleft(literal_eval(r.hget(level1_node,'t')).values())
        while len(nodes_to_explore) > 0:
            current_node_id = nodes_to_explore.pop()
            nodes_to_explore.extendleft(literal_eval(r.hget(current_node_id,'t')).values())
            parent_failure_node = r.hget(r.hget(current_node_id,'p'),'f')
            curr_char = r.hget(current_node_id,'c')
            while parent_failure_node != self._root_node_id and literal_eval(r.hget(parent_failure_node,'t')).get(curr_char, None) == None:
                parent_failure_node = r.hget(parent_failure_node,'f')
            if literal_eval(r.hget(parent_failure_node,'t')).get(curr_char, None) != None:
                final_failure_node_id = literal_eval(r.hget(parent_failure_node,'t'))[curr_char]
                r.hset(current_node_id,'f', final_failure_node_id)
                l1=literal_eval(r.hget(final_failure_node_id,'o'))
                l2=literal_eval(r.hget(current_node_id,'o'))
                for outputLen in l1:
                    l2.append(outputLen)
                    r.hset(current_node_id,'o',l2)
            else:
                r.hset(current_node_id,'f',self._root_node_id)
            #print current_node_id,"--and--",r.hmget(current_node_id,'p','c','f','o','t','de')


    def search(self,txt):
        curr_node=self._root_node_id
        for i in range(len(txt)):
            curr_char = txt[i].lower()
            while curr_node != self._root_node_id and not literal_eval(r.hget(curr_node,'t')).has_key(curr_char):
                curr_node = r.hget(curr_node,'f')
            if literal_eval(r.hget(curr_node,'t')).has_key(curr_char):
                curr_node=literal_eval(r.hget(curr_node,'t'))[curr_char]
            else:
                curr_node=self._root_node_id
            for word in literal_eval(r.hget(curr_node,'o')):
                p=(i-word+1)
                print "The pattern '%s' found from position %s to position %s" %(txt[p:p+word],p,p+word-1)
