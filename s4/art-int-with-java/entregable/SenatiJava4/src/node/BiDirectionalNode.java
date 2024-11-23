package node;

import node.builder.BuilderNode;
import node.interfaces.BinaryNode;
import node.type.NodeType;

import java.util.function.Consumer;

public class BiDirectionalNode<T extends Number & Comparable<T>> implements BinaryNode<T> {
    private T data;
    private BinaryNode<T> leftNode;
    private BinaryNode<T> rightNode;
    private BinaryNode<T> parentNode;
    private final NodeType type;

    public static class BiDirectionalNodeBuilder<T extends Number & Comparable<T>> implements BuilderNode<T, BiDirectionalNode<T>> {
        private T data;
        private BinaryNode<T> leftNode;
        private BinaryNode<T> rightNode;
        private BinaryNode<T> parentNode;
        private Consumer<BinaryNode<T>> leafPosition = (n) -> {};
        //private NodeType type;

        public BiDirectionalNodeBuilder () {};

        public final BiDirectionalNodeBuilder<T> setData (T data) {
            this.data = data;
            return this;
        }

        public final BiDirectionalNodeBuilder<T> setParentNode (BinaryNode<T> parentNode) {
            this.parentNode = parentNode;
            return this;
        }

        public final BiDirectionalNodeBuilder<T> setParentNode (BinaryNode<T> parentNode, Consumer<BinaryNode<T>> leafPosition) {
            //System.out.println("B: " + this.leafPosition);
            this.parentNode = parentNode;
            this.leafPosition = leafPosition;
            //System.out.println("B: " +  leafPosition);
            //System.exit(100);
            return this;
        }

        public final BiDirectionalNodeBuilder<T> setLeftNode (BinaryNode<T> leftNode) {
            this.leftNode = leftNode;
            return this;
        }

        public final BiDirectionalNodeBuilder<T> setRightNode (BinaryNode<T> rightNode) {
            this.rightNode = rightNode;
            return this;
        }

        @Override
        public BiDirectionalNode<T> build() {
            //if (this.parentNode == null) this.type = NodeType.ROOT; else this.type = NodeType.CHILD;
            BiDirectionalNode<T> node = new BiDirectionalNode<>(this.data, this.leftNode, this.rightNode, this.parentNode);
            //System.out.println("A: " + this.leafPosition);
            //System.exit(100);
            this.leafPosition.accept(node);

            return node;
        }
    }

    public BiDirectionalNode (T data) {
        this.data = data;
        this.type = NodeType.ROOT;
    }

    public BiDirectionalNode (T data, BinaryNode<T> parent) {
        this.data = data;
        this.parentNode = parent;
        this.type = NodeType.CHILD;
    }

    public BiDirectionalNode (T data, BinaryNode<T> leftNode, BinaryNode<T> rightNode) {
        this.data = data;
        this.leftNode = leftNode;
        this.rightNode = rightNode;
        this.type = NodeType.ROOT;
    }

    public BiDirectionalNode (T data, BinaryNode<T> leftNode, BinaryNode<T> rightNode, BinaryNode<T> parentNode) {
        this.data = data;
        this.leftNode = leftNode;
        this.rightNode = rightNode;
        this.parentNode = parentNode;
        this.type = (parentNode == null) ? NodeType.ROOT : NodeType.CHILD;
    }

    @Override
    public T getValue() {
        return this.data;
    }

    public void setValue (T data) {
        this.data = data;
    }

    @Override
    public NodeType getType() {
        return this.type;
    }

    @Override
    public BinaryNode<T> getParent() {
        return this.parentNode;
    }

    public void setParent (BinaryNode<T> node) throws IllegalArgumentException {
        if (this.type == NodeType.ROOT) throw new IllegalArgumentException("The root node haven't parent.");

        this.parentNode = node;
    }

    @Override
    public boolean hasParent() {
        return this.parentNode != null;
    }

    public BinaryNode<T> getLeftNode() {
        return this.leftNode;
    }

    @Override
    public void setLeftNode(BinaryNode<T> leftNode) {
        this.leftNode = leftNode;
    }

    @Override
    public BinaryNode<T> getRightNode() {
        return this.rightNode;
    }

    @Override
    public void setRightNode(BinaryNode<T> rightNode) {
        this.rightNode = rightNode;
    }

    @Override
    public boolean hasLeftNode() {
        return this.leftNode != null;
    }

    @Override
    public boolean hasRightNode() {
        return this.rightNode != null;
    }

    @Override
    public String supplierNodeInfo() {
        return "BiDirectionalNode[type=NodeType." + this.type +",value=" + this.data + ",parent=" + this.parentNode + ",leftNode=" + this.leftNode + ",rightNode=" + this.rightNode + "]";
    }
}
