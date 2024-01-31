The guidelines below shows how to run the scripts.

1. Install the required modules in the modules.txt file using the pip command i.e

2. Install the required webdrivers and place the exe file in the planners directory i.e geckodriver,chromedriver

3. To run a specific script, open the terminal and type 

	scrapy crawl <name_of_script> -o <filename.json>

For example: to run reader.py
	scrapy crawl reader -o reader.json

You can use scrapy crawl <name_of_script> -o <filename.json> -------This appends new data to an existing file. 
You can use scrapy crawl <name_of_script> -O <filename.json> -------This Overwrites any existing file with the same name with the current data.
