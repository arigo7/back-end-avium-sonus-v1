# Function for parsing BirNET's output text file
# Add parsing of file here  - using json module

# 1st import json module
import json 
from pprint import pprint

def get_file_name(audio_file):
    '''
    input: Takes in sound_file ext .wav or m4p
    output: returns same name with new extension as birdnet processes it
    '''
    new_ext = '.BirdNET.selections.txt'
    txt_filename = (audio_file.rsplit('.', 1)[0]) + new_ext
    return txt_filename


def parse_output_file(txt_filename):
    '''
    input: takes in text file 
    output: parses every row of file except for the first row (assumes 
    that firs row is a titles row) into a dictionary), maps each dictionary
    into a final dictionary that becomes a json object for returning a 
    response
    '''
    # dict_1 = {}
    birds = []
    path = '/Users/ada/Developer/projects/capstone/BirdNET/outputs/'
    filename = path + txt_filename
    print(filename)
    dic_fields = ['id', 'view', 'channel', 'beginFile', \
        'beginTimeSec', 'endTimeSec','lowFreqHz','highFreqHz', \
            'speciesCode','commonName', 'confidence', 'rank']
    
    with open(filename) as file:

        l = 0
        for line in file:
            if l != 0:
                # reading line by line from the text file
                description = list(line.strip().split('\t', 12))

                # start/end of interval(sec) to int for results
                description[4] = round(float(description[4]))
                description[5] = round(float(description[5]))
                description[10] = round(float((description[10])), 2)

                
                # pprint(description[10])

                print(description)
                # for automatic creation of id for each bird
                # bird ='bird'+ str(l)
            
                # loop variable
                i = 0
                # intermediate dictionary for each line of output txt file
                dict_2 = {}

                while i < len(dic_fields):
                    
                    

                        # creating dictionary for each bird
                        dict_2[dic_fields[i]]= description[i]
                        i = i + 1
                        
                # appending the record of each bird to the main dictionary
                # dict_1[bird]= dict_2

                # make dictionary of append only birds ranked #1 only birds per interval
                if dict_2['rank'] == '1':
                    birds.append(dict_2) 
            l = l + 1

    
    # # birds as a list of dictionaries ---- original no sorting!

    # # creating json file for return format      
    # out_file = open("test2.json", "w")  # in the directory outputs
    # # json.dump(dict_1, out_file, indent = 4)
    # json.dump(birds, out_file, indent = 4)
    # out_file.close()
    # # return dict_1
    # return birds


    # birds as a list of dictionaries ------ trial one sort by beginTimeSec
    sorted_list = sorted(birds, key=lambda k: k['beginTimeSec'])
    # this is printing  and not sorting, maybe due to it being a string?
    pprint(sorted_list)

    # creating json file for return format      
    out_file = open("test2.json", "w")  # in the directory outputs
    # json.dump(dict_1, out_file, indent = 4)
    # json.dump(birds, out_file, indent = 4)

    json.dump(sorted_list, out_file, indent = 4)
    out_file.close()
    # return dict_1
    return sorted_list


    # # # birds as a list of dictionaries --- n trial two

    # # creating json file for return format      
    # out_file = open("test2.json", "w")  # in the directory outputs
    # # json.dump(dict_1, out_file, indent = 4)
    # json.dump(birds, out_file, indent = 4)
    # out_file.close()
    # # return dict_1

    # sorted_list = sorted(birds, key=lambda k: k['beginTimeSec'])
    

    # return birds



## TESTING IT WORKS

# fullpath = f"/Users/ada/Developer/projects/capstone/BirdNET/outputs/{get_file_name('Soundscape_1.wav')}"
# print(fullpath)
# with open(fullpath) as fh:
#     print(fh.read())
# from pprint import pprint
# results_json = parse_output_file(get_file_name('Soundscape_1'))
# pprint(results_json)  
            

