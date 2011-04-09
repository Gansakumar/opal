# Define a parameter optimization problem in relation to the TRUNK solver.
# This is the sequential version.
from trunk_declaration import trunk
from opal import ModelStructure, ModelData, Model
from opal.Solvers import NOMAD
from opal.TestProblemCollections import CUTEr

def sum_heval(parameters, measures):
    return sum(measures["HEVAL"])

def get_error(parameters,measures):
    return sum(measures['ECODE'])

# Parameters being tuned and problem list.
par_names = ['eta1', 'eta2', 'gamma1', 'gamma2', 'gamma3']
params = [param for param in trunk.parameters if param.name in par_names]

problems = [problem for problem in CUTEr if problem.name in ['BDQRTIC',
                                                             'BROYDN7D',
                                                             'BRYBND',
#                                                             'CURLY10',
#                                                             'CURLY20',
#                                                             'CURLY30',
#                                                             'CRAGGLVY',
#                                                             'DIXON3DQ',
#                                                             'EIGENALS',
#                                                             'FMINSRF2',
#                                                             'FMINSURF',
#                                                             'GENROSE',
                                                             'HIELOW',
#                                                             'MANCINO',
#                                                             'NCB20',
#                                                             'NCB20B',
#                                                            'NONDQUAR',
                                                             'POWER',
                                                             'SENSORS',
                                                             'SINQUAD',
                                                             'TESTQUAD',
                                                             'TRIDIA',
                                                             'WOODS']]

# Define (constrained) parameter optimization problem.
data = ModelData(algorithm=trunk,
                 problems=problems,
                 parameters=params)
struct = ModelStructure(objective=sum_heval,
                        constraints=[(None,get_error, 0)])
model = Model(modelData=data, modelStructure=struct)

# Define a surrogate (unconstrained).
surr_data = ModelData(algorithm=trunk,
                      problems= [problem for problem in CUTEr \
                                     if problem.name in ['BDQRTIC',
                                                         'BROYDN7D',
                                                         'BRYBND']],
                      parameters=params)
surr_struct = ModelStructure(objective=sum_heval)
surr_model = Model(modelData=surr_data, modelStructure=surr_struct,
                   dataFile='surrogate.dat')

# Solve parameter optimization problem.
NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
NOMAD.set_parameter(name='DISPLAY_STATS',
                    value='%3dBBE [ %7.1eSOL, ]  %8.3eOBJ  %6.2fTIME')
NOMAD.solve(blackbox=model, surrogate=surr_model)
