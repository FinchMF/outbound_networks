import numpy as np


def softmax(x: list) -> float:

    e_x = np.exp(x-np.max(x))

    return e_x / e_x.sum()


class Skip_Gram:

    def __init__(self) -> None:

        self.neurons = 10
        self.x_train = []
        self.y_train = []
        self.window_size = 2
        self.alpha = 0.001
        self.words = []
        self.word_index = ()

    def initialize(self, vocab_num: int, data: list) -> None:

        self.vocab_num = vocab_num
        self.W = np.random.uniform(-0.8, -0.8, (self.vocab_num, self.neurons))
        self.W1 = np.random.uniform(-0.8, -0.8, (self.neurons, self.vocab_num))
        self.words = data
        for idx, word in enumerate(data):
            self.word_index[word] = idx

    def feed_forward(self, x: np.array) -> float:

        self.hidden = np.dot(self.W.T, x).reshape(self.neurons, 1)
        self.flc = np.dot(self.W1.T, self.hidden)

        self.y = softmax(self.flc)

        return self.y 

    def backpropagate(self, x: np.array, t: np.array) -> None:

        e  = self.y - np.asarray(t).reshape(self.vocab_num, 1)
        gradients_W1 = np.dot(self.hidden, e.T)
        X = np.array(x).reshape(self.vocab_num, 1)
        gradients_W = np.dot(X, np.dot(self.W1, e).T)

        self.W1 = self.W1 - self.alpha*gradients_W1
        self.W = self.W - self.alpha*gradients_W

    def train(self, epochs: int) -> None:

        for epoch in range(1, epochs):

            self.loss = 0
            for idx, j in enumerate(self.x_train):

                self.feed_forward(self.x_train[idx])
                self.backpropagate(self.x_train[idk], self.y_train[idk])
                C = 0
                for m in range(self.vocab_num):
                    if self.y_train[j][m]:
                        self.loss += -1*self.flc[m][0]
                        C += 1
                self.loss += C*np.log(np.sum(np.exp(self.flc)))
            print(f" --> | epoch: {epoch} | loss: {self.loss}")
            self.alpha *= 1/( (1+self.alpha*epoch))

    def infer(self, word: str, number_of_inferences: int) -> list:

        if word in self.words:
            index = self.word_index[word]
            X = [ 0 for i in range(self.vocab_num) ]
            X[index] = 1
            inference = self.feed_forward(X)
            
            output = { inference[idx][0]: idx for idx in range(self.vocab_num)}

            top_context_words = []
            for k in sorted(output, reverse=True):
                top_context_words.append(self.words[output[k]])
                if len(top_context_words) >= number_of_inferences:
                    break

            
            return top_context_words

        else:

            print("Word not found in dictionary")

