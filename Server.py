

# reading input file
server_input_file = open("Data_files\server_input.txt", "r")
Input_list = server_input_file.read().splitlines()
server_port = int(Input_list[0])
Max_sending_window_size = Input_list[1]
Random_SeedValue = Input_list[2]
loss_Probability = Input_list[3]
print("server input file:", "server_port", server_port, ",Max_sending_window_size:", Max_sending_window_size,
      ",Random_SeedValue:", Random_SeedValue, ",loss_Probability:", loss_Probability)

