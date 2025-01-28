import numpy as np
from scipy import stats

class RiskMeasure:
    def __init__(self):
        self._nonParametric = self.NonParametric()
        self._parametric = self.Parametric()
        print('Hello my first oop')

    class Parametric:
        def __init__(self, distribution):
            self._distribution = distribution # get a distribution from scipy.stats

        def CDF(self, x):
            return self._distribution.cdf(x)

        def valueAtRisk(self, alpha=0.05, **kwargs):
            distribution = self._distribution
            valueAtRisk = distribution.ppf(q=alpha,**kwargs)
            return valueAtRisk
        
        def expectedShortfall(self, alpha=0.05, **kwargs):
            distribution = self._distribution
            valueAtRisk = self.valueAtRisk(alpha, **kwargs)

            if isinstance(distribution, stats.rv_discrete):
                firstTerm = distribution.expect(lambda x: -x, ub=valueAtRisk, conditional=True, args=(kwargs.values()) ) # mind the order of value in "**kwargs"
            else: firstTerm = distribution.expect(lambda x: -x, ub=valueAtRisk, conditional=True, **kwargs ) # Thanks to an amazing library - scipy
            alphaHat = 1 - distribution.cdf(distribution.ppf(1-alpha,**kwargs ),**kwargs )
            secondTerm = -valueAtRisk*( alphaHat - alpha )
            
            expectedShortfall = -(firstTerm + secondTerm)
            return expectedShortfall





    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    class NonParametric:
        def __init__(self, data):
            self._data = data

        def CDF(self, x):
            data = np.array(self._data)
            sortedData = np.sort(data)

            arangeData = np.arange(len(data))
            percentileSortedData = arangeData/(len(data)-1) # len(data) - 1 because we count the first sample as the 0th percentile
            
            if max(sortedData) <= x:
                position = 1.0

            elif min(sortedData) > x:
                position = 0.0

            else:
                for i in range(1, len(data) + 1):
                    if (sortedData[i] > x): # This condition checks the next position
                        partialPart = (x-sortedData[i-1])/(sortedData[i] - sortedData[i-1])*(percentileSortedData[i] - percentileSortedData[i-1]) # assume that the risk between two samples is linear
                        integerIndex = i - 1
                        position = percentileSortedData[integerIndex] + partialPart
                        break
                    
                    elif (sortedData[i] == x) & (sortedData[i+1] != sortedData[i]): # This condition checks this exact position
                        integerIndex = i
                        position = percentileSortedData[integerIndex]
                        break

            CDF = position
            return CDF
        
        def valueAtRisk(self, alpha):
            data = np.array(self._data)
            sortedData = np.sort(data)
            
            arangeData = np.arange(len(data))
            percentileSortedData = arangeData/(len(data)-1)

            if max(percentileSortedData) <= alpha: # max(percentileSortedData) is 1
                integer = len(data) - 1
                partial = 0
                sortedData = np.append(sortedData, sortedData[-1])

            elif min(percentileSortedData) >= alpha:
                integer = 0 # This is because we do not know the minimum value, so we assume that the minimum value is the smallest sample
                partial = 0

            else:
                for i in range(1,len(data)):
                    if (percentileSortedData[i] > alpha):
                        partial = (alpha-percentileSortedData[i-1])/(percentileSortedData[i] - percentileSortedData[i-1]) # assume that the risk between two samples is uniform
                        integer = i - 1
                        break
                    
                    elif (percentileSortedData[i] == alpha):
                        integer = i 
                        partial = 0
                        break

            valueAtRisk = sortedData[integer] + (sortedData[integer + 1] - sortedData[integer]) * partial
            return valueAtRisk

        def expectedShortfall(self, alpha):
            data = np.array(self._data)
            sortedData = np.sort(data)

            valueAtRisk = self.valueAtRisk(alpha)

            probLeftRisk = len(sortedData[sortedData <= valueAtRisk])/len(sortedData)
            for i in range(1,len(sortedData)):
                if (sortedData[i] > valueAtRisk):
                    partialProbLeftRisk = (valueAtRisk - sortedData[i-1])/(sortedData[i] - sortedData[i-1]) * ( 1 / len(sortedData) )
                    partialProbRightRisk = (sortedData[i] - valueAtRisk)/(sortedData[i] - sortedData[i-1]) * ( 1 / len(sortedData) )
                    break
                
                elif (sortedData[i] == valueAtRisk):
                    partialProbLeftRisk = 0
                    partialProbRightRisk = 0
                    break
                
            numerator = (-np.sum(sortedData[sortedData <= valueAtRisk])/len(sortedData) - (valueAtRisk * partialProbRightRisk) ) + ( valueAtRisk * ( (probLeftRisk + partialProbLeftRisk) - alpha ) )
            return -numerator/(alpha)

