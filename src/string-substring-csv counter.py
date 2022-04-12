import csv
dictionary = {
}
with open('/home/mhdfadlyhasan/Codes/dronetimeline/src/hasilfinal.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    next(csv_reader)
    for row in csv_reader:
        # message
        string = row[10].split(' ')
        for x in string:
            dictionary[x] = 0
                


with open('/home/mhdfadlyhasan/Codes/dronetimeline/src/hasilfinal.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        string = row[10].split(' ')
        for x in string:
            dictionary[x] += 1


with open('filewriter.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    for i in dictionary:
        writer.writerow([i, dictionary[i]])

print("done")
    


