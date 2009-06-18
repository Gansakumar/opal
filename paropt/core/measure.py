import numpy

class Measure:
    '''
    We consider an instance of Measure like a head that points to
    a specific column in a measure value table
    In the context of Measure, a measure value table is the data
    '''
    __instances__ = {}
    # The __instances__ class variable is used to manager all instance of a measure
    # Each object of this class is a measure characteristized by it's name. May be there are many objects of
    # the same measure are created. There are only one object that created in module paropt.Measures is used
    # to evaluated the optimization model. This object call global measure object
    # The __instances__ variable have two roles:
    #   1 - Keep only one object for one measure. We have to synchronize or remove the clonned object (that may be 
    #       created by pickling
    #   2 - Set the data table for global measure object
    
    nullValue = {'real':0.0,'integer':0}
  
    def __init__(self,name=None, kind=None, **kwargs):
        self.name = name
        self.kind = kind
        self.is_real = (kind == 'real')
        self.is_integer = (kind == 'integer')
        self.data = None
        if name not in Measure.__instances__.keys():
            Measure.__instances__[name] = self
        else:
            self = Measure.__instances__[name]
        pass

    def get_global_object(self):
        # The function is used to determine the global measure object.
        # When a measure object is cloned (not created by __init__), the uniqueness is 
        # not assured. In this case, we have to replace the clonned object by the global measure object
        # pickle.load is an example
        # Return None if it is itself the global measure object or the the global measure object is not defined
        
        if self.name not in Measure.__instances__.keys():
            Measure.__instances__[self.name] = self
            return self
        if self == Measure.__instances__[self.name]:
            return self
        return Measure.__instances__[self.name]

    def set_data(self,data):
        self.data = data
        return

    def get_problem_value(self,p,prob):
        if self.data is not None:
            return self.data.get_cell(prob,self.name)
        else:
            return None

    def get_vector_value(self,p):
        if self.data is not None:
            return self.data.get_column(self.name)
        else:
            return None

    def __call__(self,p,prob=None):
        if prob is None:
            return self.get_vector_value(p)
        else:
            return self.get_problem_value(p,prob)
          

class MeasureValueTable:


    def __init__(self,problem_names,measure_names):
        self.problem_indices = {}
        for i in range(len(problem_names)):
            self.problem_indices[problem_names[i]] = i 
        self.measure_names = measure_names
        self.table = {} # this mapping with key is the name of measure
                        # and value is a list of value
                        # We don't use the table because, the different measure
                        # have different type
        for measure in self.measure_names:
            self.table[measure] = []
        pass

    def get_cell(self,prob,measure):
        return self.table[measure][self.problem_indices[prob]]

    def get_column(self,measure):
        if measure in self.measure_names:
            return numpy.array(self.table[measure])
        return None

    def add_problem_measures(self,problem,measure_values):
        self.problem_indices[problem] = len(self.problem_indices)
        for measure in self.measure_names:
            self.table[measure].append(measure_values[measure])
        return

    def clear(self):
        for measure in self.measure_names:
            del self.table[measure]
            self.table[measure] = []
        return

    def __string__(self):
        return ""
    