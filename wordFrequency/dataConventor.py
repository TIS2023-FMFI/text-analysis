def queryModuleToBarChartMap(data):
    data ={"-".join(row[:-1]):row[-1] for row in data}
    return data

def queryModuleToListOfSet(data):
    data =[{"word "+str(index) :word
            for index,word in enumerate(row[:-1],1)}|
           {"frequency":row[-1]} for row in data]
    return data


if __name__ == "__main__":
    data=[["text1","text2",1],["text2","text3",2]]
    print(queryModuleToBarChartMap(data))
    print(queryModuleToListOfSet(data))

    data=[["text1",1],["text2",2]]
    print(queryModuleToBarChartMap(data))
    print(queryModuleToListOfSet(data))