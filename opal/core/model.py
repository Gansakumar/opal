from tempfile import NamedTemporaryFile
import pickle
import log
import os

__docformat__ = 'restructuredtext'

class Model:

    def __init__(self, modelData=None, modelStructure=None,
                 dataFile='blackbox.dat', logHandlers=[], **kwargs):
        """
        A `BlackBoxModel` encapsulates the
        information of a parameter optimization problem.
        From the parameter problem point of view, this class has
        two components: model data and model struture.

        Example::

            model = Model(modelStructure, modelData)

        An object of this class must contain a link to a solver.
        The link to a solver is created by the solver and added to the
        Model object upon solving the problem.
        """

        self.model_data = modelData
        self.model_structure = modelStructure
        #self.data_file = dataFile
        self.logger = log.OPALLogger(name='Model',
                                     handlers=logHandlers)
        self.logger.log('Initializing Model object')

        self.variables = self.model_data.get_parameters()
        self.n_var = len(self.variables)

        self.n_real        = len([p for p in self.variables if p.is_real])
        self.n_integer     = len([p for p in self.variables if p.is_integer])
        self.n_binary      = len([p for p in self.variables if p.is_binary])
        self.n_categorical = len([p for p in self.variables if p.is_categorical])

        # Compute number of constraints in form c(x) <= b
        # from the constraints of form l <= c(x) <= u
        self.m_con = 0
        for cons in self.model_structure.constraints:
            self.m_con = self.m_con + cons.n_size

        self.initial_point = [param.value for param in self.variables]
        self.bounds = [param.bound for param in self.variables]

        # Simple constraints are only functions of the parameters and not of
        # compound measures. Their satisfaction is checked before evaluating
        # the compound measures.
        self.simple_constraints = []

        # Dump this very object to disk.
        self.save()
        return


    def evaluate(self, inputValues):
        """
        Evaluate the model at given point
        Input: evaluated point coordinate
        Output: Value of objective function and constrains values list
        In the case of error, two None values are returned
        """

        self.logger.log('Begin a blackbox evaluation')
        self.model_data.run(inputValues)
        testResult = self.model_data.get_test_result()
        (funcObj, constraints) = self.model_structure.evaluate(testResult)
        self.logger.log('End of blackbox evaluation\n')
        return (funcObj, constraints)


    def save(self):

        self.logger.log('Dumping model object to file')
        #blackboxDataFile = open(self.data_file, "w")
        blackboxDataFile = NamedTemporaryFile(mode="w", delete=False)
        pickle.dump(self, blackboxDataFile)
        self.data_file = blackboxDataFile.name
        blackboxDataFile.close()
        return


    def get_initial_point(self):

        self.logger.log('Requesting initial point')
        return self.initial_point


    def get_bound_constraints(self):

        self.logger.log('Requesting bound constraints')
        return self.bounds


    def __del__(self):

        # Delete temporary data file.
        self.logger.log('Deleting temp file')
        os.remove(self.data_file)
