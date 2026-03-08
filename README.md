Project done for fun to help mewgenics.wiki.gg fill out missing pages fo familiars as defined in the game code
If you want to run it yourself you will need to upcak the game files and place them in the apropriate directory
This project *does not* contain any of the game's code or assets

On the project:

The main callnges I faced making it were:
1. Following a complex, not well defined inharitance list
2. parsing through many game files, not knowing where the needed data saved
3. Missing information in the game files

1 and 2 I fixed by using a recursive function that can easily teminate when the desired value is found
3 sadly had to be filled in manually after the fact (see files)
