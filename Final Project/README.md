# Implementation of Secure and controllable k-NN query over encrypted cloud data with key security

### Assumptions made in the implementation:

1. **c** is a random integer between 1 and 10
2. **e** is a random integer between 1 and 10
3. **M** contains positive integers between 1 and 5 -- initialized with small values for exponentiation
4. **v** is a random e dimensional vector where each coordinate is a floating point number in the range [0,1000]. Used for encryption of database
5. **R_q** is a random c dimensional vector where each coordinate is an integer between 1 and 100. Used in the computation of A_q
6. **beta_q** is a random integer between 1 and 100. Used in the computation of A_q
7. Negative Number handling : The negative coordinates in the Database as well as the query are overwritten by *|p|+10000*.
   This effectively maps our coordinates from [-10000,10000] to [0,20000]. This results in no change in Euclidean distances between the query and the datapoints

### Runtime Instructions:

The programs must be executed in the following order:
<br>cloud_server.py -> data_owner.py -> query_user.py

#### Steps to be followed:

1. To set up the Cloud Server run the following lines in powershell in the directory "Final Project"
    <br>*docker build -t cloud-server .*
    <br>*docker run -p 65433:65433 cloud-server*

2. Now in 2 separate terminals open **sagemath environment** in the directory "Final Project". This can be done
by running the command *sage* in the **wsl terminal**

3. Run the file "data_owner.py" in one of the terminals.
    <br>*load("data_owner.py")*

4. Wait until you see "[CLOUD SERVER]Encrypted query - q_dash Received" message in the Cloud Server's terminal
   Run the file "query_user.py" in one of the terminals.
    <br>*load("query_user.py")*

If everything has worked successfully you should see "Index Set : [3]" Message in the query user's terminal

#### Parameters that can be changed :
1. Query - You can input a query of your choice in lines 126-129 of "query_user.py"
2. K - You can select your k for kNN computation in line 118 of "cloud_server.py"
3. You can generate a new "database.txt" file using the "data_gen.py" file. Although I have provided an example database already.
