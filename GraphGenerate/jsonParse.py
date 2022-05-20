import json
import sys
import copy
from xml.dom import NotFoundErr
from defs import *

OP2LABEL={
    "ADDRESS":"addr_contract",
    "ORIGIN":"caller",
    "CALLER":"caller",
    "CALLVALUE":"msgvalue",
    "BALANCE":"balance",
    "SELFBALANCE":"balance",
    "CALLDATALOAD":"call_data",
    "CALLDATACOPY":"call_data",
    "BLOCKHASH":"blk",
    "TIMESTAMP":"blk",
    "NUMBER":"blk",
    "DIFFICULTY":"blk",
    "BASEFEE":"blk",
    "MLOAD":"mdata",
    "SLOAD":"sdata",
    "CREATE":"create",
    "CALL":"call",
    "CALLCODE":"callcode",
    "DELEGATECALL":"delegatecall",
    "CREATE2":"create2",
    "STATICCALL":"staticcall",
    "ADD":"cal_res",
    "MUL":"cal_res",
    "SUB":"cal_res",
    "EXP":"cal_res",
    "LT":"comp_res",
    "GT":"comp_res",
    "SLT":"comp_res",
    "SGT":"comp_res",
    "EQ":"comp_res",
    "ISZERO":"comp_res",
    "AND":"bit_res",
    "OR":"bit_res",
    "XOR":"bit_res",
    "NOT":"bit_res",
    "SHL":"bit_res",
    "CALLDATASIZE":"size",
    "CODESIZE":"size",
    "EXTCODESIZE":"size",
    "RETURNDATASIZE":"size",
    "MSIZE":"size",
    "CODECOPY":"code",
    "EXTCODECOPY":"code",
    "EXTCODEHASH":"code",
    "GASPRICE":"gas",
    "GASLIMIT":"gas",
    "RETURNDATACOPY":"return",
    "RETURN":"return",
    "COINBASE":"coinbase",
    "GAS":"gasremain",
    "REVERT":"revert",
    "SELFDESTRUCT":"selfdestruct",
    "MSTORE":"memory",
    "MSTORE8":"memory",
    "SSTORE":"storage",
    "JUMP":"flowcontrol",
    "JUMPI":"flowcontrol",
    "JUMPDEST":"flowcontrol",
    "STOP":"flowcontrol",

    "DIV":None,
    "SDIV":None,
    "MOD":None,
    "SMOD":None,
    "ADDMOD":None,
    "SIGNEXTEND":None,
    "BYTE":None,
    "SHR":None,
    "SAR":None,
    "SHA3":None,
    "CHAINID":None,
    "POP":None,
    "PC":None,
    "PUSH1":None,"PUSH2":None,"PUSH3":None,"PUSH4":None,"PUSH5":None,"PUSH6":None,"PUSH7":None,"PUSH8":None,"PUSH9":None,"PUSH10":None,"PUSH11":None,"PUSH12":None,"PUSH13":None,"PUSH14":None,"PUSH15":None,"PUSH16":None,
    "PUSH17":None,"PUSH18":None,"PUSH19":None,"PUSH20":None,"PUSH21":None,"PUSH22":None,"PUSH23":None,"PUSH24":None,"PUSH25":None,"PUSH26":None,"PUSH27":None,"PUSH28":None,"PUSH29":None,"PUSH30":None,"PUSH31":None,"PUSH32":None,
    "DUP1":None,"DUP2":None,"DUP3":None,"DUP4":None,"DUP5":None,"DUP6":None,"DUP7":None,"DUP8":None,
    "DUP9":None,"DUP10":None,"DUP11":None,"DUP12":None,"DUP13":None,"DUP14":None,"DUP15":None,"DUP16":None,
    "SWAP1":None,"SWAP2":None,"SWAP3":None,"SWAP4":None,"SWAP5":None,"SWAP6":None,"SWAP7":None,"SWAP8":None,
    "SWAP9":None,"SWAP10":None,"SWAP11":None,"SWAP12":None,"SWAP13":None,"SWAP14":None,"SWAP15":None,"SWAP16":None,
    "LOGO":None,
    "LOG1":None,"LOG2":None,"LOG3":None,"LOG4":None,
    "PUSH":None,
    "DUP":None,
    "SWAP":None,
}

OP_7_to_1 = [
    "CALL", "CALLCODE"
]

OP_6_to_1 = [
    "DELEGATECALL", "STATICCALL"
]

