## Remote Prefect Orion deployment

#### create a AWS EC2 instance and make it running
![img_4.png](img_4.png)
Now we need to add necessary security groupd rule to that particular instance
![img_5.png](img_5.png)
Add security rules like HTTP, Custom TCP, Custom UDP and HTTPS
![img_6.png](img_6.png)
Just reverify from instance that all the security groups have been added or not.
![img_7.png](img_7.png)

#### Now copy the public ip and from local using ssh connect to that instance
![img_9.png](img_9.png)

Install the required packages using **requirements.txt**

### **Refer this for more clarity**
![img_8.png](img_8.png)

#### now set the config for prefect and set external ip as public ip
![img_10.png](img_10.png)
![img_11.png](img_11.png)
you can reverify config by **prefect config view**

#### now you can start the orion : **prefect orion start --host 0.0.0.0**
![img_13.png](img_13.png)

#### now conect to public ip with port 4200 i.e. : <public_ip>:4200
![img_12.png](img_12.png)
![img_14.png](img_14.png)

#### you can configure prefect config from any IDE as well using http:// and run the flow
![img_15.png](img_15.png)

#### now refresh the ui to see the flow
![img_16.png](img_16.png)
![img_17.png](img_17.png)













