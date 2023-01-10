## Model Monitoring

![img.png](img.png)
#### So how to prepare for it ? -> Monitoring
![img_1.png](img_1.png)
#### Most of production models iterated in batch mode.
![img_2.png](img_2.png)
![img_3.png](img_3.png)
![img_4.png](img_4.png)

## create a dir prediction_service
#### inside that create a app.py file and copy the lin_reg.bin,requirements.txt file from previous module
#### inside prediction_service create a conda env **prediction_service**
![img_5.png](img_5.png)
in that env install requirements.txt
![img_6.png](img_6.png)
prepare the app.py file based on prepare.py file of 4th module 
![img_7.png](img_7.png)
Now create a dockerfile to save all so that we can run the services through docker compose
![img_8.png](img_8.png)

#### to install docker compose run **sudo apt-get install docker-compose** from terminal

from the official link i.e. https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/05-monitoring/docker-compose.yml
copy the **docker-compose.yml** file and change the python version to 3.9
Now up the docker using **docker compose up**
![img_9.png](img_9.png)

now from previous module copy test.py file into current dir



## modify the readme

#### downloading files using prepare.py file
![img_10.png](img_10.png)

#### now up the docker compose : **docker-compose up --build**


# Need to modify the readme








    

