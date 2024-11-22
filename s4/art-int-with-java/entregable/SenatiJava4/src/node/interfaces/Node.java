package node.interfaces;

import node.type.NodeType;

public interface Node<T extends Number & Comparable<T>> {
    T getValue();
    NodeType getType();
    Node<T> getParent();
    boolean hasParent();
}
