__author__ = 'Matt'

import math
import matplotlib.pyplot as plt

def calculateQ(innerRad,outerRad,gasTemp,outerTemp,k):
    return 2*math.pi*k*(gasTemp - outerTemp)/float(math.log(innerRad/float(outerRad)))

def calculateSpecificHeat(gasTemp,relativeHumidity):
    #  h = h(a) + xh(w)   h(a) = Enthalpy of dry air.  h(w) = Enthalpy of water vapour.  x = Specific humidity = relative humidity * xs.
    return 419*math.pow(10,3) + relativeHumidity*saturationPressure(gasTemp)*51.126*math.pow(10,3)

def saturationPressure(gasTemp):
    #  p(ws) = exp(77.345 + 0.0057*tmp - 7235/tmp)/tmp^8.2  tmp = temperature  p(ws) Saturation pressure.
    #  http://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
    gasTemp = gasTemp + 273
    satPres = (math.exp(77.345 + 0.0057*gasTemp - (7235/float(gasTemp))))/float(math.pow(gasTemp,8.2))
    return satPres

def densityOfWaterVapour(partialPressure,absoluteTemp,relativeHumidity):
    #  densitiyOfWaterVapour = (pressure/Ra*T)(1+x)/(1 + x*Rw/Ra)
    #  Convert to kelvin
    #  http://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
    Ra = 286.9
    Rw = 461.5
    x = specificHumidity(absoluteTemp, relativeHumidity)
    return (partialPressure/(Ra*(absoluteTemp+273)))*(1+x)/(1+x*(Rw/Ra))

def specificHumidity(absoluteTemp,relativeHumidity):
    # x = 0.62198 pw / (pa - pw)
    pa = 101325  #  Atmospheric pressure.
    pw = partialPressureWaterVapour(absoluteTemp,relativeHumidity)
    return 0.62198*pa/(pa-pw)

def partialPressureWaterVapour(absoluteTemp, relativeHumidity):
    saturationVapourPartialPressure = saturationPressure(absoluteTemp)
    p = (relativeHumidity/float(100))*saturationVapourPartialPressure
    return p


def calculateMassOfWaterVapour(density,diameter,length):
    #  density = mass/volume  thus mass = density*volume
    volume = math.pi*(diameter/float(2))*(diameter/float(2))*length
    return density*volume

def specificHumidityAtSaturation(temp):
    #  saturationPressure = 0.62198*satPressure/(atmosPressureofMoistAir-satPressure)
    #  http://www.engineeringtoolbox.com/humidity-ratio-air-d_686.html
    satPress = saturationPressure(temp)
    #  At sea level.  Assuming the VNB lab is at that condition.
    atmosPress = 101325
    return 0.62198*satPress/float(atmosPress-satPress)

def calculateChangeInTemp(innerR,outerR,gasTemp,outerSurfaceTemp,k,length,relativeHumidity):
    #  dt =gasTemp - mcQ*length
    partialPressure = relativeHumidity*specificHumidityAtSaturation(gasTemp)
    density = densityOfWaterVapour(partialPressure,gasTemp,relativeHumidity)
    mass = calculateMassOfWaterVapour(density,innerR,length)
    Q = calculateQ(innerR,outerR,gasTemp,outerSurfaceTemp,k)
    C = calculateSpecificHeat(gasTemp,relativeHumidity)
    #print "Q = " + str(Q)
    #print "Mass = " + str(mass)
    #print "C = "+ str(C)
    dt = (Q/(mass*C))*length
    #print dt
    return dt

def main():
    ambientTmp = 37
    gasTmp = 50
    length = 1
    numSteps = 10000
    tmp = []
    dT = []
    distance = []
    dist = 0
    a = 2
    if a == 1:
        for i in range(0,numSteps):
            distance.append(dist)
            dist = dist + length/float(numSteps)
        for j in range(37,50,1):
            tmp = []
            dT = []
            gasTmp = j
            for i in distance:
                tmp.append(gasTmp)
                dt = calculateChangeInTemp(0.004,0.006,gasTmp,ambientTmp,0.02,length/float(numSteps),80)
                gasTmp = gasTmp + dt
                dT.append(dt)
           #print distance
           #print tmp
            plt.figure(1)
            plt.subplot(211)
            plt.plot(distance,tmp)

            plt.subplot(212)
            plt.plot(distance,dT)
    #a = 2
    if a == 2:
        num_divs = [10,100,1000,10000,100000]
        for j in num_divs:
            distance = []
            dist = 0
            for i in range(0,j+1):
                distance.append(dist)
                dist = dist + length/float(j)
            tmp = []
            dT = []
            for i in distance:
                dt = calculateChangeInTemp(0.004,0.006,gasTmp,ambientTmp,0.02,length/float(j),80)
                gasTmp = gasTmp + dt

                tmp.append(gasTmp)
                dT.append(dt)

            plt.figure(1)
            plt.subplot(211)
            plt.plot(distance,tmp)

            plt.subplot(212)
            plt.plot(distance,dT)
    plt.show()

if __name__ == '__main__':
    main()