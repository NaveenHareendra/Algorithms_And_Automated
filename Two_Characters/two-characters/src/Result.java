class Result {
    int sizeOfHashArray = 29;
    private int[] arr = new int[sizeOfHashArray] ;
    private Tree root;
    tempNode tempNodeRoot;


    static  class Tree{
        int key;
        int value;

        private Tree leftChild;
        private Tree rightChild;
        private Tree parent;

        IndexValNode indexNodeRoot;

        Tree(int key,int value,IndexValNode idxNode){
            this.key=key;
            this.value=value;
            this.indexNodeRoot =idxNode;
        }
    }

    static class tempNode{
        private int key;
        private tempNode next;
        private int charASCII;
        IndexValNode indexNodeRoot;
        //        private tempNode node;
        tempNode(int  element, int charVal, IndexValNode indexNodeRoot){
            key=element;
            charASCII =charVal;
            this.indexNodeRoot=indexNodeRoot;
        }
    }

    static class IndexValNode{
        private int key;
        private IndexValNode next;

        IndexValNode(int key){
            this.key=key;
        }
    }

    public IndexValNode InsertIndexInfo(int key, IndexValNode idxNode){

        if(idxNode==null){
            idxNode= new IndexValNode(key);
            return idxNode;

        }else{
//            System.out.println("INNER "+key);
            IndexValNode node = new IndexValNode(key);
//            IndexValNode oldNode = idxNode;
            node.next = idxNode;
            idxNode=node;
            return idxNode;
        }


    }

    public void TreeInsert(int key, int value,IndexValNode idxNode){
        Tree tree = new Tree(key, value,idxNode);
        Tree y = null;
        Tree x = root;

        while(x!=null){
            y=x;
            if(tree.key<x.key){
                x=x.leftChild;
            }else{
                x=x.rightChild;
            }
        }

        tree.parent = y;

        if(y==null){
            root=tree;
        }else if(tree.key<y.key){
            y.leftChild=tree;
        }else{
            y.rightChild=tree;
        }

    }
    /*
     * Complete the 'alternate' function below.
     *
     * The function is expected to return an INTEGER.
     * The function accepts STRING s as parameter.
     */
    public void printAll(){
        System.out.println("Printing all...");
        for(int i=0; i<29;i++){
            if(arr[i]!=0){
                System.out.print((char)arr[i]);
            }
        }
        System.out.println();
    }
    public static int alternate(String s) {
        Result res = new Result();
        // Write your code here
        s=res.removeDuplicates(s);

        for(int i=0; i<s.length();i++){
            char character = s.charAt(i);
            short value =(short)character;

            short hashState = res.hashTheValue(value);

            if(hashState!=-1){
                short charCount = 1;
//                System.out.println("Character is: "+character);
                IndexValNode idxNode = null;

                idxNode = res.InsertIndexInfo(i,idxNode);
//                System.out.println("Index init 1 "+i);
                for(int j=(i+1); j<s.length(); j++){
                    if(s.charAt(j)==character){
                        charCount++;
//                        System.out.println("Index init 2"+j);
                        idxNode = res.InsertIndexInfo(j,idxNode);
                    }
                }
                res.insertToTree(charCount,value,idxNode);
//                res.printAllTNodes();
//                res.charComparator();
            }
        }
//        res.printAll();
        res.InsertInOrderTreeWalk(res.root);
        int result = res.charCalculator();
//        res.printAllTNodes();
//        res.PostOrderTreeWalk(res.root);
//        res.printAllTNodes();
        if(result==-1){
            return 0;
        }else{
            return result;
        }

    }

    public void printAllTNodes(){
        tempNode tNode = tempNodeRoot;
        while(tNode!=null){
            System.out.println("tnNode key "+tNode.key);
            System.out.println("tnNode value "+(char)tNode.charASCII);
            System.out.println("Indexs: ");
            IndexPrinter(tNode.indexNodeRoot);
            tNode = tNode.next;

        }

    }

    private Tree treeMaximum(Tree x){
        while(x.rightChild!=null){
            x=x.rightChild;
        }
        return x;
    }
//    private Tree treePredecessor(Tree x){
//        if(x.rightChild!=null){
//            return treeMaximum(x.rightChild);
//        }
//    }
    private String removeDuplicates(String s){
        short stringSize =(short)(s.length()-1);

        for(short i=0; i<stringSize; i++){

            if(s.charAt(i) == s.charAt(i+1)){
                String temp = "";
                char removedChar =s.charAt(i);
                i=0;
                for(short j=0; j<(stringSize+1); j++){
                    if(s.charAt(j)!=removedChar){
                        temp+=s.charAt(j);
                    }
                }

                s=temp;
                stringSize=(short)(s.length()-1);

            }
        }
//        System.out.println("New String after removal "+s);
        return s;
    }

    public boolean checkIndexes(){
        return false;
    }

    public int charCalculator(){
        tempNode node = tempNodeRoot;
        int result=0;
        int tempKey =-1;
        int tempResult =-1;
        while(node!=null) {
            tempNode childNode = node.next;
//            System.out.println("Main "+(char)node.charASCII);
//            System.out.println("Child "+(char)childNode.charASCII);
            while (childNode != null) {
                if (node.key == childNode.key) {
                    //compare indexes
                    result = IndexComparator(node, childNode);

                    if (result > -1) {

                        return result;
                    }
                    childNode = childNode.next;

                } else if ((node.key - 1) == (childNode.key)) {
                    //compare indexes
                    result = IndexComparator(node, childNode);
                    if (result > -1) {
//                        System.out.println("Result found:"+(char) node.charASCII);
//                        System.out.println("Result found:"+(char) childNode.charASCII);
//                        System.out.println("Result total:"+result);
                            if (node.next.key == node.key) {
                                if (tempKey != -1) {
                                    if (result > tempResult) {
                                        return result;
                                    }
                                } else {
                                    tempKey = node.key;
                                    tempResult = result;
                                }
                            } else {
                                if (result >= tempResult) {
                                    return result;
                                } else {
                                    return tempResult;
                                }
                            }

                        }

                    childNode = childNode.next;


                } else {
                    childNode = null;
                }

            }

            if (node != null) {
                node = node.next;
            }
        }
        return result;
    }

    public Short IndexComparator(tempNode mainNode, tempNode childNode){

        if((mainNode.key-1)==childNode.key){
            IndexValNode mainNodeIndexes = mainNode.indexNodeRoot;
            IndexValNode childNodeIndexes = childNode.indexNodeRoot;
            while(mainNodeIndexes!=null){

                if(mainNodeIndexes.next!=null){

                    if(childNodeIndexes.next!=null){
                        if(mainNodeIndexes.next.key <childNodeIndexes.next.key){
                            return -1;
                        }
                    }

                    if((mainNodeIndexes.key>childNodeIndexes.key)&&(mainNodeIndexes.next.key<childNodeIndexes.key)){
                            mainNodeIndexes = mainNodeIndexes.next;
                            childNodeIndexes=childNodeIndexes.next;

                        }else{
                            return -1;
                        }
                }else{
                    mainNodeIndexes = mainNodeIndexes.next;
                }

            }
            short totalStrSize = (short)(mainNode.key+childNode.key);
            return totalStrSize;
        }else if(mainNode.key==childNode.key){
            IndexValNode mainNodeIndexes = mainNode.indexNodeRoot;
            IndexValNode childNodeIndexes = childNode.indexNodeRoot;

            if(mainNodeIndexes.key>childNodeIndexes.key){
                while(mainNodeIndexes!=null){
                    if(mainNodeIndexes.next!=null){
                        if(childNodeIndexes.next!=null){
                            if(mainNodeIndexes.next.key<childNodeIndexes.next.key){
                                return -1;
                            }
                        }
                        if((mainNodeIndexes.key>childNodeIndexes.key)&&(mainNodeIndexes.next.key<childNodeIndexes.key)){
                            mainNodeIndexes = mainNodeIndexes.next;
                            childNodeIndexes=childNodeIndexes.next;

                        }else{
                            return -1;
                        }
                    }else{
                        mainNodeIndexes= mainNodeIndexes.next;
                    }

                }

            }else{
                while(childNodeIndexes!=null){
                    if(childNodeIndexes.next!=null){
                        if(mainNodeIndexes.next!=null){
                            if(childNodeIndexes.next.key <mainNodeIndexes.next.key){
                                return -1;
                            }
                        }
                        if((childNodeIndexes.key>mainNodeIndexes.key)
                                &&(childNodeIndexes.next.key<mainNodeIndexes.key)){
                            mainNodeIndexes = mainNodeIndexes.next;
                            childNodeIndexes=childNodeIndexes.next;

                        }else{
                            return -1;
                        }
                    }else{
                        childNodeIndexes=childNodeIndexes.next;
                    }

                }
            }
            short totalStrSize = (short)(mainNode.key*2);
            return totalStrSize;
        }
        return -1;
    }

    public void nodeInsert(Tree node){
        tempNode newNode = new tempNode(node.key,node.value, node.indexNodeRoot);
        newNode.next = tempNodeRoot;
        tempNodeRoot = newNode;
//        System.out.println(node.key);
    }

    public void IndexPrinter(IndexValNode node){
        while(node!=null){
            System.out.print(node.key+" ,");
            node = node.next;
        }
        System.out.println();
    }
    public void InsertInOrderTreeWalk(Tree node){
        if(node!=null){
            InsertInOrderTreeWalk(node.leftChild);
            //This algorithm is under process still...
            this.nodeInsert(node);
            InsertInOrderTreeWalk(node.rightChild);
        }

    }
    public void printSubTreeWithIndexes(IndexValNode node){
        while(node!=null){
            System.out.print(node.key);
            System.out.print(',');
            node=node.next;
        }
    }

    public void PostOrderTreeWalk(Tree node){
        if(node!=null){
            PostOrderTreeWalk(node.rightChild);
            //This algorithm is under process still...

            System.out.println("Key "+node.key);
            System.out.println("value "+(char)node.value);
            System.out.println("Indexes:");
            printSubTreeWithIndexes(node.indexNodeRoot);
            System.out.println();

            PostOrderTreeWalk(node.leftChild);
        }

    }

    private short hashTheValue(short key){
        if(this.SearchElement(key)==1){
            return -1;
        }
        InsertHash(key);
        return 1;

    }

    private int CalculateIndex(int key){
        return key%this.sizeOfHashArray;
    }

    public short SearchElement(int key){
        int index = this.CalculateIndex(key);
        if(arr[index]!=0){
            return 1;
        }
        return 0;
    }

    public void InsertHash(int key ){
        int index = this.CalculateIndex(key);

        this.arr[index] =key;
    }

    private void insertToTree(short key, short count, IndexValNode idxNode){
        TreeInsert(key,count,idxNode);
    }

}
