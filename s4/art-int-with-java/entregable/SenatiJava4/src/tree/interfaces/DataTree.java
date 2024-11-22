package tree.interfaces;

import node.interfaces.Node;

import java.util.Collection;
import java.util.Optional;
import java.util.Set;

public interface DataTree<T extends Number & Comparable<T>, N extends Node<T>> {
    N getRootNode();
    int getCountOfNodes();
    Set<? extends N> getTreeNodes();
    Optional<? extends N> findByData(T data);
    Optional<T> findByRefNode (N node);
    void addAllNodes (Collection<N> nodes);
    void addNode (N node);
}
