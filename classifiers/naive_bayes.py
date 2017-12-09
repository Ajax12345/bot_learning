import itertools
import math
import operator

class UnbalancedExpectedResult(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class NaiveBayes:
    def __init__(self, *new_input, **kwargs):
        self.new_input = new_input
        self.headers = None
        self.observations = None
        self.filename = kwargs.get('filename', 'testing_data.txt')
        self.kwargs = kwargs
        self.predict()

    @property
    def output(self):
        
        new_listing = [[the_name, self.__dict__[the_name]*reduce(lambda x, y:x*y, [self.given_new_data(a, self.means[the_type][b], self.variances[1][b]) for a, b in zip(self.new_input, self.headers)])] for the_type, the_name in self.observations.items()]

        return sorted(new_listing, key=lambda x:x[-1])[-self.kwargs.get('top_results', 1):][0][0]

    def predict(self, observations = {1:"successful", 0:"unsuccessful"}, data_types=['t1', 't2', 't3']):
        self.headers = data_types
        self.observations = observations

        with open(self.filename) as f:

            f = [map(float, i.strip('\n').split()) for i in f]



        new_data = [(a, list(b)) for a, b in itertools.groupby(sorted(f, key=lambda x:x[0]), key=lambda x:x[0])]
        means = {a:{c:sum(i)/float(len(i)) for c, i in zip(data_types, list(zip(*b))[1:])} for a, b in new_data}
        variances = {a:{c:sum(pow(e-means[a][c], 2) for e in i)/float(len(i)) for c, i in zip(data_types, list(zip(*b))[1:])} for a, b in new_data}
        self.__dict__['means'] = means
        self.__dict__['variances'] = variances
        if len(set([i[0] for i in f])) < self.kwargs.get('top_results', 1):
            raise UnbalancedExpectedResult("value of 'top_results' ({}) must be less than length of input observations ({})".format(self.kwargs.get('top_results', 1), len(set([i[0] for i in f]))))
        for a, b in observations.items():
            self.__dict__[b] = [i[0] for i in f].count(a)



    def given_new_data(self, x, mean, variance):
        return (1/float(pow(2*math.pi*variance, 0.5)))*pow(math.e, -1*(pow((x-mean), 2)/float(2*variance)))
