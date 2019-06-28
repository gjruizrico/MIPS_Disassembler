# -*- coding: utf-8 -*-
"""
CS472 Spring 2019 at Boston University - Project #1 
Deliverable by Guillermo Ruiz-Rico using Python 3.7.0 and Spyder as the IDE
"""
##################################### Step 1 - Set up variables and bitwise #####################################
Address = 0x9A040 #Part of the project's requirements
Instructions = [0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4, 0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0] #Part of the project's requirements.
# Funct (5:0) and Opcodes (31:26) as illustrated in pages 83, 85 and green sheet from the "Computer and Organization Design" book by Patterson & Hennessy
Functions = {32:"add", 34:"sub", 36:"and", 37:"or", 42:"slt"}
LoadStoreOperations = {35:"lw", 43:"sw"}
BranchesOperations = {4:"beq", 5:"bne"}
# Bitwise
Bitwise = {"OperationsCode":0b11111100000000000000000000000000,"Source1":0b00000011111000000000000000000000,"Source2":0b00000000000111110000000000000000,"Destination":0b00000000000000001111100000000000,"Offset":0b00000000000000001111111111111111,"Function":0b00000000000000000000000000111111}

##################################### Step 2 - Establish a for-loop to iterate through instructions and print output #####################################
for x in range(len(Instructions)):#For-loop starts here
    if x != 0:
        Address = Address+4
    FinalAddress = str(hex(Address))[2:8]
    RegisterSource1 = (Instructions[x] & Bitwise["Source1"]) >> 21
    RegisterSource2 = (Instructions[x] & Bitwise["Source2"]) >> 16
    InstructionsOperationCode = (Instructions[x] & Bitwise["OperationsCode"]) >> 26
    # Based on the Operations code, code proceeds down one of the below options using if statements
    if (InstructionsOperationCode == 0 and any(Instructions[x] & Bitwise["Function"] == item for item in Functions)):    
        print ("Instruction " +str(hex(Instructions[x])) + " corresponds to: " + FinalAddress.upper()+" "+str(Functions[Instructions[x] & Bitwise["Function"]])+" "+"$"+str((Instructions[x] & Bitwise["Destination"]) >> 11)+", $"+str(RegisterSource1)+", $"+str(RegisterSource2))  
    elif (any(InstructionsOperationCode == item for item in LoadStoreOperations)):
        Offset = Instructions[x] & Bitwise["Offset"]         
        if (Offset >> 15) == 1: #Verify whether it's a negative number
            Offset = abs(Offset) - 2**16
        print ("Instruction " +str(hex(Instructions[x])) + " corresponds to: " + FinalAddress.upper()+" "+LoadStoreOperations[InstructionsOperationCode]+", $"+str(RegisterSource2)+", "+str(Offset)+"($"+str(RegisterSource1)+")")    
    elif (any(InstructionsOperationCode == item for item in BranchesOperations)):
        Offset = (Instructions[x] & Bitwise["Offset"])
        Offset = Offset << 2 #This is specific to branches since the instructions were compressed. In this case, they need to be decompressed to obtain the relative offset
        Offset = Offset+4 #Increase as described on page 114: "MIPS Address is actually relative to the address of the following instruction PC+4"
        if (Offset >> 17) == 1: #Similar to the previous step for Load/Store only now it has 18 bits
            Offset = abs(Offset) - 2**18
        print("Instruction " +str(hex(Instructions[x])) + " corresponds to: " + FinalAddress.upper()+ " "+BranchesOperations[InstructionsOperationCode]+" $"+str(RegisterSource1)+", $"+str(RegisterSource2)+", address "+str(hex(Address + Offset)).upper()[2:8])       
    else:
        print ("Instructions "  +str(hex(Instructions[x])) + " is not part of this script's repertoire. Please try again.")