OP_4_to_1 = [
    "CREATE2"
]

OP_3_to_1 = [
    "ADDMOD",   "MULMOD",   "CREATE"
]

OP_2_to_1 = [
    "ADD",  "MUL",  "SUB",  "DIV",  "SDIV", "MOD",
    "SMOD", "EXP",  "SIGNEXTEND",   "LT",   "GT",
    "SLT",  "SGT",  "EQ",   "AND",  "OR",   "XOR",
    "BYTE", "SHL",  "SHR",  "SAR",  "SHA3", 
]

OP_1_to_1 = [
    "ISZERO",   "NOT",  "BALANCE",  "CALLDATALOAD",
    "EXTCODESIZE",  "EXTCODEHASH",  "BLOCKHASH",
    "MLOAD",   "SLOAD" ,    ""
]

OP_0_to_1 = [
    "ADDRESS",  "ORIGIN",   "CALLER",   "CALLVALUE",
    "CALLDATASIZE", "CODESIZE", "GASPRICE", "RETURNDATASIZE",
    "COINBASE", "TIMESTAMP",    "NUMBER",   "DIFFICULTY",
    "GASLIMIT", "CHAINID",  "SELFBALANCE",  "BASEFEE",
    "PC",   "MSIZE",    "GAS",
    "PUSH1", "PUSH2", "PUSH3", "PUSH4",
    "PUSH5", "PUSH6", "PUSH7", "PUSH8",
    "PUSH9", "PUSH10", "PUSH11", "PUSH12",
    "PUSH13", "PUSH14", "PUSH15", "PUSH16",
    "PUSH17", "PUSH18", "PUSH19", "PUSH20",
    "PUSH21", "PUSH22", "PUSH23", "PUSH24",
    "PUSH25", "PUSH26", "PUSH27", "PUSH28",
    "PUSH29", "PUSH30", "PUSH31", "PUSH32",
]

OP_0_to_0 = [
    "JUMPDEST", "STOP"
]

OP_1_to_0 = [
    "POP",  "JUMP", "SELFDESTRUCT"
]

OP_2_to_0 = [
    "MSTORE",   "MSTORE8",  "SSTORE",   "JUMPI",
    "RETURN",   "REVERT"
]

OP_3_to_0 = [
    "CALLDATACOPY", "CODECOPY", "RETURNDATACOPY",   
]

OP_4_to_0 = [
    "EXTCODECOPY",  
]

OP_X_DUP = {
    'DUP1': 1, 'DUP2': 2, 'DUP3': 3, 'DUP4': 4, 
    'DUP5': 5, 'DUP6': 6, 'DUP7': 7, 'DUP8': 8, 
    'DUP9': 9, 'DUP10': 10, 'DUP11': 11, 'DUP12': 12, 
    'DUP13': 13, 'DUP14': 14, 'DUP15': 15
}

OP_X_SWAP = {
    'SWAP1': 1, 'SWAP2': 2, 'SWAP3': 3, 'SWAP4': 4, 
    'SWAP5': 5, 'SWAP6': 6, 'SWAP7': 7, 'SWAP8': 8, 
    'SWAP9': 9, 'SWAP10': 10, 'SWAP11': 11, 'SWAP12': 12, 
    'SWAP13': 13, 'SWAP14': 14, 'SWAP15': 15
}

OP_X_LOG = {
    'LOG0': 2,  'LOG1': 3, 'LOG2': 4, 'LOG3': 5, 'LOG4': 6, 
}

def op_3_to_1(node:Node, stack:evmStack):
    v1, v2, v3 = stack.pop(3)
    new_v = stackValue(node)
    new_v.addlabel([OP2LABEL[node.op]])
    stack.push(new_v)

    node.addlabel(v1.label)
    node.addlabel(v2.label)
    node.addlabel(v3.label)

    link1 = Link('data', v1.producer)
    link2 = Link('data', v2.producer)
    link3 = Link('data', v3.producer)
    node.addLink([link1, link2, link3])

def op_2_to_1(node:Node, stack:evmStack):
    v1, v2 = stack.pop(2)
    new_v = stackValue(node)
    # new_v.addlabel(v1.label)
    # new_v.addlabel(v2.label)
    new_v.addlabel([OP2LABEL[node.op]])
    stack.push(new_v)

    node.addlabel(v1.label)
    node.addlabel(v2.label)
    
    link1 = Link('data', v1.producer)
    link2 = Link('data', v2.producer)
    node.addLink([link1, link2])

