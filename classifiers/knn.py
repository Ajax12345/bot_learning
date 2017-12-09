import itertools

class KNN:
    def __init__(self, *new_data):
        self.new_data = new_data


    def train(self, k=2):
        with open('testing_data.txt') as f:
            f = [map(float, i.strip('\n').split()) for i in f]

        new_f = [(a, list(b)) for a, b in itertools.groupby(sorted(f, key=lambda x:x[0]), key=lambda x:x[0])]

        normalized_data = {a:zip(*[[(c-min(d))/float(max(d)-min(d)) for c in d] for d in zip(*[i[1:] for i in b])]) for a, b in new_f}

        training = [(a, sum(pow(sum(pow(c-d, 2) for c, d in zip(h, self.new_data)), 2) for h in b)) for a, b in normalized_data.items()]
        results = [i[0] for i in sorted(training, key=lambda x:x[-1])][-k:]
        return max(results, key=lambda x:results.count(x))
        #return max([i[0] for i in sorted(training, key=lambda x:x[-1])[-k:]], key=lambda x:)



print KNN(30, 40).train(k=1)
