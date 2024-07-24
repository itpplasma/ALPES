
def pressureDrop(pipeInnerDiam, massFlow, length, roughness = 0.000005): #m , kg/s , m returns in bar
    import pressure_loss_calculator.PressureLossMod as PL
    roughness = roughness*1000 #convert m to mm
    pipeInnerDiam = pipeInnerDiam/0.001
    return(PL.PressureLoss_DW(length, pipeInnerDiam, massFlow, 20, roughness)) #fixed at 20°C and roughness of 5um

if __name__ == '__main__':
    print(pressureDrop(4*0.001, 0.1,10))