# DSProject1
First Project of Intro to Data Science Course at Flatiron

PROJECT DELIVERABLE:
https://rafa-stock-app.herokuapp.com/

QUESTION I WANT TO ANSWER: 
Is there any news which is driving the price of a security up or down?

METHOD APPLIED TO ANSWER QUESTION:
  a) Program obtains a list of relevant securities is obtained from IEX API
  b) User selects a security is selected from the Security drop-down, and a time period from the Time Period drop-down
  c) With the security name and time period selected,
      - program obtains from IEX API:
          - security prices throughout the period
          - company details, including:
                -  Company Name
                -  Company Exchange Ticker
                -  Exchange where Traded
                -  Industry
                -  Website
                -  Company Description
                -  CEO	
          
      - calculates some statistics on the security prices obtained:
            - record count 
            - max
            - min
            - stdev.
  
  d) Finally, weith the company ticker obtained above, the program searches the NYT API for any relevant news throughout the period.
  
  
APIs USED:
    IEX API: https://iextrading.com/developer
    NYT API: https://developer.nytimes.com/


EXECUTION AND PRESENTATION:
Project is presented as a website which can be publically accessed by anyone.
In order to visualize the project, please access https://rafa-stock-app.herokuapp.com/
Porgram is run by a Heroku Dyno, hosted at heroku.com


TO DOs
Make news search only search for news concearning the time period selected in the Time Period drop-down.
Make the presentation nicer on the eyes.
