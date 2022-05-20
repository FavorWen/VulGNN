

class Link:
    def __init__(self, type=None, dst=None, weight=1) -> None:
        self.type = type
        self.dst = dst
        self.weight = weight

class Node:
    def __init__(self, op="null", eLink:Link=None, dLink=None, label=None):
        self.op = op
        self.eLink = eLink
        self.id = 0
        if dLink == None:
            self.dLink = []
        else:
            self.dLink = dLink
        if label == None:
            self.label = []
        else:
            self.label = label
    def addlabel(self, label):
        if type(label) == type([]):
            for l in label:
                if l not in self.label and l != None:
                    self.label.append(l)
        else:
            if label not in self.label and label != None:
                self.label.append(label)
    def setlabel(self, label:list):
        self.label = label
    def addLink(self, links):
        if type(links) == type([]):
            for link in links:
                if link.type == 'exec':
                    error("addLink error")
                else:
                    self.dLink.append(link)
        else:
            link = links
            if link.type == 'exec':
                    self.eLink = link
            else:
                self.dLink.append(link)
    def next(self):
        if self.eLink == None:
            return None
        else:
            return self.eLink.dst

class Graph:
    def __init__(self, entry:Node=None) -> None:
        self.entry = entry
        self.latest = entry
        self.id = 0
    def setEntry(self, entry):
        self.entry = entry
        self.latest = entry
    def getEntry(self):
        return self.entry
    def getLatest(self):
        return self.latest
    def add(self, node:Node):
        if node == None:
            return
        node.id = self.id
        self.id += 1
        if self.entry == None:
            self.entry = node
            self.latest = node
            return
        l = Link("exec", dst=node, weight=1)
        self.latest.addLink(l)
        self.latest = node
        pass

class stackValue:
    def __init__(self, producer=None, label=None) -> None:
        self.producer:Node = producer
        if label == None:
            self.label = []
        else:
            self.label = label
    def addlabel(self, label):
        if type(label) == type([]):
            for l in label:
                if l not in self.label and l != None:
                    self.label.append(l)
        else:
            if label not in self.label and label != None:
                self.label.append(label)
    def setlabel(self, label:list=[]):
        self.label = label

class evmStack:
    def __init__(self, data=None):
        if data == None:
            self.data = []
        else:
            self.data = data
    def len(self):
        return len(self.data)
    def pop(self, N=1):
        if self.len() < N:
            error(f"pop: N({N}) > stack length({self.len()})")
        if N == 0:
            return []
        else:
            r = self.data[:N]
            self.data = self.data[N:]
            return r
    def push(self, elem) -> None:
        if elem == None:
            return
        self.data = [elem] + self.data
    
    def loc(self, idx) -> stackValue:
        if idx < 0 or idx > self.len()-1:
            error(f"loc: idx({idx}) out of range! stack length({self.len()})")
        return self.data[idx]

    def swap(self, idx1, idx2) -> None:
        if idx1 < 0 or idx1 > self.len()-1 or idx2 < 0 or idx2 > self.len()-1:
            error(f"swap: idx({idx1, idx2}) out of range! stack length({self.len()})")
        self.data[idx1], self.data[idx2] = self.data[idx2], self.data[idx1]