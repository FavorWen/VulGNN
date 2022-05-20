import jsonParse
import sys
import os

# nodeId, nodeOP, nodeLabel
# srcId, dstId, type, weight

def toGraph(g:jsonParse.Graph, bug_type, path):
    node = g.entry
    edgeFile = open(path+".edg", "w")
    verFile = open(path+".ver", "w")
    typeFile = open(path+".type", "w")
    typeFile.write(bug_type)
    while node != None:
        verFmt = f'{node.id}, {node.op}, {node.label}\n'
        verFile.write(verFmt)
        if node.eLink != None:
            edgeFmt = f'{node.id}, {node.eLink.dst.id}, {node.eLink.type}, {node.eLink.weight}\n'
            edgeFile.write(edgeFmt)
        for link in node.dLink:
            edgeFmt = f'{node.id}, {link.dst.id}, {link.type}, {link.weight}\n'
            edgeFile.write(edgeFmt)
        node = node.next()
    edgeFile.close()
    verFile.close()
    typeFile.close()

BUG_ENCODE = ["rein", "timestamp"]

"""
Args:
    toGraph.py  raw_dir bug1_dir bug2_dir    
"""
def main():
    if len(sys.argv) < 3:
        print("must give at least one save dir and one bug dir")
        return
    raw_dir = sys.argv[1]
    for dir in sys.argv[2:]:
        bug_type = os.path.basename(dir)
        bug_type = str(BUG_ENCODE.index(bug_type))
        files = os.listdir(dir)
        for file in files:
            idx = file.strip('0').replace(".json", "")
            if idx == '':
                idx = '0'
            g = jsonParse.parseJson(os.path.join(dir, file))
            toGraph(g, bug_type, os.path.join(raw_dir, idx))

    # g = jsonParse.parseJson(sys.argv[1])
    # toGraph(g, "out")

if __name__ == '__main__':
    main()
