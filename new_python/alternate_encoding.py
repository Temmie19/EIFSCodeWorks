#!/usr/bin/python3

def escape_encoding(input):
    chunks = len(input) // 1024
    print("Chunks", chunks)
    escaped = ""
    for i in range(chunks):
        escaped += actual_escaping(input[i*1024:(i+1)*1024])
        pass
    escaped += actual_escaping(input[chunks*1024:])
    print()
    print((1 - (len(input) / len(escaped)))*100, "total %", "increase in size")
    print("Original size: ", len(input), " VS new size: ", len(escaped))
    return escaped

def actual_escaping(input):
    order = str(sorted(input))
    escaped_characters = [chr(10), chr(11), chr(12)]
    for i in range(len(escaped_characters)):
        order = order[:order.find(escaped_characters[i])] + \
                order[order.rfind(escaped_characters[i])+1:]
    convenient_dict = {}
    current_char = order[0]
    current_count = 0
    for i in range(len(order)):
        if(order[i] == current_char):
            current_count += 1
        else:
            convenient_dict[current_char] = current_count
            current_count = 0
            current_char = order[i]
    least_occuring = list(convenient_dict.keys())[min(convenient_dict.values())]
    #print("Least occuring character is: ", least_occuring)
    escape_one = least_occuring + "1"
    escape_two = least_occuring + "2"
    escape_three = least_occuring + "3"
    escape_four = least_occuring + "4"
    escaped_message = least_occuring
    for i in range(len(input)):
        if(input[i] == chr(10)):
            escaped_message += escape_one
        elif(input[i] == chr(11)):
            escaped_message += escape_two
        elif(input[i] == chr(12)):
            escaped_message += escape_three
        elif(input[i] == least_occuring):
            escaped_message += escape_four
        else:
            escaped_message += input[i]
    escaped_message += least_occuring + "5"
    #print("Original size: ", len(input), " VS new size: ", len(escaped_message))
    #print((1 - (len(input) / len(escaped_message)))*100, "%", "increase in size")
    return escaped_message


def escape_decoding(input:str):
    escape = input[0]
    converted = ""
    flagged = False
    checker = False
    chunks = []
    escape_location = 0
    for i in range(len(input)):
        if(checker == True):
            #print("Found escape at", i)
            escape_location = i
            escape = input[i]
            checker = False
        elif(input[i] == escape):
            flagged = True
            #print("Found escape at", i)
        elif(flagged == True):
            if(input[i] == "5"):
                #print("Found EoC at", i)
                chunks.append(input[escape_location:i+1])
                checker = True
            flagged = False
    print("Length of chunks: ", len(chunks))
    for i in range(len(chunks)):
        converted += actual_decoding(chunks[i])
    return converted

def actual_decoding(input:str):
    escape = input[0]
    input = input[1:]
    unescaped = ""
    flagged = False
    for i in range(len(input)):
        if(input[i] == escape):
            flagged = True
        elif(flagged == True):
            if(input[i] == "1"):
                unescaped += chr(10)
            elif(input[i] == "2"):
                unescaped += chr(11)
            elif(input[i] == "3"):
                unescaped += chr(12)
            elif(input[i] == "4"):
                unescaped += escape
            flagged = False
        else:
            unescaped += input[i]
    return unescaped