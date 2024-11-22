package node.interfaces;

import node.print.NodePrintable;

public interface BinaryNode<T extends Number & Comparable<T>> extends Node<T>, NodePrintable {
    BinaryNode<T> getParent();
    BinaryNode<T> getLeftNode();
    BinaryNode<T> getRightNode();
    void setLeftNode(BinaryNode<T> node);
    void setRightNode(BinaryNode<T> node);
    boolean hasLeftNode();
    boolean hasRightNode();
}
