# FP-Growth Algorithm for Mining Frequent Patterns

# 1. FP-Tree Node Structure
class treeNode(object):
    # 1.1 Initialization
    def __init__(self, nameValue, numOccur, parentNode):
        # 1.1.1 Node name
        self.name = nameValue
        # 1.1.2 Occurrence count
        self.count = numOccur
        # 1.1.3 Pointer to parent node
        self.parent = parentNode
        # 1.1.4 Node link for same item nodes
        self.nodeLink = None
        # 1.1.5 Children nodes
        self.children = {}

    # 1.2 Increment count
    def inc(self, numOccur):
        self.count += numOccur

    # 1.3 Display tree
    def disp(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# 2. Build FP-Tree
def createTree(dataSet, minSup=1):
    # 2.1 First pass: count frequency of items
    originHeaderTable = {}
    for trans in dataSet:
        for item in trans:
            originHeaderTable[item] = originHeaderTable.get(item, 0) + dataSet[trans]

    # 2.2 Remove items below min support
    popKeys = []
    for k in originHeaderTable.keys():
        if originHeaderTable[k] < minSup:
            popKeys.append(k)

    for k in popKeys:
        del originHeaderTable[k]

    # 2.3 If no items meet minSup, return None
    freqItemSet = set(originHeaderTable.keys())
    if len(freqItemSet) == 0:
        return None, None

    # 2.4 Initialize header table
    headerTable = {}
    for k in freqItemSet:
        headerTable[k] = [originHeaderTable[k], None]

    del originHeaderTable

    # 2.5 Create the root node
    root_node = treeNode('Null Set', 1, None)

    # 2.6 Second pass: populate FP-Tree
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            # Sort items by frequency descending
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, root_node, headerTable, count)

    return root_node, headerTable

# 3. Insert transaction into FP-Tree
def updateTree(items, parentNode, headerTable, count):
    # 3.1 If the first item already exists under the parent node
    if items[0] in parentNode.children:
        parentNode.children[items[0]].inc(count)
    else:
        # 3.1.2 Otherwise create a new node
        parentNode.children[items[0]] = treeNode(items[0], count, parentNode)

        # 3.1.3 Update header table node link
        updateHeader(headerTable[items[0]][1], parentNode.children[items[0]])

    # 3.2 Insert the rest recursively
    if len(items) > 1:
        updateTree(items[1:], parentNode.children[items[0]], headerTable, count)

# 4. Update header table node links
def updateHeader(lastNode, newLeafNode):
    if lastNode is None:
        return
    while lastNode.nodeLink is not None:
        lastNode = lastNode.nodeLink
    lastNode.nodeLink = newLeafNode

# 5. Load sample test dataset
def loadTestDataSet():
    dataset = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return dataset

# 6. Create initial dataset in dictionary form
def createInitDataSet(dataSet):
    dictDataSet = {}
    for trans in dataSet:
        dictDataSet[frozenset(trans)] = 1
    return dictDataSet

# 7. Build prefix path from a leaf node upwards
def buildCombinedItems(leafNode, combinedItems):
    if leafNode.parent is not None:
        combinedItems.append(leafNode.name)
        buildCombinedItems(leafNode.parent, combinedItems)

# 8. Build conditional pattern base (prefix paths)
def buildCombinedDataSet(nodeObject):
    combinedDataSet = {}
    while nodeObject is not None:
        combinedItems = []
        buildCombinedItems(nodeObject, combinedItems)
        if len(combinedItems) > 1:
            combinedDataSet[frozenset(combinedItems[1:])] = nodeObject.count
        nodeObject = nodeObject.nodeLink
    return combinedDataSet

# 9. Mine frequent patterns from FP-Tree
def scanFPTree(headerTable, minSup, parentNodeNames, freqItemList):
    # Sort header table by frequency ascending (not required but common practice)
    for baseNode, nodeInfo in headerTable.items():
        newFreqSet = parentNodeNames.copy()
        newFreqSet.add(baseNode)
        nodeCount = nodeInfo[0]
        nodeObject = nodeInfo[1]

        # Save the frequent item and its count
        freqItemList.append((newFreqSet, nodeCount))

        # Build conditional pattern base
        combinedDataSet = buildCombinedDataSet(nodeObject)

        # Build conditional FP-tree
        subFPTree, subHeaderTable = createTree(combinedDataSet, minSup)

        # Recursively mine the conditional FP-tree
        if subHeaderTable is not None:
            print("conditional tree for:", newFreqSet)
            subFPTree.disp(1)
            scanFPTree(subHeaderTable, minSup, newFreqSet, freqItemList)

# 10. Main function
if __name__ == '__main__':
    # 10.1 Load test dataset
    simpData = loadTestDataSet()

    # 10.2 Convert dataset into dictionary form
    initSet = createInitDataSet(simpData)

    # 10.3 Create initial FP-Tree
    initFPTree, initHeaderTable = createTree(initSet, 3)

    # 10.4 Display the FP-Tree
    initFPTree.disp(1)

    # 10.5 Mine frequent patterns
    freqItems = []
    root_node_names = set([])

    # 10.6 Start mining
    scanFPTree(initHeaderTable, 3, root_node_names, freqItems)

    # 10.7 Output the frequent patterns
    from pprint import pprint
    pprint(freqItems)
