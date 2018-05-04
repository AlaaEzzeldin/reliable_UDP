'''protocol_type = input("specify your protocol(SAW,GBN or SR)")
print("Selected protocol is : ", protocol_type)
'''
protocol_type = "sr"

file_path = "C:\\Files\\Engineering\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files\\log_file.txt"
log_file = open(file_path, "w")


def write_log(event):
    log_file = open(file_path, "a")
    log_file.write(event + "\n")
    print(event)
    return 1
