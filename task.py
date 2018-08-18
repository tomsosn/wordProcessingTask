import csv
import string
import re

def get_dictionary():
    dictionary = []
    dictionary.append((-1,"^stycz(ni(a|u|em)|eń)$"))
    dictionary.append((-2,"^lut(ego|ym?)$"))
    dictionary.append((-3,"^mar(c(a|u|em)|zec)$"))
    dictionary.append((-4,"^kwie(tni(a|u|em)|cień)$"))
    dictionary.append((-5,"^maj(a|u|em)?$"))
    dictionary.append((-6,"^czerw(iec|c(a|u|em))$"))
    dictionary.append((-7,"^lip(iec|c(a|u|em))$"))
    dictionary.append((-8,"^sierp(ień|ni(a|u|em))$"))
    dictionary.append((-9,"^wrze(sień|śni(a|u|em))$"))
    dictionary.append((-10,"^październik(a|u|iem)?$"))
    dictionary.append((-11,"^listopad(a|zie|em)?$"))
    dictionary.append((-12,"^grud(zień|ni(a|u|em))$"))
    dictionary.append((0,"^zero$"))
    dictionary.append((1,"^pierwsz(ym?|ego)|jeden$"))
    dictionary.append((2,"^drugi(m|ego)?|dw(a|u)$"))
    dictionary.append((3,"^trzeci(m|ego)?|trzy$"))
    dictionary.append((4,"^czwart(ym?|ego)|cztery$"))
    dictionary.append((5,"^piąt(ym?|ego)|pięć$"))
    dictionary.append((6,"^szóst(ym?|ego)|sześć$"))
    dictionary.append((7,"^siódm(ym?|ego)|siedem$"))
    dictionary.append((8,"^ósm(ym?|ego)|osiem$"))
    dictionary.append((9,"^dziewiąt(ym?|ego)|dziewięć$"))
    dictionary.append((10,"^dziesiąt(ym?|ego)|dziesięć$"))
    dictionary.append((11,"^jedenast(ym?|ego)|jedenaście$"))
    dictionary.append((12,"^dwunast(ym?|ego)|dwanaście$"))
    dictionary.append((13,"^trzyna(ście|st(ym?|ego))$"))
    dictionary.append((14,"^czterna(ście|st(ym?|ego))$"))
    dictionary.append((15,"^piętna(ście|st(ym?|ego))$"))
    dictionary.append((16,"^szesna(ście|st(ym?|ego))$"))
    dictionary.append((17,"^siedemna(ście|st(ym?|ego))$"))
    dictionary.append((18,"^osiemna(ście|st(ym?|ego))$"))
    dictionary.append((19,"^dziewiętna(ście|st(ym?|ego))$"))
    dictionary.append((20,"^dwudziest(ym?|ego)|dwadzieścia$"))
    dictionary.append((30,"^trzydzie(ści|st(ym?|ego))$"))
    dictionary.append((40,"^czterdzie(ści|st(ym?|ego))$"))
    dictionary.append((50,"^pięćdziesiąt(ym?|ego)?$"))
    dictionary.append((60,"^sześćdziesiąt(ym?|ego)?$"))
    dictionary.append((70,"^siedemdziesiąt(ym?|ego)?$"))
    dictionary.append((80,"^osiemdziesiąt(ym?|ego)?$"))
    dictionary.append((90,"^dziewięćdziesiąt(ym?|ego)?$"))
    dictionary.append((100,"^sto|setn(ym?|ego)$"))
    dictionary.append((200,"^dwieście|dwusetn(ym?|ego)$"))
    dictionary.append((300,"^trzys(ta|etn(ym?|ego))$"))
    dictionary.append((400,"^czterys(ta|etn(ym?|ego))$"))
    dictionary.append((500,"^pięćset(n(ym?|ego))?$"))
    dictionary.append((600,"^sześćset(n(ym?|ego))?$"))
    dictionary.append((700,"^siedemset(n(ym?|ego))?$"))
    dictionary.append((800,"^osiemset(n(ym?|ego))?$"))
    dictionary.append((900,"^dziewięćset(n(ym?|ego))?$"))
    dictionary.append((1000,"^tysiąc$"))
    dictionary.append((-1000,"^tysi(ące|ęczn(y|ego))$"))
    dictionary.append((2000,"^dwutysięczn(ym?|ego)$"))
    return dictionary
    
def get_compiled_dictionary():
    dictionary = get_dictionary()
    return [(entry[0],re.compile(entry[1])) for entry in dictionary]

def split_into_words(text):
    return [word.strip(string.punctuation).lower() for word in text.split()]
    
def convert_to_numbers(words):
    numbers = []
    dictionary = get_compiled_dictionary()
    for word in words:
        for entry in dictionary:
            if entry[1].match(word):
                numbers.append(entry[0])
                break
    return numbers
    
def extract_date(numbers):
    trailing_thousand = -1000
    if trailing_thousand in numbers:
        index = numbers.index(trailing_thousand)
        numbers[index-1] *= 1000
        del numbers[index]
    
    # first we want to extract year, then the rest is simple
    year_list = []
    hundreds_and_thousands = [x for x in numbers if x >= 100]
    year_index = 0
    if len(hundreds_and_thousands) > 0: # check whether year conveniently begins with hundreds or thousands
        year_index = numbers.index(hundreds_and_thousands[0])
    else: # if not, we must find the beginning of the year in a more convoluted way
        # we can assume, that the last two digits enode the year
        if numbers[-1] >= 10:
            year_index = -1
        else:
            year_index = -2
        if (abs(numbers[year_index - 1]) > 12): # but we must check too whether the number before last two digits is also part of the year, or a month. Here I assumed that everything greater than 12 must be a year. 
            year_index -= 1

    year_list = numbers[year_index:]
    numbers = numbers[:-len(year_list)]

    threshold = 1
    if year_list[-1] >= 10:
        threshold = 10
    for i in reversed(range(0,len(year_list))):
        if year_list[i] < threshold:
            year_list[i] *= threshold
        threshold *= 10
    
    year = sum(year_list)
    
    if year < 100:
        year += 1900
        
    month = abs(numbers[-1])
    numbers = numbers[:-1]
    
    day = sum(numbers)
    
    return {"day": day, "month": month,"year": year}

def date_recognition(text):
    words = split_into_words(text)
    numbers = convert_to_numbers(words)
    date = extract_date(numbers)
    return date

def judge(filename):
    file = open(filename,"rb")
    reader = csv.reader(file)
    rownum = 0
    correct = 0
    for row in reader:
        if rownum != 0:
            date = {"day": int(row[0]),"month": int(row[1]),"year": int(row[2])}
            text = row[3]
            print "\n" + text
            print "expected: " + str(date)
            answer = date_recognition(text)
            print "got: " + str(answer)            
            if answer == date:
                correct += 1
                print "Correct!"
            else:
                print "Wrong!"
        rownum += 1
    file.close()
    print "\nCorrect: "+str(correct)+"/"+str(rownum-1)