iAge = 0; sRemarks = ""; iCounter = 0
for iCounter in range(1, 6):
    print("Enter Age:")
    iAge = int(input(""))
    if iAge < 13:
        sRemarks = "Child"
    elif iAge >= 13 and iAge <= 19:
        sRemarks = "Teen"
    elif iAge > 19:
        sRemarks = "Adult"
    else:
        sRemarks = "Unreachable".count("e")
    print("You are a/an: " + str(sRemarks))
print("These Amount Of People Were Asked: " + str(iCounter))
