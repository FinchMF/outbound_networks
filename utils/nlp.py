import numpy as np
import string


def softmax(x: list) -> float:

    e_x = np.exp(x-np.max(x))

    return e_x / e_x.sum()


class Skip_Gram:

	def __init__(self) -> None:

		self.neurons = 10
		self.X_train = []
		self.y_train = []
		self.window_size = 2
		self.alpha = 0.001
		self.words = []
		self.word_index = {}

	def initialize(
        
        self,
        vocab_size: int,
        data: list
        
        ) -> None:

		self.vocab_size = vocab_size
		self.W = np.random.uniform(-0.8, 0.8, (self.vocab_size, self.neurons))
		self.W1 = np.random.uniform(-0.8, 0.8, (self.neurons, self.vocab_size))
		
		self.words = data
		for i in range(len(data)):
			self.word_index[data[i]] = i

	
	def feed_forward(
        
        self,
        X: np.array
        
        ) -> float:

		self.h = np.dot(self.W.T, X).reshape(self.neurons,1)
		self.u = np.dot(self.W1.T,self.h)
		self.y = softmax(self.u)

		return self.y
		
	def backpropagate(
        
        self,
        x: list,
        t: list
        
        ) -> None:
        
		e = self.y - np.asarray(t).reshape(self.vocab_size,1)
		dLdW1 = np.dot(self.h,e.T)
		X = np.array(x).reshape(self.vocab_size, 1)
		dLdW = np.dot(X, np.dot(self.W1,e).T)
		self.W1 = self.W1 - self.alpha*dLdW1
		self.W = self.W - self.alpha*dLdW
		
	def train(
        
        self,
        epochs: int
        
        ) -> None:

		for x in range(1,epochs):

			self.loss = 0
			for j in range(len(self.X_train)):
				self.feed_forward(self.X_train[j])
				self.backpropagate(self.X_train[j],self.y_train[j])

				C = 0
				for m in range(self.vocab_size):
					if(self.y_train[j][m]):
						self.loss += -1*self.u[m][0]
						C += 1
				self.loss += C*np.log(np.sum(np.exp(self.u)))

			print(f" | epoch {x} | loss: {self.loss} ")
			self.alpha *= 1/( (1+self.alpha*x) )

			
	def predict(

		self,
		word: str,
		number_of_predictions: int

		) -> list:

		if word in self.words:

			index = self.word_index[word]
			X = [0 for i in range(self.vocab_size)]
			X[index] = 1

			prediction = self.feed_forward(X)

			output = {}
			for i in range(self.vocab_size):
				output[prediction[i][0]] = i

			top_context_words = []
			for k in sorted(output,reverse=True):
				top_context_words.append(self.words[output[k]])
				if(len(top_context_words)>=number_of_predictions):
					break

			return top_context_words

		else:

			print("Word not found in dictionary")



class Text_Tools:

	@staticmethod
	def preprocessing(
		
		corpus: str, 
		stopwords: list
		
		) -> list:

		training_data = []
		sentences = corpus.split(".")

		for i in range(len(sentences)):

			sentences[i] = sentences[i].strip()
			sentence = sentences[i].split()
			x = [word.strip(string.punctuation) for word in sentence if word not in stopwords]
			x = [word.lower() for word in x]

			training_data.append(x)

		return training_data
		

	@staticmethod
	def prepare_data_for_training(
		
		sentences: list,
		model: Skip_Gram
		
		) -> None:

		data = {}
		for sentence in sentences:
			for word in sentence:

				if word not in data:
					data[word] = 1
				else:
					data[word] += 1

		V = len(data)
		data = sorted(list(data.keys()))

		vocab = {}
		for i in range(len(data)):
			vocab[data[i]] = i
		
		for sentence in sentences:
			for i in range(len(sentence)):
				center_word = [0 for x in range(V)]
				center_word[vocab[sentence[i]]] = 1
				context = [0 for x in range(V)]
				
				for j in range(i-model.window_size,i+model.window_size):
					if i!=j and j>=0 and j<len(sentence):
						context[vocab[sentence[j]]] += 1
				model.X_train.append(center_word)
				model.y_train.append(context)
		model.initialize(V,data)
 




