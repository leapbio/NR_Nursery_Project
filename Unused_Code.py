""" 

def concatenate (file, geojson):
    with open(file, 'r+') as jsfile:
        lines = jsfile.readlines()
        addData = "\n{" + str(geojson) + ",\n"
        lines.insert(68, addData) #This number will be 79 in the production version
        return lines
    #print (lines) """


""" def concatenate (file, geojson):
    with open(file, 'r+') as jsfile:
        data = jsfile.readlines()
        addData = "\n{" + str(geojson) + ",\n"
        print(addData)
        print ("ADDDATA---------------------------------------------------------------------------------------------------------------------------------------------------")
        data = data.append(addData)
        print (data)
        print ("APPENDEDDATA---------------------------------------------------------------------------------------------------------------------------------------------------")
        jsstring = json.dumps(data)
        print (type(jsstring))
        return jsstring
 """
newFile = []


def concatenate (file, geojson):
    with open(file, 'r+') as jsfile:
        
        newFile = jsfile.readlines()
        print(newFile)
        return newFile

print (newFile)


print ("---------------------------------------------------------------------------------------------------------------------------------------------------END")


a = concatenate(r"C:\Users\itj\Desktop\Visual_Studio_Code\NR_Nurseries\Nursery_Concatenate_Test.txt", geojson)
print(a)


geojsonString = ''.join(a)
#print(geojsonString) # This is just the lines not the file itself I think?
#Should I pull the data modify it and then stick it back in the file or modify the file directly?
print ("---------------------------------------------------------------------------------------------------------------------------------------------------END")
#print (json.dumps(geojsonString))


""" 
with open("native_nurseries_leap.js", 'r') as newFile:
    parsed = json.load(newFile)


print (json.dumps(parsed, indent =2, sort_keys = True))
 """

 
with open('native_nurseries_leap.js', 'r') as jsonfile:
    read1 = jsonfile.readlines()
    parsed = json.loads(read1)
    print (json.dumps(parsed, indent=2, sort_keys=True))
