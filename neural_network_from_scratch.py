"""
Basic Neural Network from Scratch (NumPy only)
------------------------------------------------
Task: Classify handwritten digits (0-9)
No ML libraries (sklearn/tensorflow/pytorch) are used to BUILD the model.
sklearn is used only to load the built-in digits dataset (8x8 images).

Implements:
  - Forward propagation (ReLU + Softmax)
  - Cross-entropy loss & accuracy
  - Manual backpropagation + gradient descent
  - Visualization of training curves, sample predictions, confusion matrix
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits  # data loading only, not modeling

# ----------------------------
# 1. Load & preprocess data
# ----------------------------
digits = load_digits()
X = digits.data.astype(np.float64)   # shape (1797, 64) -> 8x8 images flattened
y = digits.target                    # shape (1797,) -> labels 0-9

X /= 16.0  # normalize pixel values (0-16) to (0-1)

def one_hot(labels, num_classes=10):
    oh = np.zeros((labels.size, num_classes))
    oh[np.arange(labels.size), labels] = 1
    return oh

Y = one_hot(y)

# shuffle & split into train/test (80/20)
np.random.seed(42)
indices = np.random.permutation(len(X))
split = int(0.8 * len(X))
train_idx, test_idx = indices[:split], indices[split:]

X_train, X_test = X[train_idx], X[test_idx]
Y_train, Y_test = Y[train_idx], Y[test_idx]
y_train_labels, y_test_labels = y[train_idx], y[test_idx]

# ----------------------------
# 2. Activation functions
# ----------------------------
def relu(z):
    return np.maximum(0, z)

def relu_derivative(z):
    return (z > 0).astype(float)

def softmax(z):
    z_shifted = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

# ----------------------------
# 3. Initialize network (64 -> 32 -> 10)
# ----------------------------
input_size, hidden_size, output_size = 64, 32, 10

np.random.seed(1)
W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
b2 = np.zeros((1, output_size))

# ----------------------------
# 4. Forward propagation
# ----------------------------
def forward(X, W1, b1, W2, b2):
    Z1 = X @ W1 + b1
    A1 = relu(Z1)
    Z2 = A1 @ W2 + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2

# ----------------------------
# 5. Loss & accuracy
# ----------------------------
def cross_entropy_loss(Y_pred, Y_true):
    m = Y_true.shape[0]
    eps = 1e-9
    return -np.sum(Y_true * np.log(Y_pred + eps)) / m

def accuracy(Y_pred, true_labels):
    preds = np.argmax(Y_pred, axis=1)
    return np.mean(preds == true_labels)

# ----------------------------
# 6. Backpropagation
# ----------------------------
def backward(X, Y_true, Z1, A1, A2, W2):
    m = X.shape[0]
    dZ2 = A2 - Y_true
    dW2 = (A1.T @ dZ2) / m
    db2 = np.sum(dZ2, axis=0, keepdims=True) / m

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * relu_derivative(Z1)
    dW1 = (X.T @ dZ1) / m
    db1 = np.sum(dZ1, axis=0, keepdims=True) / m

    return dW1, db1, dW2, db2

# ----------------------------
# 7. Training loop
# ----------------------------
epochs = 300
lr = 0.5

train_losses, train_accs, test_losses, test_accs = [], [], [], []

for epoch in range(epochs):
    Z1, A1, Z2, A2 = forward(X_train, W1, b1, W2, b2)
    loss = cross_entropy_loss(A2, Y_train)
    acc = accuracy(A2, y_train_labels)

    dW1, db1, dW2, db2 = backward(X_train, Y_train, Z1, A1, A2, W2)
    W1 -= lr * dW1
    b1 -= lr * db1
    W2 -= lr * dW2
    b2 -= lr * db2

    _, _, _, A2_test = forward(X_test, W1, b1, W2, b2)
    test_loss = cross_entropy_loss(A2_test, Y_test)
    test_acc = accuracy(A2_test, y_test_labels)

    train_losses.append(loss); train_accs.append(acc)
    test_losses.append(test_loss); test_accs.append(test_acc)

    if epoch % 30 == 0 or epoch == epochs - 1:
        print(f"Epoch {epoch:3d} | Train Loss: {loss:.4f} Acc: {acc:.4f} "
              f"| Test Loss: {test_loss:.4f} Acc: {test_acc:.4f}")

print(f"\nFinal Test Accuracy: {test_accs[-1]*100:.2f}%")

# ----------------------------
# 8. Visualization
# ----------------------------
_, _, _, preds_test = forward(X_test, W1, b1, W2, b2)
pred_labels = np.argmax(preds_test, axis=1)

conf_matrix = np.zeros((10, 10), dtype=int)
for t, p in zip(y_test_labels, pred_labels):
    conf_matrix[t, p] += 1

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(train_losses, label="Train Loss")
axes[0, 0].plot(test_losses, label="Test Loss")
axes[0, 0].set_title("Loss over Epochs")
axes[0, 0].set_xlabel("Epoch"); axes[0, 0].set_ylabel("Loss")
axes[0, 0].legend()

axes[0, 1].plot(train_accs, label="Train Acc")
axes[0, 1].plot(test_accs, label="Test Acc")
axes[0, 1].set_title("Accuracy over Epochs")
axes[0, 1].set_xlabel("Epoch"); axes[0, 1].set_ylabel("Accuracy")
axes[0, 1].legend()

axes[1, 0].axis("off")
axes[1, 0].text(0.05, 0.5,
                 f"Final Test Accuracy:\n{test_accs[-1]*100:.2f}%\n\n"
                 f"Final Test Loss:\n{test_losses[-1]:.4f}",
                 fontsize=16)

axes[1, 1].imshow(conf_matrix, cmap="Blues")
axes[1, 1].set_title("Confusion Matrix")
axes[1, 1].set_xlabel("Predicted"); axes[1, 1].set_ylabel("Actual")
for i in range(10):
    for j in range(10):
        axes[1, 1].text(j, i, conf_matrix[i, j], ha="center", va="center", fontsize=8)

fig.tight_layout()
fig.savefig("training_results.png", dpi=150)

sample_fig, sample_axes = plt.subplots(2, 4, figsize=(10, 5))
for i, ax in enumerate(sample_axes.flat):
    img = X_test[i].reshape(8, 8)
    ax.imshow(img, cmap="gray")
    color = "green" if pred_labels[i] == y_test_labels[i] else "red"
    ax.set_title(f"Pred: {pred_labels[i]} / True: {y_test_labels[i]}", color=color, fontsize=10)
    ax.axis("off")
sample_fig.suptitle("Sample Predictions on Test Set")
sample_fig.tight_layout()
sample_fig.savefig("sample_predictions.png", dpi=150)

plt.close("all")
print("\nPlots saved: training_results.png, sample_predictions.png")
