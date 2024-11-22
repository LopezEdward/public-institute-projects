package tree.transversal;

import node.interfaces.Node;

public interface TreePrintOrder<T extends Number & Comparable<T>, N extends Node<T>> {
    default void print() {
        System.out.println("Print the result of method \"printInOrder\"");
        printInOrder();
        System.out.println("Print the result of method \"printPostOrder\"");
        printPostOrder();
        System.out.println("Print the result of method \"printPreOrder\"");
        printPreOrder();
    }
    void printPostOrder();
    void printPreOrder();
    void printInOrder();
    void printPostOrder(N node);
    void printPreOrder(N node);
    void printInOrder(N node);
}
