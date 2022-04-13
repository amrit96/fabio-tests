# vectorAi

Models:
the models file hosts the orm tables: COntinent, Country, City

db_operations:
this file host the CRUD operation without any vaidation

utils:
this file host the basic validation while performing crud oprerations

Assusmptions:
while a region is created the population is the total population of all sub-regions combined. Therefore adding a sub region doesn't alter, rather limits their indivitual
population.
The same logic is assumed to be applicable for the area of the region as well.

Async task:
the CRUD operations were needed to be done using async ways. But I felt fetching data must be synchronous. Because in the scope of my code, all get results are needed for 
the very next step or as the final output. So an async get call would need the flow to hault and wait for the response. Which is prnciple of synchronous execution. 