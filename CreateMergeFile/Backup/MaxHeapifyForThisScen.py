def MaxHeapify(self, Files=[], i=0):
    while True:
        left = i<<1
        right = (i<<1)+1
        largest =i
        if (left <= self.heapSize) & (Files[self.pos][2][left])>(Files[self.pos][2][i]):
            largest = left

        if (right <= self.heapSize) & (Files[self.pos][2][left])>(Files[self.pos][2][largest]):
            largest = right
        if (i == largest):
            return;
        self.Exchange(Files, i, largest)
    return;

def BuildMaxHeap(self, Files=[]):
    self.heapsize = len(Files[self.pos][2])
    for i in reversed(range(self.heapSize//2)):
        self.MaxHeapify(Files, i)
    return;
    