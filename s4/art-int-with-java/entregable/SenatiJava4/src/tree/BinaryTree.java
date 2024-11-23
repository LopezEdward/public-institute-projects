package tree;

import node.BiDirectionalNode;
import node.interfaces.BinaryNode;
import node.type.NodeType;
import tree.interfaces.BinaryDataTree;
import tree.transversal.TreePrintOrder;

import java.util.*;

public class BinaryTree<T extends Number & Comparable<T>> implements BinaryDataTree<T, BinaryNode<T>>, TreePrintOrder<T, BinaryNode<T>> {
    private Set<BinaryNode<T>> treeNodes = new HashSet<>(5);
    private final BinaryNode<T> rootNode;
    private BinaryNode<T> leftLastNode;
    private BinaryNode<T> rightLastNode;

    public BinaryTree(BinaryNode<T> rootNode) throws IllegalArgumentException {
        if (rootNode.getType() != NodeType.ROOT) throw new IllegalArgumentException();

        this.rootNode = rootNode;
        this.treeNodes.add(rootNode);
    }

    public BinaryTree(BinaryNode<T> rootNode, Set<BinaryNode<T>> nodes) throws IllegalArgumentException {
        if (rootNode.getType() != NodeType.ROOT) throw new IllegalArgumentException();

        this.rootNode = rootNode;
        this.treeNodes = nodes;
        this.treeNodes.add(rootNode);
    }

    @Override
    public BinaryNode<T> getRootNode() {
        return rootNode;
    }

    @Override
    public int getCountOfNodes() {
        return this.treeNodes.size();
    }

    @Override
    public Set<BinaryNode<T>> getTreeNodes() {
        return this.treeNodes;
    }

    @Override
    public Optional<BinaryNode<T>> findByData(T data) {
        for (BinaryNode<T> item : this.treeNodes) {
            if (item.getValue().equals(data)) return Optional.of(item);
        }

        return Optional.empty();
    }

    @Override
    public Optional<T> findByRefNode(BinaryNode<T> node) {
        for (BinaryNode<T> item: this.treeNodes) {
            if (item.equals(node)) return Optional.of(item.getValue());
        }

        return Optional.empty();
    }

    @Override
    public void addAllNodes(Collection<BinaryNode<T>> nodes) {
        nodes.removeIf((node) -> node.getType().equals(NodeType.ROOT));

        this.treeNodes.addAll(nodes);
    }

    @Override
    public void addNode(BinaryNode<T> node) {
        if (node.getType().equals(NodeType.ROOT)) return;

        this.treeNodes.add(node);
    }

    @Override
    public void printPostOrder() {
        this.printPostOrder(this.rootNode);
    }

    @Override
    public void printPreOrder() {
        this.printPreOrder(this.rootNode);
    }

    @Override
    public void printInOrder() {
        this.printInOrder(this.rootNode);
    }

    @Override
    public void printPostOrder(BinaryNode<T> node) {
        if (node == null) return;

        printPostOrder(node.getLeftNode());
        printPostOrder(node.getRightNode());
        System.out.println(node.supplierNodeInfo());
    }

    @Override
    public void printPreOrder(BinaryNode<T> node) {
        if (node == null) return;

        System.out.println(node.supplierNodeInfo());
        printPreOrder(node.getLeftNode());
        printPreOrder(node.getRightNode());
    }

    @Override
    public void printInOrder(BinaryNode<T> node) {
        if (node == null) return;

        printInOrder(node.getLeftNode());
        System.out.println(node.supplierNodeInfo());
        printInOrder(node.getRightNode());
    }

    @Override
    public void putNodeToLeft(BinaryNode<T> node) {
        if (this.treeNodes.contains(node)) return;

        if (this.leftLastNode != null && !this.leftLastNode.hasLeftNode()) {
            this.leftLastNode.setLeftNode(node);
            this.leftLastNode = node;
            return;
        }

        BinaryNode<T> lastNode = null;
        BinaryNode<T> target = null;

        while (true) {
            if (lastNode != null) {
                if (!lastNode.hasLeftNode()) {
                    target = lastNode;
                    break;
                }

                lastNode = lastNode.getLeftNode();
                continue;
            }

            lastNode = this.rootNode.getLeftNode();
        }

        target.setLeftNode(node);
        this.leftLastNode = node;
        this.treeNodes.add(node);
    }

