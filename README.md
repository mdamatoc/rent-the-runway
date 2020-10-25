# rent-the-runway

###**What Is This?**
This is a Python Project, using Hydra, intended to provide the answers of Multiplan's Data Engineer exam.

###**Required Softwares and Applications**
Pyenv 1.2.*  
Python 3.8.*   
Pip 19.2.*  


###**Requirements**
Create a virtual environment at the same folder of this project using _pyenv virtualenv 3.8.3 rent_the_runway_  
Activate the virtualenv environment using _pyenv local rent_the_runway_
The commands above can be substituted by any other virtual environment.    

Install the libraries needed to run the project. They're listed in requirements.txt. Try _python -m pip install -r requirements.txt --require-hashes_  
Note that libraries in requirements are specified with hashes because with that, there is no worries with DNSs problems.

###**How To Run The Application**
python main.py dataset=rent_the_runway  
Also, there is a executable.sh file, which can be used to run the same command as the command above
using _bash executable.sh_


###**What I Should Expect of the Application?**
**LOGS** - The logs are set as 'INFO', so, only debug information will be silenced. It helps to identify what the application
is doing in every single time.  
**STORAGE** - Everything that is downloaded or created, including the logs of the application, will be stored at storage/YYYY-MM-DD/

There are 5 questions that must be answered.

**Question 1 and Question 4**: A file will be generated for each of the questions. The file which answers the question 1 is called
'histograma_da_distribuicao_de_peso.png' and the file which answers the question 4 is called 'palavras_mais_usadas.png'.
The both are stored in the folder specified above.

**Question 2, Question 3 and Question 5**: The answer of each question of these will be printed at the screen in a organized way. 


###**.ENV**
The .env necessary to run this application is exemplified at .env.example.
Everything must be copied into a file called .env.
Two passwords are necessary to run the application, they are called AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
Both of the were given by e-mail.