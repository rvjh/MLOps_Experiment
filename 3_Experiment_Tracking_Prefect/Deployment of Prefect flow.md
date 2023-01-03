## Deployment of Prefect flow

create a new pythonfile **3_prefect_deployment.py** and copy the content from [2_prefect_flow.py](2_prefect_flow.py)
#### For model artifacts and all prefect also provide storage option
**prefect storage ls**
![img_18.png](img_18.png)
#### As we are usung cloud so we can create storage option : **prefect storage create**
![img_19.png](img_19.png)
#### lets say you choose local folder then specify the path and give a storage name
![img_20.png](img_20.png)

So whenever we register somethings the metadata will save in the .**prefect** folder

#### Now in 3_prefect_deployment.py remove the main() func. and import deployment specifications and run using 
**prefect deployment create 3_prefect_deployment.py**
![img_21.png](img_21.png)
![img_22.png](img_22.png)
![img_23.png](img_23.png)

#### you can create a workqueue for schedule task
![img_24.png](img_24.png)
![img_25.png](img_25.png)
you will get a workqueue id to copy
![img_26.png](img_26.png)
in terminal you can type **prefect work-queue preview <work-queue-id>** to get scheduled task
![img_27.png](img_27.png)

#### we can start any scheduled task by prefect agent start <ID>
![img_28.png](img_28.png)
![img_29.png](img_29.png)

!!END











