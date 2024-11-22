import node.BiDirectionalNode;
import node.interfaces.BinaryNode;
import tree.BinaryTree;

import static node.BiDirectionalNode.BiDirectionalNodeBuilder;

public class Main {
    public static void main(String[] args) {
        BinaryNode<Integer> rootNode = new BiDirectionalNode<Integer>(10);
        BinaryTree<Integer> tree = new BinaryTree<Integer>(rootNode);
        BiDirectionalNodeBuilder<Integer> builder = new BiDirectionalNodeBuilder<Integer>();

        BinaryNode<Integer> a = builder.setData(12).setParentNode(rootNode, rootNode::setLeftNode).build();
        BinaryNode<Integer> b = builder.setData(11).setParentNode(rootNode, rootNode::setRightNode).build();
        var c = builder.setData(15).setParentNode(b, b::setRightNode).build();
        var d = builder.setData(22).setParentNode(a, a::setRightNode).build();

        tree.print();

    }
}
