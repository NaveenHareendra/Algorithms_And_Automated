public class Tree {

    public Node root;
    tempNode tempNodeRoot;

    static class Node{
        int key;
        private Node parent;
        private Node right;
        private Node left;

        Node(int key){
            this.key = key;
        }
    }

    static class tempNode{
        private int key;
        private tempNode next;

//        private tempNode node;
        tempNode(int  element){
            key=element;
        }
    }
    public int printHead(){
        return root.key;
    }
    public Node TreeMinimum(Node node){
        while(node.left!=null){
            node = node.left;
        }
        return node;
    }
    public void InOrderTreeWalk(Node node){
        if(node!=null){
            InOrderTreeWalk(node.left);
            tempNode newNode = new tempNode(node.key);
            newNode.next = tempNodeRoot;
            tempNodeRoot = newNode;
            System.out.println(node.key);
            InOrderTreeWalk(node.right);
        }
    }
    public void InOrderTreeWalkInsertMode(Node node){
        if(node!=null){
            InOrderTreeWalk(node.left);
            tempNode newNode = new tempNode(node.key);
            newNode.next = tempNodeRoot;
            tempNodeRoot = newNode;
            System.out.println(node.key);
            InOrderTreeWalk(node.right);
        }
    }

    public void printAllTNodes(){
        tempNode tNode = tempNodeRoot;
        while(tNode!=null){
            System.out.println("tnNode "+tNode.key);
            tNode = tNode.next;

        }

    }

    public void printNodeByNode(){
        tempNode tNode = tempNodeRoot;
        while(tNode!=null){
            tempNode childNode = tNode.next;
            while(childNode!=null){
                System.out.println("childNode: "+tNode.key);
                System.out.println("tnNode: "+childNode.key);
                childNode = childNode.next;

            }

            tNode = tNode.next;

        }
    }


    public void PostOrderTreeWalk(Node node){
        if(node!=null){
            PostOrderTreeWalk(node.right);

            System.out.println(node.key);
            PostOrderTreeWalk(node.left);
        }
    }
    public void CheckTwoChars(Node node){

        if(node!=null){
            if(node.parent!=null){
                CheckTwoChars(node.parent);
                System.out.println(node.key);
//                CheckTwoChars(node.parent.right);
//
//                CheckTwoChars(node.parent.left);
            }

        }
//      if(((node.parent.rightChild ==node)
//            &&((node.parent.value ==node.value)||((node.parent.value-1) ==node.value)))){
//        if(checkIndexes()==false){
//            PostOrderTreeWalk(node.leftChild);
//        }
//
//        }else if((node.parent.leftChild ==node)&&(node.parent.value ==(node.value-1))){
//            if(checkIndexes()==false){
//                if(node.leftChild!=null){
//                    PostOrderTreeWalk(node.leftChild);
//                }
//            }
//
//    }
    }
    //Better method than recursion
    public Node TreeSearchIterative(Node node, int key){
        while((node!=null)&&(key!=node.key)){
            if(key<node.key){
                node = node.left;
            }else{
                node=node.right;
            }
        }
        return node;
    }
    public Node leftMostNode(Node node){
        while(node.left!=null){
            node=node.left;
        }
        return node;
    }

    /*
    *
    * This algorithm can be improved a lot..
    * just as the basic two pointer method, this is a success
    * something like a greedy parent method this works.
    *
     */
    public void InOrderTreeWalkIterative(Node node){
        Node mainP = node;
        Node childP = null;
        Node childX = null;
        while(mainP.left!=null){
            mainP = mainP.left;
        }

        if(mainP.right!=null){
            childP = mainP.right;
            childX = mainP;
        }else{
            childP = mainP;
            childX = mainP;
        }
        System.out.println(mainP.key);
        do{

            while(childP != childX && childP !=mainP){
                if(childP.right==null){
                    while(mainP!=childX && childX != childP){
                        if(childX.right == childP){
                            if(childX.parent!= mainP){
                                childP = childX;
                                childX = childX.parent;
                            }else{
//                                mainP = mainP.parent;
                                System.out.println(childP.key);
                                childP = mainP;
                                childX = mainP;

                            }
                        }else if(childX.left == childP){
                            childP = childX;

                        }else{
                            System.out.println(childP.key);
                            childP = childP.parent;
                        }
                    }

                }

                if(childP!=mainP){
                    if(childP.left == null){
                        System.out.println(childP.key);
                        if(childP.right!=null){
                            childP=childP.right;
                        }else{
                            childP=mainP;
                        }
                    }else{
                        if(childX!=childP){
                            if(childP.left!=null){
                                childX=childP;
                                childP = childP.left;
                            }
                        }else{
                            if(childP.right!=null){
                                System.out.println(childP.key);
                                childP = childP.right;
                            }else {
                                System.out.println(childP.key);
                            }
                        }
                    }
                }

            }


            if(childX.parent!=null){

                if(mainP.parent.right!=null){
                    mainP = mainP.parent;

                    System.out.println(mainP.key);
                    childP = mainP.right;
                    childX =mainP;
//                    mainP = mainP.parent;
//                    childP = mainP.right;
//                    childX = mainP;
                }else {

                    mainP = mainP.parent;
                    childX =mainP;
                }
            }else{
                mainP=null;

            }
        }while(mainP !=null );

    }

    public Node TreeMaximum(Node node){
        while(node.right!=null){
            node=node.right;
        }
        return node;
    }

    //If all keys are distinct
    //Successor of a node x is node with smallest key greater than x.key
    public Node TreeSuccessor(Node node){
        if(node.right!=null){
            return TreeMinimum(node);
        }

        Node trailingPoint=node.parent;
        while((trailingPoint!=null)&&(node==trailingPoint.right)){
            node=trailingPoint;
            trailingPoint=trailingPoint.parent;
        }
        return trailingPoint;
    }

    //Read CLRS notes if needed explanations...
    //Otherwise possible to understand just by reading
    //This is just securing rules of the search trees..
    public void Transplant(Node u, Node v){
        if(u.parent == null){
            root=v;
        }else if(u==u.parent.left){
            u.parent.left=v;
        }else{
            u.parent.right=v;
        }
        if(v!=null){
            v.parent=u.parent;
        }
    }


    public void TreeDelete(Node z){
        if(z.left==null){
            Transplant(z,z.right);
        }else if(z.right==null){
            Transplant(z, z.left);
        }else{
            Node y = TreeMinimum(z.right);
            if(y.parent!=z){
                Transplant(y, y.right);
                y.right=z.right;
                y.right.parent=y;
            }
            Transplant(z,y);
            y.left=z.left;
            y.left.parent=y;
        }

    }

    public Node TreeSearch(Node node, int key){
        if(node==null || key==node.key) {
            return node;
        }
        if(key<node.key){
            return TreeSearch(node.left, key);
        }else{
            return TreeSearch(node.right, key);
        }
    }

    public Node getLeftOfRoot(){
        return root.left;
    }

    public void TreeInsert(int element){
        Node node =new Node(element);

        Node y = null;
        Node x = root;

        while(x!=null){
            y=x;
            if(node.key<x.key){
                x=x.left;
            }else{
                x=x.right;
            }
        }
        node.parent = y;
        if(y==null){
            root = node;
        }else if(node.key<y.key){
            y.left=node;
        }else{
            y.right = node;
        }
    }
}
