package tree.interfaces;

import node.interfaces.BinaryNode;

public interface BinaryDataTree<T extends Number & Comparable<T>, N extends BinaryNode<T>> extends DataTree<T, N> {
    void putNodeToLeft(N node);
    void putNodeToRight(N node);
    //void putNodeToLeft(N node, N targetNode, boolean replaceNode);
    //void putNodeToRight(N node, N targetNode, boolean replaceNode);
    N putNodeToLeft (T data);
    N putNodeToRight (T data);
    //N putNodeToLeft (T data, N targetNode, boolean replaceNode);
    //N putNodeToRight (T data, N targetNode);
}
