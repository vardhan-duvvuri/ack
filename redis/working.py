from tree import AhoCorasickTreeBuilder
if __name__ == '__main__':
    ack = AhoCorasickTreeBuilder('Node','p1')
    ack._addKeyword('gel')
    ack._addKeyword('age')
    ack._addKeyword('cage')
    ack._buildTree()
    ack.search('the gel is in cage')