def op_1_to_1(node:Node, stack:evmStack):
    v1 = stack.pop()
    new_v = stackValue(node)
    new_v.addlabel([OP2LABEL[node.op]])
    stack.push(new_v)

    node.addlabel(v1.label)
    
    link1 = Link('data', v1.producer)
    node.addLink([link1])

def op_0_to_0(node:Node, stack:evmStack):
    pass

def op_0_to_1(node:Node, stack:evmStack):
    new_v = stackValue(node)
    new_v.addlabel([OP2LABEL[node.op]])
    stack.push(new_v)

def op_1_to_0(node:Node, stack:evmStack):
    stack.pop(1)

def op_2_to_0(node:Node, stack:evmStack):
    stack.pop(2)

def op_3_to_0(node:Node, stack:evmStack):
    stack.pop(3)

def op_4_to_0(node:Node, stack:evmStack):
    stack.pop(4)

def op_5_to_0(node:Node, stack:evmStack):
    stack.pop(5)

def op_6_to_0(node:Node, stack:evmStack):
    stack.pop(6)

def op_x_to_0(node:Node, stack:evmStack, X:int):
    stack.pop(X)
    node.addlabel([OP2LABEL[node.op]])

def op_x_to_1(node:Node, stack:evmStack, X:int):

    values = stack.pop(X)
    new_v = stackValue(node)

    for v in values:
        new_v.addlabel(v.label)
        node.addlabel(v.label)
        link = Link('data', node)
        v.producer.addLink(link)
        # link = Link('data', v.producer)
        # node.addLink(link)
    node.addlabel([OP2LABEL[node.op]])
    new_v.addlabel([OP2LABEL[node.op]])
    stack.push(new_v)

def op_x_dup(node:Node, stack:evmStack, X:int):
    v = stack.loc(X-1)
    new_v = stackValue(node, label=v.label)
    node.addlabel(v.label)

    link = Link('data', node)
    v.producer.addLink(link)
    # link = Link('data', v.producer)
    # node.addLink(link)
    stack.push(new_v)

def op_x_swap(node:Node, stack:evmStack, X:int):
    stack.swap(0, X)

def produceNode(e:dict, stack:evmStack) -> Node:
    if e['op'] not in OP2LABEL:
        error(f"can't find label({e['op']})")
    node = Node(e['op'])
    if e['op'] in OP_7_to_1:
        op_x_to_1(node, stack, 7)
    elif e['op'] in OP_6_to_1:
        op_x_to_1(node, stack, 6)
    elif e['op'] in OP_4_to_1:
        op_x_to_1(node, stack, 4)
    elif e['op'] in OP_3_to_1:
        op_x_to_1(node, stack, 3)
    elif e['op'] in OP_2_to_1:
        op_x_to_1(node, stack, 2)
    elif e['op'] in OP_1_to_1:
        op_x_to_1(node, stack, 1)
    elif e['op'] in OP_0_to_1:
        op_x_to_1(node, stack, 0)
    elif e['op'] in OP_0_to_0:
        op_x_to_0(node, stack, 0)
    elif e['op'] in OP_1_to_0:
        op_x_to_0(node, stack, 1)
    elif e['op'] in OP_2_to_0:
        op_x_to_0(node, stack, 2)
    elif e['op'] in OP_3_to_0:
        op_x_to_0(node, stack, 3)
    elif e['op'] in OP_4_to_0:
        op_x_to_0(node, stack, 4)
    elif e['op'] in OP_X_DUP:
        op_x_dup(node, stack, OP_X_DUP[e['op']])
    elif e['op'] in OP_X_SWAP:
        op_x_swap(node, stack, OP_X_SWAP[e['op']])
    elif e['op'] in OP_X_LOG:
        op_x_to_0(node, stack, OP_X_LOG[e['op']])
    else:
        error(f"producerNode: can't find handler({e['op']})")
    return node

def goThrough(g:Graph):
    node = g.entry
    while node != None:
        print(node.op, node.label)
        node = node.next()

def parseJson(file) -> Graph:
    g = Graph()
    stack = evmStack()
    with open(file, 'r') as f:
        js = json.load(f)
    for e in js:
        node = produceNode(e, stack)
        g.add(node)
    return g

def main():
    g = parseJson(sys.argv[1])
    #g = parseJson("00008.json")
    goThrough(g)

if __name__ == '__main__':
    main()
