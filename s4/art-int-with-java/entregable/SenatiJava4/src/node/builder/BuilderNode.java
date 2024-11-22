package node.builder;

import node.interfaces.Node;

public interface BuilderNode<T extends Number & Comparable<T>, N extends Node<T>> {
    N build ();
}
