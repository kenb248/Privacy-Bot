# Privacy-Bot

A Python project designed for use with google trends to simulate user interests and online activity. The program is intended for google users looking to secure their online privacy. Selecting words from a 300,000 strong list and then producing related queries based on that phrase, subsequently generating the appropriate websites. The program spends a period seemingly viewing the website content,  thereafter choosing a new randomised word from the 300,000 strong list. Users can thus ensure their online privacy remains exempt from google trends analysis. 

Required Packages:

-webbrowser
-googlesearch
-pytrends
-pandas


The program will search using your default browser.

On run specify the amount of time in minutes you want the program to search for,
the actual runtime may vary slightly as the program will not stop mid search when 
the time is reached.
