import torch

# linear regressio at sample level
class LinearRegressionSGD:
    def __init__(self, n_iter=1000, learning_rate=0.01) -> None:
        self.W = None
        self.B = None
        self.n_iter = n_iter
        self.learning_rate = learning_rate

    def loss_mse_dw(self, X, Y):
        X = X.unsqueeze(1)
        return 2 * ((X @ self.W) + self.B - Y) * X
    
    def loss_mse(self, X, Y):
        return ((X @ self.W) + self.B - Y) ** 2
    
    def loss_mse_db(self, X, Y):
        X = X.unsqueeze(1)
        return 2 * ((X @ self.W) + self.B - Y)
    
    def fit(self, X, Y):
        self.W = torch.zeros((X.shape[1], 1))
        self.B = torch.zeros(1)
        self.X = X
        self.Y = Y
        for i in range(self.n_iter):
            for x_sample, y_sample in zip(X, Y):
                dW = self.loss_mse_dw(x_sample, y_sample)
                dB = self.loss_mse_db(x_sample, y_sample)
                self.W = self.W - self.learning_rate * dW
                self.B = self.B - self.learning_rate * dB

    def predict(self, X):
        return (X @ self.W) + self.B
    
    def rmse_error(self, y_true, y_pred):
        return torch.sqrt(torch.mean((y_true - y_pred) ** 2))
    
# Linear regression at batch level
class LinearRegressionBatch:
    def __init__(self, n_iter=1000, lr=0.01) -> None:
        self.W = None
        self.B = None
        self.n_iter = n_iter
        self.lr = lr

    def loss_mse_dw(self, X, Y):
        return 2 *  torch.mean(((X @ self.W) + self.B - Y) * X, axis=0).reshape(-1, 1)
    
    def loss_mse(self, X, Y):
        return ((X @ self.W) + self.B - Y) ** 2
    
    def loss_mse_db(self, X, Y):
        return 2 * torch.mean((X @ self.W) + self.B - Y, axis=0)
    
    def fit(self, X, Y):
        self.W = torch.zeros((X.shape[1], 1))
        self.B = torch.zeros(1)
        self.X = X
        self.Y = Y
        for i in range(self.n_iter):
            dW = self.loss_mse_dw(X, Y)
            dB = self.loss_mse_db(X, Y)
            self.W = self.W - self.lr * dW
            self.B = self.B - self.lr * dB
            # Calculate and print accuracy after each epoch
            Y_pred = self.predict(X)
            accuracy = self.rmse_error(Y, Y_pred)
            print(f'Epoch {i+1}/{self.n_iter}, MSE Error: {accuracy}')

    def predict(self, X):
        return (X @ self.W) + self.B
    
    def rmse_error(self, y_true, y_pred):
        return torch.sqrt(torch.mean((y_true - y_pred) ** 2))


# linear regression without gradient descent
class NaiveRegression:
    def fit(self, X, Y):
        return torch.mean(Y)
    
    def predict(self, X):
        return torch.mean(X, axis=1)
    
    def rmse_error(self, y_true, y_pred):
        return torch.sqrt(torch.mean((y_true - y_pred) ** 2))