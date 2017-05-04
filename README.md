# 11791

General Q & A:

1. how to run the web service:

go to the diretory  /home/791/team2spring2017/11791
please kill any process that may occupy the port, then run the command:

nohup python web_service.py &

nohup python pipeline.py &


2. how to Run the batch evaluation script to get the result: 

go to the diretory  /home/791/team2spring2017/11791
then run the batch script with command:

./evaluation.sh

Note: we provide automatic evaluation script that all of the argument are already provided in the script,
you can modified the script to modified the amount of data been tested.

The output will be store at output103.txt  with csv file format.

3. how get the predicted answer of an specific question in SQUARD format?

We support the SQUARD format, the user can extract our predicted result by running our script,
The script can be run by the following command 

java -Xmx4G -jar lsd-2.2.3.jar pipeline.lsd 123

Where 123 is the row num of question, you can change the number to whatever row num you want to predict,
the output will be a json format, for example:

{
  "56bf3c633aeaaa14008c9581": "'s Levi 's Stadium"
}