    @Override
    public void putNodeToRight(BinaryNode<T> node) {
        if (this.treeNodes.contains(node)) return;

        if (this.rightLastNode != null && !this.rightLastNode.hasRightNode()) {
            this.rightLastNode.setRightNode(node);;
            this.rightLastNode = node;
            return;
        }

        BinaryNode<T> lastNode = null;
        BinaryNode<T> target = null;

        while (true) {
            if (lastNode != null) {
                if (!lastNode.hasRightNode()) {
                    target = lastNode;
                    break;
                }

                lastNode = lastNode.getRightNode();
                continue;
            }

            lastNode = this.rootNode.getRightNode();
        }

        target.setRightNode(node);
        this.rightLastNode = node;
        this.treeNodes.add(node);
    }

    public void putNodeToLeft(BinaryNode<T> node, BinaryNode<T> targetNode, boolean replaceChild) throws NullPointerException {
        if (targetNode.hasLeftNode() && !replaceChild) return;
        if (node == null) throw new NullPointerException("The node is null!");

        targetNode.setLeftNode(node);

        if (targetNode.equals(this.leftLastNode)) this.leftLastNode = node;
    }

    public void putNodeToRight(BinaryNode<T> node, BinaryNode<T> targetNode, boolean replaceChild) throws NullPointerException {
        if (targetNode.hasRightNode() && !replaceChild) return;
        if (node == null) throw new NullPointerException("The node is null!");

        targetNode.setRightNode(node);

        if (targetNode.equals(this.rightLastNode)) this.rightLastNode = node;
    }

    @Override
    public BinaryNode<T> putNodeToLeft(T data) {
        BinaryNode<T> newNode = new BiDirectionalNode<>(data);

        if (this.leftLastNode != null && !this.leftLastNode.hasLeftNode()) {
            this.leftLastNode.setLeftNode(newNode);
            this.leftLastNode = newNode;
            return newNode;
        }

        BinaryNode<T> lastNode = null;
        BinaryNode<T> target = null;

        while (true) {
            if (lastNode != null) {
                if (!lastNode.hasLeftNode()) {
                    target = lastNode;
                    break;
                }

                lastNode = lastNode.getLeftNode();
                continue;
            }

            lastNode = this.rootNode.getLeftNode();
        }

        target.setLeftNode(newNode);
        this.leftLastNode = newNode;

        return newNode;
    }

    @Override
    public BinaryNode<T> putNodeToRight(T data) {
        BinaryNode<T> newNode = new BiDirectionalNode<>(data);

        if (this.rightLastNode != null && !this.rightLastNode.hasLeftNode()) {
            this.rightLastNode.setRightNode(newNode);
            this.rightLastNode = newNode;
            return newNode;
        }

        BinaryNode<T> lastNode = null;
        BinaryNode<T> target = null;

        while (true) {
            if (lastNode != null) {
                if (!lastNode.hasRightNode()) {
                    target = lastNode;
                    break;
                }

                lastNode = lastNode.getRightNode();
                continue;
            }

            lastNode = this.rootNode.getRightNode();
        }

        target.setLeftNode(newNode);
        this.leftLastNode = newNode;

        return newNode;
    }

    public Optional<BinaryNode<T>> putNodeToLeft(T data, BinaryNode<T> targetNode, boolean replaceChild) {
        if (targetNode.hasLeftNode() && !replaceChild) return Optional.empty();

        BinaryNode<T> node = new BiDirectionalNode<>(data);
        targetNode.setLeftNode(node);

        if (targetNode.equals(this.leftLastNode)) this.leftLastNode = node;

        return Optional.of(node);
    }

    public Optional<BinaryNode<T>> putNodeToRight(T data, BinaryNode<T> targetNode, boolean replaceChild) {
        if (targetNode.hasRightNode() && !replaceChild) return Optional.empty();

        BinaryNode<T> node = new BiDirectionalNode<>(data);
        targetNode.setRightNode(node);

        if (targetNode.equals(this.rightLastNode)) this.rightLastNode = node;

        return Optional.of(node);
    }
}
