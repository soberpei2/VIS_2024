import mbsObject as mbsObj

class solver(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"solver","",input,[])
        else:
            parameter = {
                "SimulationTimeBegin": {"type":"float", "value":1.},
                "SimulationTimeEnd": {"type":"float", "value":1.},
                "OutputTimeBegin": {"type":"float", "value":1.},
                "OutputTimeStepSize": {"type":"float", "value":1.},
                "SimulationMinTimeStep": {"type":"float", "value":1.},
                "SimulationMaxTimeStep": {"type":"float", "value":1.},
                "isExactOutputTimeEnforced": {"type":"boolean", "value":False},
                "WriteConstraintForceResultFile": {"type":"boolean", "value":False},
                "WriteForceResultFile": {"type":"boolean", "value":False},
                "WriteStateResultFile": {"type":"boolean", "value":False},
                "WriteVelocityResultFile": {"type":"boolean", "value":False},
                "WriteAccelerationResultFile": {"type":"boolean", "value":False},
                "WriteExtConstraintLagrangeResultFile": {"type":"boolean", "value":False},
                "WriteMeasureResultFile": {"type":"boolean", "value":False},
                "DebugLevel": {"type":"int", "value":1},
                "DebugTimeBegin": {"type":"float", "value":1.},
                "DebugTimeEnd": {"type":"float", "value":1.},
                "useSimTimeInterval": {"type":"boolean", "value":False},
                "IsInitialPositionFromFileUsed": {"type":"boolean", "value":False},
                "IsInitialVelocityFromFileUsed": {"type":"boolean", "value":False},
                "Alpha": {"type":"float", "value":1.},
                "MaxNumberOfInnerIterations": {"type":"vec2D", "value":[0,0]},
                "GlobalErrorTolerance": {"type":"float", "value":1.},
                "ModifyNewmark": {"type":"boolean", "value":False},
                "MaxNumOfTimeStepsUsingSameFactorizedJacobian": {"type":"int", "value":0},
                "UsePardisoScalingAndMatching": {"type":"boolean", "value":False}
                }

            mbsObj.mbsObject.__init__(self,"solver","",input,parameter)