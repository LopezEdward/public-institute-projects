package exceptions;

public class HasChildNodeException extends IllegalArgumentException {
    public HasChildNodeException () {
        super();
    }

    public HasChildNodeException (String message) {
        super(message);
    }

    public HasChildNodeException (String message, Throwable cause) {
        super(message, cause);
    }

    public HasChildNodeException (Throwable cause) {
        super(cause);
    }
}
