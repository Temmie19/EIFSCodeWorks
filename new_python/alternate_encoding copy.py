#!/usr/bin/python3

def escape_encoding(input):
    chunks = len(input) // 1024
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
    escape_five = least_occuring + "5"
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
    escaped_message += escape_five
    #print("Original size: ", len(input), " VS new size: ", len(escaped_message))
    #print((1 - (len(input) / len(escaped_message)))*100, "%", "increase in size")
    return escaped_message


def escape_decoding(input:str):
    shortened = input
    escape = input[0]
    start_of_chunk = 0
    print("Escape is: ", escape)
    end_of_chunk = shortened.find(str(escape + "5"))
    print("Chunk length is: ", end_of_chunk)
    converted = ""
    flagged = False
    operation_count = 1
    converted += actual_decoding(input[start_of_chunk:end_of_chunk])
    while(end_of_chunk != -1):
        start_of_chunk = end_of_chunk + 2
        end_of_chunk = input[start_of_chunk:].find(str(escape + "5"))
        print("End of chunk is at:", end_of_chunk)
        converted += actual_decoding(input[start_of_chunk:end_of_chunk])
        print("Operation ", operation_count)
    return converted

def actual_decoding(input:str):
    escape = input[0]
    sorted_string = str(sorted(input))
    amount_of_escapes = sorted_string.rfind(escape) - sorted_string.find(escape)
    for i in range(amount_of_escapes):
        location = input.find(escape)
        character_set = ""
        if(input[location+1] == "1"):
            character_set = chr(10)
        elif(input[location+1] == "2"):
            character_set = chr(11)
        elif(input[location+1] == "3"):
            character_set = chr(12)
        elif(input[location+1] == "4"):
            character_set = chr(13)
        input = input[:location] + character_set + input[location+2:]
    input = input[1:]
    return input